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


class Events_cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()
        self.filename_s = "event.json"

    @cherrypy.tools.json_out()
    def GET(self, id=None, desc=None, x=7, y=7, halltype=0, savehallplan=False):
        result = {}

        if id and id != '-2':
            result['plan'] = self.db.findEntryWithFieldId('hallplan.json', 'eventid', id)
            if result['plan'] is None:
                result['layouts'] = self.createHallLayouts(id, int(x), int(y), int(halltype), savehallplan)
            if savehallplan:
                result['plan'] = self.db.findEntryWithFieldId('hallplan.json', 'eventid', id)
            result['organizer'] = self.db.readFile('organizer.json')['data']
            result['bookings'] = self.db.findAllEntriesWithFieldId('booking.json', 'eventid', id)
            result['exhibitors'] = self.db.findAllIdsByList('exhibitor.json',
                                                            self.db.getAllForeignIdsFromData(result['bookings'],
                                                                                             'exhibitorid'))
            result['all_exhibitors'] = self.db.readFile('exhibitor.json')['data']
            result['bookingtypes'] = self.db.readFile('bookingtype.json')
        else:
            result['plan'] = self.db.readFile('hallplan.json')['data']
            result['organizer'] = self.db.readFile('organizer.json')['data']
            result['event'] = {
                "id": -2,
                "name": '',
                "startdate": '',  # datetime.datetime.now().strftime('%Y.%m.%d'),
                "enddate": '',
                "desc": '',
                "organizerid": ''
            }
            if id == '-2':
                return result

        if id is None:
            result['data'] = self.getAll()
            return result

        if id == str('-1'):
            return result

        data = self.getOneById(id)
        result['event'] = data
        if data:
            return result
        return self.view_o.createAlert("Messe mit dieser ID ist nicht vorhanden.", 404)

    @cherrypy.tools.json_out()
    def POST(self, name, desc, startdate, enddate, organizerid):
        return {
            "id": self.createEvent(name, desc, startdate, enddate, organizerid)
        }

    @cherrypy.tools.json_out()
    def PUT(self, id, name, desc, startdate, enddate, organizerid):
        if self.updateEvent(id, name, desc, startdate, enddate, organizerid):
            return self.view_o.createFeedbackMessage("Messe erfolgreich bearbeitet.", 200)
        return self.view_o.createAlert("Messe ID " + id + " ist nicht vorhanden.", 404)

    def getAll(self):
        return self.db.readFile(self.filename_s)['data']

    def getOneById(self, id):
        return self.db.findId(self.filename_s, id)

    def createEvent(self, name, desc, startdate, enddate, organizerid):
        newId = self.db.getMaxId(self.filename_s) + 1
        data = self.db.readFile(self.filename_s)

        entry = {
            "id": newId,
            "name": name,
            "startdate": startdate,  # datetime.datetime.now().strftime('%Y.%m.%d'),
            "enddate": enddate,
            "desc": desc,
            "organizerid": int(organizerid)
        }

        data['data'].append(entry)
        self.db.writeFile(self.filename_s, data)

        return newId

    def updateEvent(self, id, name, desc, startdate, enddate, organizerid):
        if not self.db.isNumber(id):
            return False

        if self.db.findId(self.filename_s, id) is None:
            return False

        data = self.db.readFile(self.filename_s)

        for entry in data['data']:
            if int(entry['id']) == int(id):
                entry['name'] = name
                entry['desc'] = desc
                if startdate != None:
                    entry['startdate'] = startdate
                if enddate != None:
                    entry['enddate'] = enddate
                entry['organizerid'] = organizerid
                break

        self.db.writeFile(self.filename_s, data)
        return True

    def createHallLayouts(self, id, x, y, halltype, safehallplan):
        layouts = []

        newBookingId = self.db.getMaxId('booking.json') + 1
        newHallplanId = self.db.getMaxId('hallplan.json') + 1
        bookings = []

        if halltype == 0:
            for i in range(x):
                for j in range(y):
                    if i == 1 or i == x - 2 or j == 1 or j == y - 2:
                        bookings.append({
                            "id": int(++newBookingId),
                            "desc": "Veranstalter",
                            "hallplanid": int(newHallplanId),
                            "eventid": int(id),
                            "exhibitorid": -1,
                            'x': i,
                            'y': j,
                            'bookingtype': 0
                        })
        elif halltype == 1:
            for i in range(x):
                for j in range(y):
                    if i == int(x / 2) or j == int(y / 2):
                        bookings.append({
                            "id": int(++newBookingId),
                            "desc": "Veranstalter",
                            "hallplanid": int(newHallplanId),
                            "eventid": int(id),
                            "exhibitorid": -1,
                            'x': i,
                            'y': j,
                            'bookingtype': 0
                        })
        elif halltype == 2:
            for i in range(x):
                for j in range(y):
                    if i == 0 or j == 0 or i == int(x / 2) or j == int(y / 2) or i == x - 1 or j == y - 1:
                        bookings.append({
                            "id": int(++newBookingId),
                            "desc": "Veranstalter",
                            "hallplanid": int(newHallplanId),
                            "eventid": int(id),
                            "exhibitorid": -1,
                            'x': i,
                            'y': j,
                            'bookingtype': 0
                        })
        elif halltype == 3:
            for i in range(x):
                for j in range(y):
                    if i == 1 or i == x - 2 or j % 3 == 0:
                        bookings.append({
                            "id": int(++newBookingId),
                            "desc": "Veranstalter",
                            "hallplanid": int(newHallplanId),
                            "eventid": int(id),
                            "exhibitorid": -1,
                            'x': i,
                            'y': j,
                            'bookingtype': 0
                        })

        layouts.append({
            "w": x,
            "h": y,
            "layout": halltype,
            "capacity": x * y,
        })

        layouts[0]['bookings'] = bookings

        if safehallplan:
            data = self.db.readFile('hallplan.json')
            entry = {
                "id": int(newHallplanId),
                "eventid": int(id),
                "w": x,
                "h": y,
                "capacity": x * y,
            }

            data['data'].append(entry)
            self.db.writeFile('hallplan.json', data)
            data = self.db.readFile('booking.json')
            data['data'] = data['data'] + bookings
            self.db.writeFile('booking.json', data)

        return layouts
