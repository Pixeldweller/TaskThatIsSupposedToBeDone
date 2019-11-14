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


class Exhibitors_cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()
        self.filename_s = "exhibitor.json"

    @cherrypy.tools.json_out()
    def GET(self, id=None, loadEvents=True):
        result = {}


        if id is None and id != -2:
            result['data'] = self.getAll()
        else:
            data = self.getOneById(id)

        if id == str('-2'):
            result['exhibitor'] = {
                "id": -2,
                "name": '',
                "desc": ''
            }
            return result

        if loadEvents:
            if id:
                result['bookings'] = self.db.findAllEntriesWithFieldId('booking.json', 'exhibitorid', id)
                eventids = []
                for e in result['bookings']:
                    eventids.append(e['eventid'])
                result['events'] = self.db.findAllIdsByList('event.json', eventids)

            else:
                result['bookings'] = self.db.readFile('booking.json')['data']
                result['events'] = self.db.findAllIdsByList('event.json', self.db.getAllIdsFromData(result['data']))
                return result

        result['exhibitor'] = data
        if data:
            return result
        return self.view_o.createAlert("Aussteller mit dieser ID ist nicht vorhanden.", 404)

    @cherrypy.tools.json_out()
    def POST(self, name, desc):
        return {
            "id": self.createOrganizer(name, desc)
        }

    @cherrypy.tools.json_out()
    def PUT(self, id,name, desc):
        if self.updateOrganizer(id,name,desc):
            return self.view_o.createFeedbackMessage("Aussteller erfolgreich bearbeitet.", 200)
        return self.view_o.createAlert("Aussteller ID " + id + " ist nicht vorhanden.", 404)

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
