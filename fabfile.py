# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric import *
import json
import math

#setup

with open('project-info.json',encoding = 'UTF-8') as f:
        config = json.loads(f.read(),encoding='utf-8')

PROJECT_DIR = config['projectDir']
PROJECT = config['project']
REPO = config['repo']
ENTRY_POINT = config['entry']
EXEC_BIN = config['exec']

c = Connection(config["host"],config["user"])
c.config.run['replace_env'] = False

detailedTag = c.local('git describe --tags',hide=True).stdout.strip()
tag = float(detailedTag[:detailedTag.find('-')])

#must be run on command line
@task
def commit(arg):
	c.local('pipreqs --force .')
	c.local('git add .')
	c.local('git commit')
	c.local('git push')

#end setup

@task
def release(arg):
    iterateTag(0.1)
    createNewTag()
    checkRemoteMachine()
    checkoutTag()
    buildDependancies()
    restartService()
    
@task
def release_major(arg):
    iterateTag(1.0)
    createNewTag()
    checkRemoteMachine()
    checkoutTag()
    buildDependancies()
    restartService()
    
def iterateTag(step):
    global tag 
    print("Current verion: v" + str(tag))
    tag += step
    if step == 1:
        tag = math.floor(tag,2)
    print("Upgrading to version: v" + str(tag))

def createNewTag():
    global tag
    c.local('git tag {}'.format(str(tag)))
    c.local('git push origin {}'.format(str(tag)))

def checkRemoteMachine():
    global tag
    exists = c.run("[ -d {}{} ] && echo 'True' || echo 'False'".format(PROJECT_DIR,PROJECT)).stdout.strip()

    if(exists == 'False'):
        c.sudo('bash -c "cd {} && git clone {}"'.format(PROJECT_DIR,REPO))
            
def checkoutTag():
    c.sudo('bash -c "cd {} && git fetch && git checkout tags/{}"'.format(PROJECT_DIR+PROJECT,tag))

def buildDependancies():
    c.sudo('bash -c "cd {} && pip install -r requirements.txt"'.format(PROJECT_DIR+PROJECT))

def restartService():
    c.run("{} {}{}/{}".format(EXEC_BIN,PROJECT_DIR,PROJECT,ENTRY_POINT))
