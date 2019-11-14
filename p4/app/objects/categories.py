import os
import cherrypy

from p3.app.database import Database_cl
from p3.app.view import View_cl

"""

Anforderung             GET                 PUT               POST              DELETE
----------------------------------------------------------------
katfehler/              Alle                -                 Ein neue          -
                        Fehlerkategorien                      Fehlerkategorie       
                        liefern                               anlegen       
--------------------------------------------------------------------------------------------------
katfehler/id            Ein                 Ein               -                 Ein
katfehler/?id=id        Fehlerkategorie     Fehlerkategorien                    Lösungskategorien
                        liefern             updaten                             loeschen
---------------------------------------------------------------------------------------------------
katursache/             Alle                -                 Ein neue           -
                        Lösungskategorien                     Lösungskategorien       
                        liefern                               anlegen       
---------------------------------------------------------------------------------------------------
katursache/id           Ein                 Ein               -                  Ein
katursache/?id=id       Lösungskategorien   Lösungskategorien                    Lösungskategorien
                        liefern             updaten                              loeschen
"""


@cherrypy.tools.json_out()
class Category_cl(object):
    exposed = True

    def __init__(self, path, filename):
        self.db = Database_cl(path)
        self.view_o = View_cl()
        self.filename_s = filename

    def GET(self, id=None):
        return {'bug': self.db.readFile('bug_category.json')['data'],
                'cause': self.db.readFile('cause_category.json')['data']}

    def getAll(self):
        return self.db.readFile(self.filename_s)['data']

    def getOneById(self, id):
        return self.db.findId(self.filename_s, id)

    def createCategory(self, title):
        newId = self.db.getMaxId(self.filename_s) + 1
        data = self.db.readFile(self.filename_s)

        entry = {
            "id": newId,
            "title": title
        }

        data['data'].append(entry)
        self.db.writeFile(self.filename_s, data)
        return newId

    def updateCategory(self, id, title):
        if not self.db.isNumber(id):
            return False

        if self.db.findId(self.filename_s, id) is None:
            return False

        data = self.db.readFile(self.filename_s)

        for entry in data['data']:
            if entry['id'] == int(id):
                entry['title'] = title
                break

        self.db.writeFile(self.filename_s, data)
        return True

    # type 0 - bug_cat / type 1 - cause_cat
    def deleteCategory(self, id, filename_s, type):
        if not self.db.isNumber(id):
            return False

        if self.db.findId(filename_s, id) is None:
            return False

        jsonFILE = self.db.readFile(filename_s)
        data_bugs = self.db.readFile('bug.json')
        categories = []
        bugs = []

        if type == 0:
            for entry in data_bugs['data']:
                if not int(id) in entry['bug_category']:
                    bugs.append(entry)
                elif len(entry['bug_category']) > 1:
                    entry['bug_category'].remove(int(id))
                    bugs.append(entry)
        elif type == 1:
            for entry in data_bugs['data']:
                if entry['cause_category'] == (int(id)):
                    entry['cause_category'] = -1
                bugs.append(entry)


        for entry in jsonFILE['data']:
            if not int(entry['id']) == int(id):
                categories.append(entry)

        jsonFILE['data'] = categories
        data_bugs['data'] = bugs

        self.db.writeFile('bug.json', data_bugs)
        self.db.writeFile(filename_s, jsonFILE)
        return True


class BugCategory_cl(Category_cl):
    exposed = True

    def __init__(self, path):
        Category_cl.__init__(self, path, "bug_category.json")

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        if id is None:
            return self.getAll()

        data = self.getOneById(id)
        if not data is None:
            return data
        return self.view_o.createAlert("Fehler-Kategorie mit dieser ID ist nicht Vorhanden.", 404)

    @cherrypy.tools.json_out()
    def POST(self, title):
        return {
            "id": self.createCategory(title)
        }

    @cherrypy.tools.json_out()
    def PUT(self, id, title):
        if self.updateCategory(id, title):
            return self.view_o.createFeedbackMessage("Fehler-Kategorie erfolgreich bearbeitet.", 200)
        return self.view_o.createAlert("Fehler-Kategorie ID " + id + " ist nicht vorhanden.", 404)

    @cherrypy.tools.json_out()
    def DELETE(self, id):
        if self.deleteCategory(id, self.filename_s,0):
            return self.view_o.createFeedbackMessage("Fehler-Kategorie erfolgreich gelöscht.", 200)
        return self.view_o.createAlert("Fehler-Kategorie ID " + id + " ist nicht vorhanden.", 404)


class CauseCategory_cl(Category_cl):
    exposed = True

    def __init__(self, path):
        Category_cl.__init__(self, path, "cause_category.json")

    @cherrypy.tools.json_out()
    def GET(self, id=None):
        if id is None:
            return self.getAll()

        data = self.getOneById(id)
        if not data is None:
            return data
        return self.view_o.createAlert("Ursachen-Kategorie mit dieser ID ist nicht Vorhanden.", 404)

    @cherrypy.tools.json_out()
    def POST(self, title):
        return {
            "id": self.createCategory(title)
        }

    @cherrypy.tools.json_out()
    def PUT(self, id, title):
        if self.updateCategory(id, title):
            return self.view_o.createFeedbackMessage("Ursachen-Kategorie erfolgreich bearbeitet.", 200)
        return self.view_o.createAlert("Ursachen-Kategorie ID " + id + " ist nicht vorhanden.", 404)

    @cherrypy.tools.json_out()
    def DELETE(self, id):
        if self.deleteCategory(id, self.filename_s,1):
            return self.view_o.createFeedbackMessage("Ursachen-Kategorie erfolgreich gelöscht.", 200)
        return self.view_o.createAlert("Ursachen-Kategorie ID " + id + " ist nicht vorhanden.", 404)
