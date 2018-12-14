from __future__ import with_statement
from fabric import *
import json

with open('project-info.json') as f:
    config = json.load(f)

c = Connection(config["host"],config["user"])
local = Connection('localhost')

@task
def release(v):
    checkVersion(float(v))

def checkVersion(version):
    #print(float(config["version"])
    if (version <= config["version"]):
        local.run('Project is currently V' % config["version"])