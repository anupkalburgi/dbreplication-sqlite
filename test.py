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

		for replica in replics:
			for key in master:
				if key not in replica:
					put

			for key in replica:
				if key not in master:
					del key from relica

			for resp in sync_ed[0]:
				if len(resp[0]['message']) != len(keys):
					print "Will have to sync up", resp
	else:
		print "Synced"



def put(key,value):
	if key in PROCESSING:
		print "Cannot do this operation"
		return "Cannot do this operation"
	else:
		PROCESSING.append(key)
		seq = SEQ.next()
		ms = MasterStore(key,value)
		ms.put(seq)
		resp = replicas_put(key,value)
		if resp:
			ms.commit(seq)
		else:
			ms.roll_back(seq)
		PROCESSING.remove(key)

def cdel(key):
	if key in PROCESSING:
		print "Cannot do this operation"
		return "Cannot do this operation"
	else:
		PROCESSING.append(key)
		seq = SEQ.next()
		ms = MasterStore(key,value)
		ms.delete(seq)
		resp = replicas_del(key)
		if resp:
			ms.commit(seq)
		PROCESSING.remove(key)

for i in range(len(DATA)):
        t = Thread(target=put,args=( DATA[i][0],DATA[i][1] )) 
        t2 = Thread(target=put,args=( DATA[i][0],DATA[i][1] )) 
        threads.append(t)
        threads.append(t2)
        t.start()
        t2.start()

results = []
for t in threads:
        t.join()

# sync()


