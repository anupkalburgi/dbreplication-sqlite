import sqlite3
import fcntl

ROLL_BACK_LOG =  "roll_back.log"

import logging
logger = logging.getLogger('data_store')
hdlr = logging.FileHandler('data_store.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


def checkTableExists(dbcon, tablename):
	dbcur = dbcon.cursor()
	table = dbcur.execute('select name from sqlite_master where type="table"')
	if 'keyvalue' in table.fetchone()[0]:
		dbcur.close()
		return True
	else:
		dbcur.close()
		return False

	dbcur.close()
	return False

class DataStore(object):
	def __init__(self, key=None, value=None):
		self.key = key 
		self.value = value

	def create_table(con,tablename=None):
		cur = con.cursor()
		try:
			cur.execute("CREATE TABLE keyvalue (key int , value varchar(30))")
			logger.info("Successfully created sqlite3 table")
		except sqlite3.Error as e:
			logger.error("Failed to create sqlite3 table,: {}".format(e))
			raise
		return True

	def get_connection(self):
		con = sqlite3.connect('test.db')
		if not checkTableExists(con,'keyvalue'):
			self.create_table(con)
		return con

	def execute(self,con,stmt):
		try:
			con.execute(stmt)
			logger.info("Successfully executed {} to sqlite3".format(stmt))
		except sqlite3.Error as e:
			logger.error("Failed to  executed {} to sqlite3, Error:{}".format(stmt,e) )
			raise
		return True

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


	def get(self, key ):
		'''
			Get operation should not work if key being still been operated on
		'''
		sql =  "SELECT key, value FROM keyvalue WHERE key={}".format(key)
		with self.get_connection() as con:
			cur = con.cursor()
			result = cur.execute(sql)
		if result.rowcount > 1:
			return result.fetchone()[1]
		else:
			return None

	def update_roll_back_log(self, seq ):
		with open(ROLL_BACK_LOG,'r') as f: # While reading i will not need a lock. 
			lines = f.readlines()

		# I think whole of this has to be Locked, as i dont want these two variables to be changed by the time they reach a stage where 
		#they are being written to the file
		# But also before coming here my wrapper is going to check if the key is being operated on.
		line_to_delete = []
		lines_to_append = []

		for line in lines:
			print line.split("-")[0], seq
			if line.split("-")[0] == str(seq):
				print "lot it"
				line_to_delete = line
			else:
				lines_to_append.append(line)
		print line_to_delete
		if line_to_delete:
			with open(ROLL_BACK_LOG, 'r+') as f: # Here the contents of the file change and hence the locks 
				fcntl.flock(f, fcntl.LOCK_EX)
				for write_line in lines_to_append:
					f.write(write_line)
				fcntl.flock(f, fcntl.LOCK_UN)
			return True
		else:
			return False


	def append_roll_back_log(self,seq, stmt):
		with open(ROLL_BACK_LOG, 'a') as f:
			fcntl.flock(f, fcntl.LOCK_EX)
			f.write("{}-{}\n".format(seq,stmt))
			fcntl.flock(f, fcntl.LOCK_UN)
		return True

	def delete(self,seq): 
		'''
		May be i shoud also check if have the key before deleting
		'''
		sql = self.get_sql_stmt("DEL")
		if self.append_roll_back_log(seq,sql[1]):
			with self.get_connection() as con:
				if self.execute(con,sql[0]):
					return True
				else:
					return False

	def put(self,seq):
		sql = self.get_sql_stmt("PUT")
		## With file handle we will have to wrte sql[1]  and sel to a file
		if self.append_roll_back_log(seq,sql[1]):
			with self.get_connection() as con:
				if self.execute(con,sql[0]):
					return True
				else:
					return False

		# write the seq num and equivalanet roll back stmt
		# commit to DB 
		# return 



	def commit(self,seq):
		'''
			delete the seq entry fro the file.(To accomadate nested queries move the stuff to another log)
		'''
		if self.update_roll_back_log(seq):
			print "Dot it "
			return 'Done'
		else:
			print "wtf"
			return False


d = DataStore(20,"Another attempt to check")
d.put(124)

d = DataStore()
print d.get(20)

d =  DataStore()
d.commit(124)

# d = DataStore()
# print d.get(12)
