import sqlite3
import fcntl
import threading
from atomicwrite import AtomicFile


ROLL_BACK_LOG =  "master_rollback.log"

import logging
logger = logging.getLogger('master_store')
hdlr = logging.FileHandler('master_store.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)
DB = "master.db"

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    table = list(dbcur.execute('select name from sqlite_master where type="table"'))
    if table:
        dbcur.close()
        return True
    else:
        dbcur.close()
        return False
    dbcur.close()
    return False

class MasterStore(object):
    def __init__(self, key=None, value=None):
        self.key = key 
        self.value = value
        self.lock = threading.Lock()


    def create_table(self,con,tablename=None):
        cur = con.cursor()
        try:
            cur.execute("CREATE TABLE keyvalue (key int , value varchar(30))")
            logger.info("Successfully created sqlite3 table")
        except sqlite3.Error as e:
            logger.error("Failed to create sqlite3 table,: {}".format(e))
            raise
        return True

    def get_connection(self):
        con = sqlite3.connect(DB)
        if not checkTableExists(con,'keyvalue'):
            self.create_table(con)
        return con

    def execute(self,con,stmt):
        try:
            result = con.execute(stmt)
            logger.info("Successfully executed {} to sqlite3".format(stmt))
        except sqlite3.Error as e:
            logger.error("Failed to  executed {} to sqlite3, Error:{}".format(stmt,e) )
            return False
        return result

    def get_sql_stmt(self,action):
        '''
            No roll back for get actions
            Every time the cursor should be executing the 1st statment and logging the second one for the roll_back
        '''
        if action=="PUT" and self.value is not None:
            ex_stmt = "INSERT INTO keyvalue (key , value ) VALUES ({},\"{}\")".format(self.key, self.value)
            roll_back = "DELETE FROM keyvalue WHERE key={}".format(self.key)
        elif action == "DEL":
            ex_stmt = "DELETE FROM keyvalue WHERE key={}".format(self.key)
            roll_back = "INSERT INTO keyvalue (key , value ) VALUES ({},\"{}\" )".format(self.key, self.value)

        return (ex_stmt,roll_back)


    def commited(self,key):
        with open(ROLL_BACK_LOG,'r') as f: # While reading i will not need a lock. 
            lines = f.readlines()
        for line in lines:
            if line.split("-")[1] == str(key):
                return False
        else:
            return True


    def get(self, key ):
        '''
            Get operation should not work if key being still been operated on
        '''
        if not self.commited(key):
            return 'Error: Not availabe for read'

        sql =  "SELECT key, value FROM keyvalue WHERE key={}".format(key)
        print sql
        with self.get_connection() as con:
            result = list(con.execute(sql))
        if len(result) > 0:
            return (result[0][0],result[0][1])
        else:
            return None


    def update_roll_back_log(self, seq ):
        self.lock.acquire()
        with open(ROLL_BACK_LOG,'r') as f: # While reading i will not need a lock. 
            lines = f.readlines()

        # I think whole of this has to be Locked, as i dont want these two variables to be changed by the time they reach a stage where 
        #they are being written to the file
        # But also before coming here my wrapper is going to check if the key is being operated on.

        line_to_delete = []
        lines_to_append = []
        try:
            for line in lines:
                if str(line.split("-")[0]) == str(seq):
                    line_to_delete = line
                else:
                    lines_to_append.append(line)

            with AtomicFile(ROLL_BACK_LOG, 'r+') as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    f.truncate()
                    fcntl.flock(f, fcntl.LOCK_UN)
            if lines_to_append:
                with AtomicFile(ROLL_BACK_LOG, 'r+') as f: # Here the contents of the file change and hence the locks 
                    fcntl.flock(f, fcntl.LOCK_EX)
                    for write_line in lines_to_append:
                        f.write(write_line)
                    fcntl.flock(f, fcntl.LOCK_UN)
        except ValueError:
            logger.error("Cound not comeplete the operation there was a exception" )
            raise
        finally:
            self.lock.release()
            logger.info("Giving up Lock:Updating roll_back log")
            if line_to_delete:
                return line_to_delete
            else:
                return True


    def append_roll_back_log(self,seq , key ,stmt):
        with AtomicFile(ROLL_BACK_LOG, 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write("{}-{}-{}\n".format(seq,key,stmt))
            fcntl.flock(f, fcntl.LOCK_UN)
        return True

    def delete(self,seq, key ): 
        '''
        May be i shoud also check if have the key before deleting
        '''
        key_value  = self.get(key)
        if key_value:
            (self.key, self.value) = key_value
            sql = self.get_sql_stmt("DEL")
            if self.append_roll_back_log(seq,self.key,sql[1]):
                with self.get_connection() as con:
                    if self.execute(con,sql[0]):
                        return True
                    else:
                        self.update_roll_back_log(seq)
        return False

    def put(self,seq):
        sql = self.get_sql_stmt("PUT")
        ## With file handle we will have to wrte sql[1]  and sel to a file
        if self.append_roll_back_log(seq,self.key,sql[1]):
            with self.get_connection() as con:
                if self.execute(con,sql[0]):
                    return True
                else:
                    self.update_roll_back_log(seq)
                    return False
        return False


    def roll_back(self,seq):
        stmt = self.update_roll_back_log(seq)
        if type(stmt) != bool:
            with self.get_connection() as con:
                stmt = stmt.strip('\n').split("-")[2]
                if self.execute(con, stmt):
                    return True
                else:
                    return False



    def commit(self,seq):
        '''
            delete the seq entry fro the file.(To accomadate nested queries move the stuff to another log)
        '''
        if self.update_roll_back_log(seq):
            return True
        else:
            print "wtf"
            return False

    def get_master_keys(self):
        sql = "SELECT key from keyvalue"
        with self.get_connection() as con:
            results = list(self.execute(con,sql))

        results  = [ x[0] for x in results ]
        results = '-'.join(str(x) for x in results) 
        return results


# d = DataStore(220,"Another attempt to check get without parameter")
# d.put(150)

# print d.get(220)

# d =  DataStore()
# d.commit(150)

# d = DataStore(2900,"Another attempt to check get without parameter")
# d.put(180)

# ds =  DataStore()
# print ds.get(220)[1]

# d = DataStore()
# print d.get(200)

# d = DataStore()
# print d.get(12)
