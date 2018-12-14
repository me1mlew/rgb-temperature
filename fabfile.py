# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric import *
import json

with open('project-info.json',encoding = 'UTF-8') as f:
        config = json.loads(f.read(),encoding='utf-8')

project_dir = config['projectDir'] + config['project']
project = config['project']

c = Connection(config["host"],config["user"])
c.config.run['replace_env'] = False

detailedTag = c.local('git describe --tags',hide=True)
tag = float(detailedTag.stdout[1:4].strip())

@task
def release(arg):
    iterateTag(0.1)
    checkRemoteMachine()
    
@task
def release_major(arg):
    iterateTag(1.0)

def iterateTag(step):
    global tag 
    print("Current verion: v" + str(tag))
    tag += step
    print("Upgrading to version: v" + str(tag))

def createNewTag():
    #todo create new tag in github
    global tag
    c.local('git tag ' + tag)
    c.local('git push origin' + tag)

def checkRemoteMachine():
    #todo check if dir is on remote machine
    global tag 
    test='/usr/local/bin/test'
    exists = c.run("[ -d {} ] && echo 'True' || echo 'False'".format(project_dir)).stdout.strip()

    if(exists == 'False'):
        c.sudo("mkdir {}".format(project_dir))
    
def checkoutTag():
    #todo checkout tag on remote machine
    global tag

def buildDependancies():
    #todo build dependancies
    global tag

def restartService():
    #retart the applciation on the machine
    global tag