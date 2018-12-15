# -*- coding: utf-8 -*-
from __future__ import with_statement
from fabric import *
import json

#setup

with open('project-info.json',encoding = 'UTF-8') as f:
        config = json.loads(f.read(),encoding='utf-8')

project_dir = config['projectDir']
project = config['project']

c = Connection(config["host"],config["user"])
c.config.run['replace_env'] = False

detailedTag = c.local('git describe --tags',hide=True)
tag = float(detailedTag.stdout[1:4].strip())

@task
def commit(arg):
	c.local('pipreqs --force .')
	c.local('git add -p')
	c.local('git commit')
	c.local('git push')

#end setup
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
    global tag
    c.local('git tag ' + tag)
    c.local('git push origin' + tag)

def checkRemoteMachine():
    global tag
    exists = c.run("[ -d {}{} ] && echo 'True' || echo 'False'".format(project_dir,project)).stdout.strip()

    if(exists == 'False'):
        c.sudo("mkdir {}".format(project_dir))
        with c.cd(project_dir):
                c.run("git clone {}".format(config['repo']))
            
def checkoutTag():
    with c.cd("{}{}".format(project_dir,project)):
        c.run("git checkout tags/v{}".format(str(tag)))


def buildDependancies():
	with c.cd("{}{}".format(project_dir,project)):
		c.run("pip install -r requirements.txt")

def restartService():
    c.run("{}".format(config['entry']))