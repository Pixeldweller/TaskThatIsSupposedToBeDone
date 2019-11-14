# coding:utf-8

# Demonstrator es/te/tm

import sys
import os.path
import cherrypy

from app import application, template
from app.objects import custom, projects, components, employees, categories, bugs, report

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
      projects.Projects_cl(currentDir_s),
      '/projekt',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      projects.ProjectComponent_cl(currentDir_s),
      '/projektkomponenten',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )


   cherrypy.tree.mount(
      components.Component_Cl(currentDir_s),
      '/komponente',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      employees.QualityManagement_Cl(currentDir_s),
      '/qsmitarbeiter',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )


   cherrypy.tree.mount(
      employees.SoftwareDeveloper_Cl(currentDir_s),
      '/swentwickler',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )


   cherrypy.tree.mount(
      categories.BugCategory_cl(currentDir_s),
      '/katfehler',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      categories.CauseCategory_cl(currentDir_s),
      '/katursache',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      bugs.Bugs_cl(currentDir_s),
      '/fehler',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )


   cherrypy.tree.mount(
       employees.Employee_cl(currentDir_s),
      '/mitarbeiter',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      categories.Category_cl(currentDir_s,""),
      '/kategorie',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
      report.Prolist_cl(currentDir_s),
      '/prolist',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.tree.mount(
        report.Katlist_cl(currentDir_s),
      '/katlist',
      {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}}
   )

   cherrypy.engine.start()
   cherrypy.engine.block()

#----------------------------------------------------------
if __name__ == '__main__':
#----------------------------------------------------------
   main()