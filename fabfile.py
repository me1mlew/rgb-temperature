# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric import *
import json

#setup

with open('project-info.json',encoding = 'UTF-8') as f:
        config = json.loads(f.read(),encoding='utf-8')

project_dir = config['projectDir']
project = config['project']
repo = config['repo']
entryPoint = config['entry']
execBin = config['exec']

c = Connection(config["host"],config["user"])
c.config.run['replace_env'] = False

detailedTag = c.local('git describe --tags',hide=True)
tag = float(detailedTag.stdout[1:3].strip())

#must be run ono command line
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
    print("Upgrading to version: v" + str(tag))

def createNewTag():
    global tag
    c.local('git tag {}'.format(str(tag)))
    c.local('git push origin {}'.format(str(tag)))

def checkRemoteMachine():
    global tag
    exists = c.run("[ -d {}{} ] && echo 'True' || echo 'False'".format(project_dir,project)).stdout.strip()

    if(exists == 'False'):
        c.sudo('bash -c "cd {} && git clone {}"'.format(project_dir,repo))
            
def checkoutTag():
    c.sudo('bash -c "cd {} && git fetch && git checkout tags/{}"'.format(project_dir+project,tag))

def buildDependancies():
    c.sudo('bash -c "cd {} && pip install -r requirements.txt"'.format(project_dir+project))

def restartService():
    c.run("{} {}{}/{}".format(execBin,project_dir,project,entryPoint))