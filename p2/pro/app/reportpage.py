import cherrypy
import html

from .startpage import StartPage

class ReportPage(StartPage):

    def __init__(self, view, db):
        self.db = db
        self.view = view
        self.pageCount = 0

    def default_view(self, feedbackmessage = ''):
        pro_dict = self.db.readFile('project.json')
        pro_dict['possible_employees'] = sorted(self.db.get_employees(), key=lambda k: k['lastname'])
        pro_dict['possible_customers'] = sorted(self.db.get_customers(), key=lambda k: k['name'])
        pro_dict['msg'] = feedbackmessage

        for entry in pro_dict['data']:
            for empl in entry['employee']:
                for possible_empl in pro_dict['possible_employees']:
                    if empl['employee_id'] == possible_empl['id']:
                        empl['lastname'] = possible_empl['lastname']
                        empl['firstname'] = possible_empl['firstname']
            entry['employee'] = sorted(entry['employee'], key=lambda x: x['lastname'])
            #entry['employee'] = sorted(entry['employee'], key=lambda x: x['firstname'])

        pro_dict['data'] = sorted(pro_dict['data'], key=lambda x:x['title'])

        return self.view.renderTemplateWithDictionary("projects/p_report.mako", data_op=pro_dict)

