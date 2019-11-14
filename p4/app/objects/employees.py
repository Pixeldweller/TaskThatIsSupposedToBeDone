import os
import cherrypy

from p3.app.database import Database_cl
from p3.app.view import View_cl

"""

Anforderung       GET          PUT          POST          DELETE
----------------------------------------------------------------
swentwickler/     Alle         -           Ein neuen       -
                  SW-Ent                   SW-Ent       
                  liefern                  anlegen       

----------------------------------------------------------------
swentwickler/id   Ein         Ein            -           Ein
swentwickler/?id  SW-Ent      SW-Ent                     SW-Ent 
                  liefern     updaten                    loeschen

----------------------------------------------------------------
qsmitarbeiter/    Alle         -           Ein neuen       -
                  QS-Mit                   QS-Mit       
                  liefern                  anlegen       

----------------------------------------------------------------
qsmitarbeiter/id  Ein         Ein            -           Ein
qsmitarbeiter/?id QS-Mit      QS-Mit                     QS-Mit
                  liefern     updaten                    loeschen
"""


@cherrypy.tools.json_out()
class Employee_cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()

    def GET(self, id=None):
        if id is not None:
            return self.db.findId("employee.json", id)

        return self.db.readFile('employee.json')

    def DELETE(self, id):
        if self.deleteEmployee(id):
            return self.view_o.createFeedbackMessage("Mitarbeiter erfolgreich gelöscht.", 200)
        return self.view_o.createAlert("Mitarbeiter ID " + id + " ist nicht vorhanden.", 404)

    def createEmployee(self, roleid, username, firstname, lastname, email):
        newId = self.db.getMaxId('employee.json') + 1
        data = self.db.readFile('employee.json')

        entry = {
            "id": newId,
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "email": email,
            "roleId": int(roleid),
        }

        data['data'].append(entry)
        self.db.writeFile('employee.json', data)
        return newId

    def updateEmployee(self, id, roleid, username, firstname, lastname, email):
        if not self.db.isNumber(id):
            return False

        if self.db.findId("employee.json", id) is None:
            return False

        data = self.db.readFile('employee.json')

        exists = False
        for role in data['roles']:
            if role['id'] == int(roleid):
                exists = True
                break

        if not exists:
            return False

        # find the searched employee and update the inforamtion
        for entry in data['data']:
            if entry['id'] == int(id):
                entry['roleId'] = int(roleid)
                entry['username'] = username
                entry['firstname'] = firstname
                entry['lastname'] = lastname
                entry['email'] = email
                break

        # save the new data to file
        self.db.writeFile('employee.json', data)
        return True

    def deleteEmployee(self, id):
        if not self.db.isNumber(id):
            return False

        if self.db.findId("employee.json", id) is None:
            return False

        jsonFILE = self.db.readFile('employee.json')
        employee = []
        data_bugs = self.db.readFile('bug.json')
        bugs = []

        for entry in data_bugs['data']:
            if int(entry['qsemployee']) != int(id):
                if int(entry['swemployee']) == int(id):
                    entry['swemployee'] = -1
                bugs.append(entry)

        data_bugs['data'] = bugs

        for entry in jsonFILE['data']:
            if not int(entry['id']) == int(id):
                employee.append(entry)

        jsonFILE['data'] = employee

        self.db.writeFile('bug.json', data_bugs)
        self.db.writeFile('employee.json', jsonFILE)
        return True


class SoftwareDeveloper_Cl(Employee_cl):
    exposed = True

    def __init__(self, path):
        Employee_cl.__init__(self, path)

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        if id is None:
            return self.getAllSoftwareDeveloper()

        data = self.getSoftwareDeveloperById(id)
        if not data is None:
            return data
        return self.view_o.createAlert("Software-Entwickler mit dieser ID ist nicht Vorhanden.")

    @cherrypy.tools.json_out()
    def POST(self, username, firstname, lastname, email):
        return {
            "id": self.createSoftwareDeveloper(username, firstname, lastname, email)
        }

    @cherrypy.tools.json_out()
    def PUT(self, id, roleid, username, firstname, lastname, email):
        if self.updateEmployee(id, roleid, username, firstname, lastname, email):
            return self.view_o.createFeedbackMessage("Software Entwickler erfolgreich bearbeitet.", 200)
        return self.view_o.createAlert("Software Entwickler ID " + id + " ist nicht vorhanden.", 404)

    @cherrypy.tools.json_out()
    def DELETE(self, id):
        if self.deleteEmployee(id):
            return self.view_o.createFeedbackMessage("Software Entwickler erfolgreich gelöscht.", 200)
        return self.view_o.createAlert("Software Entwickler ID " + id + " ist nicht vorhanden.", 404)

    def getAllSoftwareDeveloper(self):
        data = self.db.readFile('employee.json')
        softwareDeveloper = {
            'data':[],
            'roles': data['roles'],
            'show': 0
        }

        for entry in data['data']:
            if int(entry['roleId']) == 0:
                softwareDeveloper['data'].append(entry)

        return softwareDeveloper

    def getSoftwareDeveloperById(self, id):
        if not self.db.isNumber(id):
            return None

        data = self.db.findId("employee.json", id)

        if data is None:
            return None

        if int(data['roleId']) == 0:
            return data
        return None

    def createSoftwareDeveloper(self, username, fistname, lastname, email):
        return self.createEmployee(0, username, fistname, lastname, email)


# ------------------------------------------------
class QualityManagement_Cl(Employee_cl):
    exposed = True

    def __init__(self, path):
        Employee_cl.__init__(self, path)

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        if id is None:
            return self.getAllQualityManagement()

        data = self.getQualityManagementById(id)
        if not data is None:
            return data

        return self.view_o.createAlert("QS-Mitarbeiter mit dieser ID ist nicht vorhanden.")

    # Create a new quality employee and return the id as json
    @cherrypy.tools.json_out()
    def POST(self, username, firstname, lastname, email):
        return {
            "id": self.createQualityManagement(username, firstname, lastname, email)
        }

    @cherrypy.tools.json_out()
    def PUT(self, id, roleid, username, firstname, lastname, email):
        if self.updateEmployee(id, roleid, username, firstname, lastname, email):
            return self.view_o.createFeedbackMessage("QS-Mitarbeiter erfolgreich bearbeitet.", 200)
        return self.view_o.createAlert("QS-Mitarbeiter ID " + id + " ist nicht vorhanden.", 404)

    @cherrypy.tools.json_out()
    def DELETE(self, id):
        if self.deleteEmployee(id):
            return self.view_o.createFeedbackMessage("QS-Mitarbeiter erfolgreich gelöscht.", 200)
        return self.view_o.createAlert("QS-Mitarbeiter ID " + id + " ist nicht vorhanden.", 404)

    # -------------------- QualityManagement Functions

    def getAllQualityManagement(self):
        data = self.db.readFile('employee.json')
        qs = {
            'data':[],
            'roles': data['roles'],
            'show':1
        }
        for entry in data['data']:
            if int(entry['roleId']) == 1:
                qs['data'].append(entry)

        return qs

    def getQualityManagementById(self, id):
        if not self.db.isNumber(id):
            return None

        data = self.db.findId("employee.json", id)

        if data is None:
            return None

        if int(data['roleId']) == 1:
            return data
        return None

    def createQualityManagement(self, username, firstname, lastname, email):
        return self.createEmployee(1, username, firstname, lastname, email)
