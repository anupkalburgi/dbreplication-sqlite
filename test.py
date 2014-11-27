from cord import replicas_put,replicas_get,replicas_del
from threading import Thread

DATA = [(30000,"Testing replication"),(35000,"Concurrent"),(45000,"Not fault tollerent"),(28000,"and my attept")]

threads = []
responses = [[] for i in range (len(DATA) ) ]

PROCESSING = []


def put(key,value):
	if key in PROCESSING:
		return "Cannot do this operation"
	else:
		PROCESSING.append(key)
		resp = replicas_put(key,value)
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


