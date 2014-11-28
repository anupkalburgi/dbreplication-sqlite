from cord import replicas_put,replicas_get,replicas_del, SEQ
from masterstore import MasterStore
from threading import Thread

DATA = [(1300,"Testing replication"),(1350,"Concurrent"),(1450,"Not fault tollerent"),(1280,"and my attept")]

threads = []
responses = [[] for i in range (len(DATA) ) ]

PROCESSING = []



def put(key,value):
	if key in PROCESSING:
		print "Cannot do this operation"
		return "Cannot do this operation"
	else:
		PROCESSING.append(key)
		resp = replicas_put(key,value)
		if resp:
			seq = SEQ.next()
			ms = MasterStore(key,value)
			ms.put(seq)
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


