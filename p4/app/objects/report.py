# coding: utf-8

# Demonstrator / keine Fehlerbehandlung

import cherrypy
import datetime
import time

from p3.app.database import Database_cl
from p3.app.view import View_cl

# Method-Dispatching!

# Übersicht Anforderungen / Methoden

"""
Anforderung              GET         
-----------------------------------------
prolist/            Auswertung Fehler 
                    nach Projekt/Komponente/Status 
                    als Liste anfordern                         
-----------------------------------------------------------------------------
katlist/          Auswertung Fehler nach
                    Kategorie/Status als Liste
                    anfordern  
"""


# ----------------------------------------------------------
class Prolist_cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()

    @cherrypy.tools.json_out()
    def GET(self):
        data = {'projects': self.db.readFile('project.json')['data'],
                'components': self.db.readFile('component.json')['data'],
                'bugs': self.db.readFile('bug.json')['data']}
        reportData = []
        reportList = []
        for p in data['projects']:
            components = []
            for c in data['components']:
                if int(c['project']) == int(p['id']):
                    bugs = []
                    for b in data['bugs']:
                        if int(b['component']) == int(c['id']):
                            reportList.append({'project': p['title'], 'component': c['name'], 'bug': b['startdesc'],
                                               'status': b['type']})
                            bugs.append({'desc': b['startdesc'], 'type': b['type'],'startdate':b['startdate'],'enddate':b['enddate'], 'diff': self.days_between(b['startdate'],b['enddate'])})
                    components.append({'name': c['name'], 'childs': bugs})
            reportData.append({'title': p['title'], 'childs': components})
        report = {'data': reportData}

        return report

    def days_between(self,d1, d2):
        if d2 is None:
            return '-'
        d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
        return str(abs((d2 - d1).days))+' Tage'

class Katlist_cl(object):
    exposed = True

    def __init__(self, path):
        self.db = Database_cl(path)
        self.view_o = View_cl()

    @cherrypy.tools.json_out()
    def GET(self):
        data = {'bug_category': self.db.readFile('bug_category.json')['data'],
                'bugs': self.db.readFile('bug.json')['data']}
        reportData = []
        reportList = []
        for c in data['bug_category']:
            bugs = []
            for b in data['bugs']:
                if (int(c['id']) in b['bug_category']):
                    reportList.append({'category': c['title'], 'bug': b['startdesc'], 'status': b['type']})
                    bugs.append({'desc': b['startdesc'], 'type': b['type'],'startdate':b['startdate'],'enddate':b['enddate'], 'diff': self.days_between(b['startdate'],b['enddate'])})
            reportData.append({'category': c['title'], 'childs':bugs})
        report = {'data': reportData}
        return report

    def days_between(self,d1, d2):
        if d2 is None:
            return '-'
        d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
        return str(abs((d2 - d1).days))+' Tage'
# EOF
