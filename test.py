from cord import replicas_put,replicas_get,replicas_del, SEQ , all_synced
from masterstore import MasterStore
from threading import Thread

DATA = [(913,"Testing replication"),(112,"Concurrent"),(214,"Not fault tollerent"),(219,"and my attept")]

threads = []
responses = [[] for i in range (len(DATA) ) ]

PROCESSING = []



def sync():
	sync_ed = all_synced()
	if type(sync_ed) is not bool:
		print "Not Sycn", sync_ed
		for resp in sync_ed:
			if len(resp[0]['message']) != len(keys):
				print "Will have to sync up", resp
	else:
		print "Synced"



# def put(key,value):
# 	if key in PROCESSING:
# 		print "Cannot do this operation"
# 		return "Cannot do this operation"
# 	else:
# 		PROCESSING.append(key)
# 		resp = replicas_put(key,value)
# 		if resp:
# 			seq = SEQ.next()
# 			ms = MasterStore(key,value)
# 			ms.put(seq)
# 			ms.commit(seq)
# 		PROCESSING.remove(key)

# for i in range(len(DATA)):
#         t = Thread(target=put,args=( DATA[i][0],DATA[i][1] )) 
#         t2 = Thread(target=put,args=( DATA[i][0],DATA[i][1] )) 
#         threads.append(t)
#         threads.append(t2)
#         t.start()
#         t2.start()

# results = []
# for t in threads:
#         t.join()

sync()


