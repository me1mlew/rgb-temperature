from __future__ import with_statement
from fabric import *
import json

with open('project-info.json') as f:
        config = json.load(f)

c = Connection(config["host"],config["user"])
c.config.run['replace_env'] = False

detailedTag = c.local('git describe --tags',hide=True)
tag = float(detailedTag.stdout[1:])

@task
def release(arg):
    iterateTag(0.1)
    
@task
def release_major(arg):
    iterateTag(1.0)

def iterateTag(step):
    global tag 
    tag += step
    print(str(tag))

def createNewTag():
    #todo create new tag in github
    global tag

def checkRemoteMachine():
    #todo check if dir is on remote machine
    global tag

def checkoutTag():
    #todo checkout tag on remote machine
    global tag

def buildDependancies():
    #todo build dependancies
    global tag

def restartService():
    #retart the applciation on the machine
    global tag