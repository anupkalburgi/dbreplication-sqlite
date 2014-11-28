from cord import replicas_put,replicas_get,replicas_del, SEQ , all_synced
from masterstore import MasterStore
from threading import Thread
from cord_connect import client 

DATA = [(913,"Testing replication"),(112,"Concurrent"),(214,"Not fault tollerent"),(219,"and my attept")]

threads = []
responses = [[] for i in range (len(DATA) ) ]

PROCESSING = []



def sync():
	sync_ed = all_synced()
	print "Not Cync"
	if type(sync_ed) is not bool:
		master_keys = sync_ed[1][1].split('-')
		responses = sync_ed[1][0]


		out_of_sync = filter(lambda item : not set( item[0]['message'].split('-'))  == set(master_keys) \
			or not len( item[0]['message'].split('-'))  == len(master_keys) , responses )

		for server in out_of_sync:
			server_keys = server[0]['message'].split('-')  
			print server_keys
			print master_keys
			missing_key = list (set(master_keys)  - set(server_keys) )
			if missing_key:
				for key in missing_key:
					kv = MasterStore().get(key)
					print server['server']
					if type(kv) is not bool:
						print server['server']
						response = []
						seq = SEQ.next()
						if client(server['server'] , "{};put;{};{}".format(seq,kv[0],kv[1]) , response ,seq):
							if client(server['server'] , "{};com;;".format(seq), response, seq):
								pass

			# extra_keys = list (set(server_keys)  - set(missing_key) )
			# if extra_keys:
			# 	logger,info("Replica {} has extra keys".format(server['server']))
			# 	#Will have to delete extra keys from the replica
			
			keys = []
			dup_keys = []
			for key in server_keys:
				print key
				if key in keys:
					print "Dup"
					dup_keys.append(key)
				else:
					keys.append(key)
					

			print dup_keys
			print keys
			if dup_keys:
				print "I have dups"
				for key in dup_keys:
					seq = SEQ.next()
					if client(server['server'] , "{};del;{};".format(seq,kv[0]) , response):
						if client(server['server'] , "{};com;;".format(seq) , response):
							pass




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


