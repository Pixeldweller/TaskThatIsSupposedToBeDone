# coding:utf-8

# Demonstrator es/te/tm

import sys
import os.path
import cherrypy

from app import application, template
from app.objects import events, exhibitors, organizers, bookings

#----------------------------------------------------------
def main():
#----------------------------------------------------------

   # aktuelles Verzeichnis ermitteln, damit es in der Konfigurationsdatei als
   # Bezugspunkt verwendet werden kann
   try:                                    # aktuelles Verzeichnis als absoluter Pfad
      currentDir_s = os.path.dirname(os.path.abspath(__file__))
   except:
      currentDir_s = os.path.dirname(os.path.abspath(sys.executable))
   cherrypy.Application.currentDir_s = currentDir_s

   configFileName_s = os.path.join(currentDir_s, 'server.conf') # im aktuellen Verzeichnis
   if os.path.exists(configFileName_s) == False:
      # Datei gibt es nicht
      configFileName_s = None

   # autoreload-Monitor hier abschalten
   cherrypy.engine.autoreload.unsubscribe()


   # 1. Eintrag: Standardverhalten, Berücksichtigung der Konfigurationsangaben im configFile
   cherrypy.tree.mount(
      None, '/', configFileName_s
   )

   # 2. Eintrag: Method-Dispatcher für die "Applikation" "app" vereinbaren
   cherrypy.tree.mount(
      application.Application_cl(currentDir_s),
      '/app',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )


   # 2. Eintrag: Method-Dispatcher für die "Applikation" "templates" vereinbaren
   cherrypy.tree.mount(
      template.Template_cl(),
      '/templates',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   # X. Eintrag:
   cherrypy.tree.mount(
      organizers.Organizer_cl(currentDir_s),
      '/organizer',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      exhibitors.Exhibitors_cl(currentDir_s),
      '/exhibitor',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      bookings.Bookings_cl(currentDir_s),
      '/booking',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      events.Events_cl(currentDir_s),
      '/event',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )



   cherrypy.engine.start()
   cherrypy.engine.block()

#----------------------------------------------------------
if __name__ == '__main__':
#----------------------------------------------------------
   main()