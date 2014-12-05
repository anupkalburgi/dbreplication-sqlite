from cord_connect import client , REPLICA, logger
from threading import Thread
import random

from masterstore import MasterStore


def get_seq():
    number = 5
    while True:
        yield number
        number += 1
SEQ = get_seq() 


def replicas_put(key, value):
    threads = []
    responses = [[] for i in range (len(REPLICA) ) ]
    seq = SEQ.next()
    for i in range(len(REPLICA)):
            t = Thread(target=client,
                    args=(REPLICA[i], "{};put;{};{}".format(seq,key,value), responses[i] , seq)  )
            threads.append(t)
            t.start()
    results = []
    for t in threads:
            t.join()

    for response in responses:
            if response[0]['status'] == 'False':
                print "Could not connect to one of the servers Please check"
                print response[0]['server']
                #return False

    if all(message[0]['status'] == 'True'  for message in responses):
        print "All worked fine"
        commit_reponses = [[] for i in range(len(responses)) ]
        commit_threads = []
        for i in range(len(responses)):
            t = Thread(target=client,
                        args=(responses[i][0]['server'], 
                            "{};com;;".\
                            format(responses[i][0]['seq']), 
                            commit_reponses[i] , 
                            seq
                        ))
            commit_threads.append(t)
            t.start()

        for t in commit_threads:
            t.join()
        logger.error("Data Commted to all the replicas")
        return True

    else:
        print "Commit failed"
        logger.error("Aborting, put operation has failed {}".format((key,value)))
        failed_threads = filter( lambda x : bool( x[0]['status']=='False') , responses )
        succeded_threads = filter( lambda x : bool( x[0]['status']=='True') , responses )

        if succeded_threads:
            logger.error("Aborting the succeded_threads threads {}".format(succeded_threads))
            for i in range(len(succeded_threads)):
                print "succeded_threads", succeded_threads[i][0]['server']
                abort_reponses = [[] for i in range(len(succeded_threads)) ]
                abort_threads = []
                t = Thread(target=client,
                        args=(succeded_threads[i][0]['server'],
                            "{};abort;;".format(succeded_threads[i][0]['seq']), 
                            abort_reponses[i] , 
                            seq
                        ))
                abort_threads.append(t)
                t.start()
            for t in abort_threads:
                t.join()
        else:
            logger.error("Aswesome all of them failed")
        return False


def replicas_get(key):
    server = random.choice(REPLICA)
    response = []
    print server  
    resp = client(server, ";get;{};".format(key),response)
    return response


def all_same(items, master):
    for item in items:
        if len(item[0]['message']) == len(master):
            if len(item[0]['message']) == len(master) ==0:
                pass
            elif  not set( item[0]['message'].split('-') ) == set( master.split('-') ):
                return False
        else:
            return False
    else:
        return True


def all_synced():
    threads = []
    responses = [[] for i in range (len(REPLICA) ) ]

    for i in range(len(REPLICA)):
            t = Thread(target=client,args=(REPLICA[i], ";keys;;" , responses[i]))
            threads.append(t)
            t.start()

    for t in threads:
            t.join()

    master_keys = MasterStore().get_master_keys()
    if all_same(responses, master_keys):
        return True
    else:
        return (False,[responses,master_keys] )



def replicas_del(key):
    threads = []
    responses = [[] for i in range (len(REPLICA) ) ]
    seq = SEQ.next()
    for i in range(len(REPLICA)):
            t = Thread(target=client,
                    args=(REPLICA[i], "{};del;{};".format(seq,key), responses[i] , seq)  )
            threads.append(t)
            t.start()

    results = []
    for t in threads:
            t.join()

    print responses
    if all(message[0]['status'] == 'True'  for message in responses):
        print "All worked fine"
        logger.info("All worked fine with {}".format((key)))
        commit_reponses = [[] for i in range(len(responses)) ]
        commit_threads = []
        for i in range(len(responses)):
            t = Thread(target=client,
                        args=(responses[i][0]['server'], 
                            "{};com;;".\
                            format(responses[i][0]['seq']), 
                            commit_reponses[i] , 
                            seq
                        ))
            commit_threads.append(t)
            t.start()

        for t in commit_threads:
            t.join()
        logger.error("Data Commted to all the replicas")
        return True

    else:
        print "Commit failed"
        logger.error("Aborting, put operation has failed {}".format((key)))
        failed_threads = filter( lambda x : bool( x[0]['status']=='False') , responses )
        succeded_threads = filter( lambda x : bool( x[0]['status']=='True') , responses )

        if succeded_threads:
            logger.error("Aborting the succeded_threads threads {}".format(succeded_threads))
            for i in range(len(succeded_threads)):
                print succeded_threads[i][0]['server']
                abort_reponses = [[] for i in range(len(succeded_threads)) ]
                abort_threads = []
                t = Thread(target=client,
                        args=(succeded_threads[i][0]['server'],
                            "{};abort;;".format(succeded_threads[i][0]['seq']), 
                            abort_reponses[i] , 
                            seq
                        ))
                abort_threads.append(t)
                t.start()
            for t in abort_threads:
                t.join()
        else:
            logger.error("Aswesome all of them failed")
        return False

#replicas_put(101,'new_test_data')
# replicas_del(101)




#replicas_get(102)


    # for response in responses:
    #     if response[0]['status'] == 'True':
    #         abort_thread = []



# print commit_reponses




# TODO:
# Make this concurrent
# Test for replication

# for i in range(1,20):
#     thread = Thread(target = client, args = ('127.0.0.1',, "{};abort;;".format(i) ))


#     #thread = Thread(target = client, args = ('127.0.0.1',, "{};com;;".format(i) ))
    
#     # thread = Thread(target = client, args = ('127.0.0.1',, ";get;{};".format(i) ))
#     # thread = Thread(target = client, args = ('127.0.0.1',, "{};del;{};".format(i+1,i) ))
#     thread.start()
#     thread.join()

# client('127.0.0.1', 55218, "Hello World 1")
# client('127.0.0.1', 55218, "Hello World 2")
# client('127.0.0.1', 55218, "Hello World 3")