from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.user = 'anupk'
env.password = 'Anup1107'
env.always_use_pty = False
code_dir = '/home/anupk/dbreplication-sqlit'

def replicas():
    # env.hosts = ['medusa-node2.vsnet.gmu.edu',\
    #              'medusa-node3.vsnet.gmu.edu',\
    #              'medusa-node4.vsnet.gmu.edu',\
    #              'medusa-node5.vsnet.gmu.edu']

    env.hosts = REPLICA = ['129.174.55.248']

# def bootstrap():
#     env.hosts = ['medusa-node1.vsnet.gmu.edu']


def update():
    with settings(warn_only=True):
        if not run("test -d %s" % code_dir).failed:
            run('rm -rf %s' % code_dir)
        run("git clone  https://github.com/anupkalburgi/dbreplication-sqlite.git %s" % code_dir)
        # run("sleep 1")
        # run("cd %s;mkdir -p logs;touch logs/errors.log" % code_dir)


def deploy():
    #TODO--Before starting of with command check if the directoy exists
    with settings(warn_only=True):
        #run('export PYRO_SERIALIZERS_ACCEPTED=serpent,json,marshal,pickle') Right now i have it my \
        # in my bash_profile, that will not work at scale
        # Right way of doing it is http://stackoverflow.com/questions/8313238/best-way-to-add-an-environment-variable-in-fabric
        run("cd %s;python threaded_server.py  >& /dev/null < /dev/null &" %code_dir)

def status():
    run("ps -ef | grep python threaded_server")

def kill():
    run("fuser -k 50504/tcp;sleep 1")


# def shut_down():
#     kill()
#     stop()



