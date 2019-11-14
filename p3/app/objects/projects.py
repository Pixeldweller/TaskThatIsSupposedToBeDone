# coding: utf-8

# Demonstrator / keine Fehlerbehandlung

import cherrypy

from p3.app.database import Database_cl
from p3.app.view import View_cl

# Method-Dispatching!

# Übersicht Anforderungen / Methoden

"""
Anforderung               GET         PUT          POST          DELETE
-----------------------------------------------------------------------------
projekt/                  Alle         -           Ein neues       -
                          Projekte                 Projekt       
                          liefern                  anlegen       
-----------------------------------------------------------------------------
projekt/id                Ein         Ein           -            Ein
projekt/?id=id            Projekt     Projekt                    Projekt
                          liefern     updaten                    loeschen
------------------------------------------------------------------------------
projektkomponenten/id     Komponenten   -           -             -
projektkomponenten/?id=id gemäß Projekt    
                          ID liefern     
-----------------------------------------------------------------------------
"""


# ----------------------------------------------------------
class Projects_cl(object):
    # ----------------------------------------------------------

    exposed = True

    # -------------------------------------------------------
    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        if id is None:
            return self.db.readFile('project.json')['data']

        data = self.db.findId("project.json", id)
        if not data is None:
            data_components = self.db.readFile('component.json')['data']
            data['component_name'] = []
            for entry in data['component']:
                data['component_name'].append(data_components[entry]['name'])
            return data
        return self.view_o.createAlert("Projekt ID ist nicht Vorhanden.")

    @cherrypy.tools.json_out()
    def POST(self, title, desc):
        return {
            "id": self.createProject(title=title, desc=desc)
        }

    @cherrypy.tools.json_out()
    def PUT(self, id, title, desc):
        if self.updateProject(id=id, title=title, desc=desc):
            return self.view_o.createFeedbackMessage("Projekt erfolgreich bearbeitet.", 200)
        return self.view_o.createAlert("Projekt ID " + id + " ist nicht vorhanden.", 404)

    @cherrypy.tools.json_out()
    def DELETE(self, id):
        if self.deleteProject(id=id):
            return self.view_o.createFeedbackMessage("Projekt erfolgreich gelöscht.", 200)
        return self.view_o.createAlert("Projekt ID " + id + " ist nicht vorhanden.", 404)

    def createProject(self, title, desc):
        newId = self.db.getMaxId('project.json') + 1
        data = self.db.readFile('project.json')
        newEntry = {
            "id": newId,
            "title": title,
            "desc": desc,
            "component": []
        }

        data['data'].append(newEntry)

        self.db.writeFile('project.json', data)
        return newId

    def updateProject(self, id, title, desc):
        if not self.db.isNumber(id):
            return False

        if self.db.findId("project.json", id) is None:
            return False

        data = self.db.readFile('project.json')

        for entry in data['data']:
            if int(entry['id']) == int(id):
                entry['title'] = title
                entry['desc'] = desc
                break

        self.db.writeFile('project.json', data)
        return True

    def deleteProject(self, id):
        if not self.db.isNumber(id):
            return False

        if self.db.findId("project.json", id) is None:
            return False

        jsonFILE = self.db.readFile('project.json')
        data = []

        for entry in jsonFILE['data']:
            if not int(entry['id']) == int(id):
                data.append(entry)
            else:
                componentslist = entry['component']

        jsonFILE['data'] = data
        self.db.writeFile('project.json', jsonFILE)

        jsonFILE = self.db.readFile('component.json')
        components = []

        data_bugs = self.db.readFile('bug.json')

        for componentId in componentslist:
            bugs = []
            for entry in data_bugs['data']:
                if int(entry['component']) != int(componentId):
                    bugs.append(entry)
            data_bugs['data'] = bugs

        for entry in jsonFILE['data']:
            if int(id) != int(entry['project']):
                components.append(entry)
        jsonFILE['data'] = components

        self.db.writeFile('bug.json', data_bugs)
        self.db.writeFile('component.json', jsonFILE)
        return True

class ProjectComponent_cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()

    @cherrypy.tools.json_out()
    def GET(self, id):
        element = self.db.findId("project.json", id)
        if element is None:
            return self.view_o.createAlert("Projekt ID " + id + " ist nicht vorhanden.", 404)
        components = element['component']
        data = {'projects':self.db.readFile('project.json')['data']}
        list = []
        for entry in components:
            component = self.db.findId("component.json", entry)
            if not component is None:
                list.append(component)
        data['data'] = list
        return data
# EOF
