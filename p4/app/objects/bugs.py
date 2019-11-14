import os
import cherrypy
import datetime

from p3.app.database import Database_cl
from p3.app.view import View_cl

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


class Bugs_cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()
        self.filename_s = "bug.json"

    @cherrypy.tools.json_out()
    def GET(self, id=None, type=None):
        result = {
            'component': self.db.readFile('component.json')['data'],
            'project': self.db.readFile('project.json')['data'],
            'employee': self.db.readFile('employee.json')['data'],
            'bug_category': self.db.readFile('bug_category.json')['data'],
            'cause_category': self.db.readFile('cause_category.json')['data']
        }

        if type:
            if type == 'erfasst' or type == 'behoben':
                result['data'] = self.getByType(type)
                if type == 'erfasst':
                    result['show'] = 0
                if type == 'behoben':
                    result['show'] = 1

                return result
            else:
                return self.view_o.createAlert("Fehlertyp '" + type + "' ist ungültig.", 404)
        else:
            if id is None:
                result['data'] = self.getAll()
                return result

            if id == str('-1'):
                return result

            data = self.getOneById(id)
            result['bug'] = data
            if not data is None:
                return result
            return self.view_o.createAlert("Fehler mit dieser ID ist nicht Vorhanden.", 404)

    @cherrypy.tools.json_out()
    def POST(self, startdesc, qsemployee, component, bug_category, startdate, swemployee=None):
        return {
            "id": self.createBug(startdesc, qsemployee, component, bug_category, startdate, swemployee)
        }

    @cherrypy.tools.json_out()
    def PUT(self, id, startdesc=None, qsemployee=None, component=None, bug_category=None, startdate=None,
            swemployee=None, enddate=None, cause_category=None,
            causedesc=None, approval=None):

        if approval is not None:
            self.updateBugApproval(id,approval)
            if int(approval) is 1:
                return self.view_o.createFeedbackMessage("Fehler wurde freigegeben.", 200)
            else:
                return self.view_o.createFeedbackMessage("Fehler wurde in Zustand Erfasst versetzt.", 200)


        if cause_category is None:
            if self.updateBugQS(id, startdesc, qsemployee, component, bug_category, startdate, swemployee):
                return self.view_o.createFeedbackMessage("Fehler erfolgreich bearbeitet.", 200)
            return self.view_o.createAlert("Fehler ID " + id + " ist nicht vorhanden.", 404)
        else:
            if self.updateBugSW(id, swemployee, enddate, cause_category, causedesc):
                return self.view_o.createFeedbackMessage("Fehler erfolgreich bearbeitet.", 200)
            return self.view_o.createAlert("Fehler ID " + id + " ist nicht vorhanden.", 404)

    def getAll(self):
        return self.db.readFile(self.filename_s)['data']

    def getByType(self, type):
        data_all = self.getAll()
        data = []

        for entry in data_all:
            if entry['type'] == type:
                data.append(entry)

        return data

    def getOneById(self, id):
        return self.db.findId(self.filename_s, id)

    def createBug(self, startdesc, qsemployee, component, bug_category, startdate, swemployee=None):
        newId = self.db.getMaxId(self.filename_s) + 1
        data = self.db.readFile(self.filename_s)
        data_components = self.db.readFile('component.json')['data']
        data_bug_category = self.db.readFile('bug_category.json')['data']
        data_cause_category = self.db.readFile('cause_category.json')['data']

        # TODO: Validieren der Abhängigkeiten
        entry = {
            "id": newId,
            "startdesc": startdesc,
            "startdate": startdate,  # datetime.datetime.now().strftime('%Y.%m.%d'),
            "enddate": None,
            "qsemployee": int(qsemployee),
            # "swemployee": int(swemployee),
            "component": int(component),
            # "bug_category": bug_category, Muss Array sein!
            "cause_category": -1,
            'causedesc': None,
            "type": "erfasst"
        }

        if swemployee is not None:
            entry['swemployee'] = int(swemployee)
        else:
            entry['swemployee'] = -1
        try:
            entry['bug_category'] = [int(i) for i in bug_category]
        except:
            entry['bug_category'] = [int(bug_category)]

        data['data'].append(entry)
        self.db.writeFile(self.filename_s, data)
        return newId

    def updateBugApproval(self,id,approval):
        if not self.db.isNumber(id):
            return False

        if self.db.findId(self.filename_s, id) is None:
            return False

        data = self.db.readFile(self.filename_s)

        for entry in data['data']:
            if int(entry['id']) == int(id):
                if int(approval) is 1:
                    entry['type'] = "freigegeben"
                else:
                    entry['type'] = "erfasst"
                    entry['enddate'] = None
                    entry['causedesc'] = entry['causedesc'] + '\n -LÖSUNG ABGELEHNT-'
                break

        self.db.writeFile(self.filename_s, data)
        return True
    # QS
    def updateBugQS(self, id, startdesc, qsemployee, component, bug_category, startdate, swemployee):
        if not self.db.isNumber(id):
            return False

        if self.db.findId(self.filename_s, id) is None:
            return False

        data = self.db.readFile(self.filename_s)

        for entry in data['data']:
            if int(entry['id']) == int(id):
                entry['startdesc'] = startdesc
                entry['qsemployee'] = int(qsemployee)
                entry['component'] = int(component)
                # entry['bug_category'] = bug_category
                entry['startdate'] = startdate
                entry['swemployee'] = int(swemployee)
                try:
                    entry['bug_category'] = [int(i) for i in bug_category]
                except:
                    entry['bug_category'] = [int(bug_category)]

                entry['type'] = 'erfasst'
                entry['enddate'] = None
                break

        self.db.writeFile(self.filename_s, data)
        return True

    # SW
    def updateBugSW(self, id, swemployee, enddate, cause_category, causedesc):
        if not self.db.isNumber(id):
            return False

        if self.db.findId(self.filename_s, id) is None:
            return False

        data = self.db.readFile(self.filename_s)

        for entry in data['data']:
            if int(entry['id']) == int(id):
                entry['swemployee'] = int(swemployee)
                entry['enddate'] = enddate
                entry['cause_category'] = int(cause_category)
                entry['causedesc'] = causedesc
                entry['type'] = 'behoben'
                break

        self.db.writeFile(self.filename_s, data)
        return True
