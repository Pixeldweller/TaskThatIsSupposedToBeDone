import os
import cherrypy
import datetime

from p4.app.database import Database_cl
from p4.app.view import View_cl

"""

Anforderung             GET                PUT                POST             DELETE
----------------------------------------------------------------
fehler/                 Alle               -                  Ein neuen        -
                        Fehler                                Fehler       
                        liefern                               anlegen       
--------------------------------------------------------------------------------------------------
fehler/id               Ein                Ein                -                -
fehler/?id=id           Fehler             Fehler      
                        liefern            updaten     
--------------------------------------------------------------------------------------------------
fehler/type             Alle Fehler        -                  -                -
fehler/?type=type       eines Types
                        liefern
--------------------------------------------------------------------------------------------------
"""


class Organizer_cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()
        self.filename_s = "organizer.json"

    @cherrypy.tools.json_out()
    def GET(self, id=None, loadEvents=False):
        result = {}
        if loadEvents:
            result['events'] = self.db.findAllEntriesWithFieldId('event.json', 'organizerid', id)
        else:
            result['events'] = self.db.readFile('event.json')['data']

        if id is None:
            result['organizer'] = self.getAll()
            return result

        if int(id) == -2:
            result['organizer'] = {
                "id": -1,
                "name": '',
                "desc": ''
            }
            return result

        data = self.getOneById(id)
        result['organizer'] = data
        if data:
            return result
        return self.view_o.createAlert("Veranstalter mit dieser ID ist nicht vorhanden.", 404)

    @cherrypy.tools.json_out()
    def POST(self, name, desc):
        return {
            "id": self.createOrganizer(name, desc)
        }

    @cherrypy.tools.json_out()
    def PUT(self, id,name, desc):
        if self.updateOrganizer(id,name,desc):
            return self.view_o.createFeedbackMessage("Veranstalter erfolgreich bearbeitet.", 200)
        return self.view_o.createAlert("Veranstalter ID " + id + " ist nicht vorhanden.", 404)

    def getAll(self):
        return self.db.readFile(self.filename_s)['data']

    def getOneById(self, id):
        return self.db.findId(self.filename_s, id)

    def createOrganizer(self, name, desc):
        newId = self.db.getMaxId(self.filename_s) + 1
        data = self.db.readFile(self.filename_s)

        entry = {
            "id": newId,
            "name": name,
            "desc": desc
        }

        data['data'].append(entry)
        self.db.writeFile(self.filename_s, data)

        return newId

    def updateOrganizer(self,id, name,desc):
        if not self.db.isNumber(id):
            return False

        if self.db.findId(self.filename_s, id) is None:
            return False

        data = self.db.readFile(self.filename_s)

        for entry in data['data']:
            if int(entry['id']) == int(id):
                entry['name'] = name
                entry['desc'] = desc
                break

        self.db.writeFile(self.filename_s, data)
        return True
