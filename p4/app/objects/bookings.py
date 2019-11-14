import os
import cherrypy
import datetime

from p4.app.database import Database_cl
from p4.app.view import View_cl


class Bookings_cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()
        self.filename_s = "booking.json"
        self.helpfilename_s = "booking.json"

    @cherrypy.tools.json_out()
    def GET(self, eventid=None, id=None):
        result = {}
        if eventid and id is None:
            result['bookings'] = self.db.findAllEntriesWithFieldId(self.filename_s, 'eventid', eventid)
            result['exhibitors'] = []
            for entry in result['bookings']:
                result['exhibitors'].append(self.db.findId('exhibitor.json', int(entry['exhibitorid'])))
            return result
        if eventid == str('-1') and id:
            data = self.getOneById(id)
            result['bookings'] = data
            result['exhibitors'] = self.db.findId('exhibitor.json', data['exhibitorid'])
            return result

        result['bookings'] = self.getAll()
        result['events'] = self.db.readFile('event.json')['data']
        result['exhibitors'] = self.db.readFile('exhibitor.json')['data']
        return result

    @cherrypy.tools.json_out()
    def POST(self, hallplanid, eventid, exhibitorid, x, y, desc, bookingtype):
        id =  self.createBooking(int(hallplanid), int(eventid), int(exhibitorid), int(x), int(y), desc,
                           int(bookingtype))

        if not isinstance(id, int):
            return id

        return {
            "id": id
        }

    @cherrypy.tools.json_out()
    def PUT(self, id, exhibitorid, x, y, desc, bookingtype):
        if self.updateBooking(id, exhibitorid, x, y, desc, bookingtype):
            return self.view_o.createFeedbackMessage("Buchung erfolgreich bearbeitet.", 200)
        return self.view_o.createAlert("Buchung ID " + id + " ist nicht vorhanden.", 404)

    def getAll(self):
        data = self.db.readFile(self.filename_s)['data']
        filtered = []
        for entry in data:
            if entry['desc'] != 'Veranstalter':
                filtered.append(entry)
        return filtered

    def getOneById(self, id):
        return self.db.findId(self.filename_s, id)

    def createBooking(self, hallplanid, eventid, exhibitorid, x, y, desc, bookingtype):
        newId = self.db.getMaxId(self.filename_s) + 1
        data = self.db.readFile(self.filename_s)

        doublette = None

        for index in data['data']:
            if index['eventid'] == eventid and index['x'] == x and index['y'] == y:
                doublette = index

        if doublette is not None:
            if exhibitorid != -1 and doublette['bookingtype'] != -1:
                return self.view_o.createAlert("Position ist bereits ausgebucht, bitte wählen Sie eine andere Position.", 404)
            else:
                data['data'].remove(doublette)

        entry = {
            "id": newId,
            "hallplanid": int(hallplanid),
            "eventid": int(eventid),
            "exhibitorid": int(exhibitorid),
            "x": int(x),
            "y": int(y),
            "desc": desc,
            "bookingtype": int(bookingtype)
        }

        data['data'].append(entry)
        self.db.writeFile(self.filename_s, data)

        return newId

    def updateBooking(self, id, exhibitorid, x, y, desc, bookingtype):
        if not self.db.isNumber(id):
            return False

        if self.db.findId(self.filename_s, id) is None:
            return False

        data = self.db.readFile(self.filename_s)

        for entry in data['data']:
            if int(entry['id']) == int(id):
                entry['exhibitorid'] = exhibitorid
                entry['x'] = x
                entry['y'] = y
                entry['desc'] = desc
                entry['bookingtype'] = bookingtype
                break

        self.db.writeFile(self.filename_s, data)
        return True
