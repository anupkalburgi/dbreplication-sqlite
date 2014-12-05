python version: 2.7 
No external dependency. SqlLite3 Library for data persistence. 


fab file commands:
-------------------

	fab -f fab.py replicas update   ## Fetches  code from git and deploys to the specified dir
	fab -f fab.py replicas deploy   ## Starts the threaded servers for replicas
	fab -f fab.py replicas kill		## Brings down all the replica server processes



python cord_server.py  -- Starts the master node. Checks all nodes are up and sync up with all replicas

	assign4->$python cord_server.py
	Could not connect to one of the servers Please check
	We have got a problem
	assign4->$	


test.py has the test code i used. Every file has test code at the end of the file. 


The master and Roll back log
----------------------------
master_rollback.log 
roll_back.log 


All the major events in the program as recorded in here
-------------------------------------------------------
master_store.log 
data_sotre.log


All the questions and the design choices are explained in the following documents.

Design and Implementations details: design_doc.txt and implementation.txt 
-----------------------------------
design decisions  - ACID properties and way of choices to implement them. 
and implementation details - API class, structure and arguments




