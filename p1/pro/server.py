# coding: utf-8

import os.path
import cherrypy
import sys

from app import application

def main():

    try:
        currentDir = os.path.dirname(os.path.abspath(__file__))
    except:
        currentDir = os.path.dirname(os.path.abspath(sys.executable))
    cherrypy.Application.currentDir = currentDir

    configFileName = 'server.conf'
    if os.path.exists(configFileName) == False:
        configFileName = None

    cherrypy.engine.autoreload.unsubscribe()
    #cherrypy.engine.timeout_monitor.unsubscribe()

    cherrypy.quickstart(application.Application(currentDir), config=configFileName)

if __name__ == '__main__':
    main()
