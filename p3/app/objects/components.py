# coding: utf-8

# Demonstrator / keine Fehlerbehandlung

import cherrypy

from p3.app.database import Database_cl
from p3.app.view import View_cl

# Method-Dispatching!

# Übersicht Anforderungen / Methoden

"""
Anforderung              GET          PUT          POST          DELETE
-----------------------------------------------------------------------------
komponente/               Alle        -            Ein neue      -
                          Komponenten              Komponenten       
                          liefern                  anlegen       
-----------------------------------------------------------------------------
komponente/id             Eine        Eine         -             Eine
komponente/?id=id         Komponente  Komponente                 Komponente
                          liefern     updaten                    loeschen
"""


# ----------------------------------------------------------
class Component_Cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        if id is None:
            return {'data': self.db.readFile('component.json')['data'],
                    'projects': self.db.readFile('project.json')['data']};

        data = self.db.findId("component.json", id)
        if not data is None:
            data['projects'] = self.db.readFile('project.json')['data']
            return data
        return self.view_o.createAlert("Komponenten ID ist nicht vorhanden.")

    @cherrypy.tools.json_out()
    def POST(self, title, desc, projects):
        id = self.createComponent(title, desc, projects)
        if not id is None:
            return {
                "id": id
            }
        return self.view_o.createAlert("Nicht alle angebene Projekte sind vorhanden.", 400)

    @cherrypy.tools.json_out()
    def PUT(self, id, title, desc, projects):
        code = self.updateComponent(id=id, name=title, desc=desc, projectids=projects)
        if code == 0:
            return self.view_o.createFeedbackMessage("Komponente erfolgreich bearbeitet.", 200)
        elif code == 1:
            return self.view_o.createAlert("Komponenten ID ist nicht vorhanden.", 404)
        else:
            return self.view_o.createAlert("Nicht alle angebene Projekte sind vorhanden.", 400)

    @cherrypy.tools.json_out()
    def DELETE(self, id):
        if self.deleteComponent(id=id):
            return self.view_o.createFeedbackMessage("Komponente erflogreich gelöscht.", 200)
        return self.view_o.createAlert("Komponenten ID ist nicht vorhanden.", 404)

    def createComponent(self, name, desc, projectids):
        newId = self.db.getMaxId('component.json') + 1
        data = self.db.readFile('component.json')

        newEntry = {
            "id": newId,
            "name": name,
            "desc": desc,
            "project": int(projectids)
        }

        data['data'].append(newEntry)

        success = True
        # Add the component to the project component array
        data_projects = self.db.readFile('project.json')

        exists = False
        for entry in data_projects['data']:
            if int(projectids) == int(entry['id']):
                entry['component'].append(int(newId))
                exists = True
                break
        if not exists:
            success = False

        if not success:
            return None

        self.db.writeFile('project.json', data_projects)
        self.db.writeFile('component.json', data)
        return newId

    def updateComponent(self, id, name, desc, projectids):
        if not self.db.isNumber(id):
            return 1

        if self.db.findId("component.json", id) is None:
            return 1

        data = self.db.readFile('component.json')
        # Test if project ids is an int value or an array

        projects = projectids

        for entry in data['data']:
            if int(entry['id']) == int(id):
                entry['name'] = name
                entry['desc'] = desc
                oldProject = entry['project']
                entry['project'] = projects
                break

        # Delete the component from all projects
        data_projects = self.db.readFile('project.json')
        for entry in data_projects['data']:
            if int(oldProject) == int(entry['id']):
                try:
                    entry['component'].remove(int(id))
                except:
                    print('Components update error found.')
                break

        success = True
        for projectId in projects:
            exists = False
            for entry in data_projects['data']:
                if int(projectId) == int(entry['id']):
                    entry['component'].append(int(id))
                    exists = True
                    break
            if not exists:
                success = False
                break

        if not success:
            return 2

        self.db.writeFile('project.json', data_projects)
        self.db.writeFile('component.json', data)
        return 0

    def deleteComponent(self, id):
        if not self.db.isNumber(id):
            return False

        if self.db.findId("component.json", id) is None:
            return False

        # Get the current file
        data = self.db.readFile('component.json')
        data_bugs = self.db.readFile('bug.json')

        # Remove the component from the components array
        components = []
        for entry in data['data']:
            if not entry['id'] == int(id):
                components.append(entry)
            else:
                projects = entry['project']
        data['data'] = components

        bugs = []
        for entry in data_bugs['data']:
            if entry['component'] != int(id):
                bugs.append(entry)
        data_bugs['data'] = bugs

        # Remove the component id from the projects
        data_projects = self.db.readFile('project.json')
        for projectEntry in data_projects['data']:
            for value in projects:
                if projectEntry['id'] == int(value):
                    projectEntry['component'].remove(int(id))

        self.db.writeFile('bug.json', data_bugs)
        self.db.writeFile('project.json', data_projects)
        self.db.writeFile('component.json', data)
        return True
# EOF
