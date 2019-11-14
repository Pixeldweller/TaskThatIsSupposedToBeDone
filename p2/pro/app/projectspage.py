import cherrypy

from .startpage import StartPage

class ProjectsPage(StartPage):

    def __init__(self, view,db):
        StartPage.__init__(self,view,db)

    @cherrypy.expose
    def table_view(self, changeMode = False):
        cherrypy.session['p_table_view_active'] = changeMode
        return self.default_view()

    def default_view(self, feedbackmessage = ''):
        pro_dict = self.get_projects()
        pro_dict['possible_employees'] = sorted(self.db.get_employees(),key=lambda k: k['lastname'])
        pro_dict['possible_customers'] = sorted(self.db.get_customers(),key= lambda k: k['name'])
        pro_dict['msg'] = feedbackmessage

        for entry in pro_dict['data']:
            for empl in entry['employee']:
                for possible_empl in pro_dict['possible_employees']:
                    if empl['employee_id'] == possible_empl['id']:
                        empl['name'] = possible_empl['firstname']+' '+possible_empl['lastname']
            entry['employee'] = sorted(entry['employee'], key=lambda x: x['name'])

        show_table_view = cherrypy.session.get('p_table_view_active')
        if show_table_view:
            return self.view.renderTemplateWithDictionary("projects/p_table.mako", data_op=pro_dict)
        else:
            return self.view.renderTemplateWithDictionary("projects/p_table_display.mako", data_op=pro_dict)

    @cherrypy.expose
    def add(self, id, number,title,desc,startdate, duration,budget,customer,**args):
        data = self.find_project_by_id(id)
        id = self.escape(id)
        number = self.escape(number)
        title = self.escape(title)
        desc = self.escape(desc)
        startdate = self.escape(startdate)
        duration = self.escape(duration)
        budget = self.escape(budget)
        customer = self.escape(customer)
        # **arg escape?
        try:
            if data is not None:
                updated = self.update_project(id, number, title, desc, startdate, duration, budget, args, customer)
                return self.default_view('''Update Erfolgreich.''')
            else:
                added = self.add_project(number, title, desc, startdate, duration, budget, args, customer)
                return self.default_view('''Hinzufügem Erfolgreich.''')
        except Exception as e:
            return self.re_edit(str(e),id,number,title,desc,startdate, duration,budget,customer, **args)

    @cherrypy.expose
    def edit(self, p_id, reloaded=False, num=-1, title='-Neuer Titel-', desc='-Neue Beschreibung-', startdate='',
             duration=1, budget=0.0, customer=0):
        data = self.find_project_by_id(p_id)
        if num is -1:
            num = int(p_id)
        if data is not None:
            data['possible_employees'] = self.db.get_employees()
            data['possible_customers'] = self.db.get_customers()
            if reloaded:
                data['num'] = num
                data['title'] = title
                data['desc'] = desc
                data['startdate'] = startdate
                data['duration'] = duration
                data['budget'] = budget
                data['customer'] = customer
            return self.view.renderTemplateWithDictionary("projects/p_edit.mako", data_op=data)
        else:
            data = {
                "id": self.db.getMaxId("project.json") + 1,
                "number": int(num),
                "title": title,
                'desc': desc,
                'startdate': startdate,
                'duration': duration,
                'budget': budget,
                'employee': [],
                'customer': customer
            }
            data['possible_employees'] = self.db.get_employees()
            data['possible_customers'] = self.db.get_customers()

            return self.view.renderTemplateWithDictionary("projects/p_edit.mako", data_op=data)

    def re_edit(self,error_msg, id, number,title,desc,startdate, duration, budget,customer,**args):
        ##data = self.find_project_by_id(id)
        data = {
            "id": id,
            "number": number,
            "title": title,
            'desc': desc,
            'startdate': startdate,
            'duration': duration,
            'budget': budget,
            'employee': args,
            'customer': customer
        }
        data['possible_employees'] = self.db.get_employees()
        data['possible_customers'] = self.db.get_customers()
        data['msg'] = "Fehler aufgetreten: %s" % error_msg
        return self.view.renderTemplateWithDictionary("projects/p_edit_error.mako", data_op=data)

    @cherrypy.expose
    def show(self, project_id):
        data = self.find_project_by_id(project_id)
        if data is not None:
            data['possible_employees'] = self.db.get_employees()
            data['possible_customers'] = self.db.get_customers()

            for empl in data['employee']:
                for possible_empl in data['possible_employees']:
                    if empl['employee_id'] == possible_empl['id']:
                        empl['name'] = possible_empl['lastname']
            data['employee'] = sorted(data['employee'], key=lambda x: x['name'])

            return self.view.renderTemplateWithDictionary("projects/p_detail_time.mako", data_op=data)
        else:
            return self.default_view('Datensatz nicht vorhanden.')

    @cherrypy.expose
    def delete(self, num=None):
        self.delete_project(num=num)
        return self.default_view('Datensatz gelöscht.')

    def get_projects(self):
        return self.db.readFile('project.json')

    def find_project_by_id(self, num):
        return self.db.findId('project.json', num)

    def update_project(self, num, number, title, desc, startdate, duration, budget,employee,customer):
        dictionary = self.db.readFile('project.json')
        data = []
        lastEmplId = None
        lastEntry = None
        # incoming ex. " '1-pw0': 1 "
        # [{"employee_id": 1, "pw0": 3, "pw1": 5, "pw2": 1, "pw3": 2},...] <- Needed format

        for entry in employee:
            info = entry.split("-")
            value = employee[info[0]+'-'+info[1]]
            if value is '':
                continue
            if lastEmplId is not info[0]:
                lastEntry = {'employee_id': int(info[0])}
                lastEntry[info[1]] = value
                lastEmplId = info[0]
                data.append(lastEntry)
            else:
                lastEntry[info[1]] = value

        ##Sort to lastname?
        for entry in dictionary['data']:
            if entry['id'] == int(num):
                entry['number'] = int(number)
                entry['title'] = title
                entry['desc'] = desc
                entry['startdate'] = startdate
                entry['duration'] = duration
                entry['budget'] = budget
                entry['customer'] = int(customer)
                entry['employee'] = data
                self.db.writeFile('project.json', dictionary)
                return True
        return False

    def add_project(self, number, title, desc, startdate, duration, budget, employee, customer):
        dictionary = self.db.readFile('project.json')
        num = int(self.db.getMaxId('project.json') + 1)
        data = []
        lastEmplId = None
        lastEntry = None
        for entry in employee:
            info = entry.split("-")
            value = employee[info[0] + '-' + info[1]]
            if value is '':
                continue
            if lastEmplId is not info[0]:
                lastEntry = {'employee_id': int(info[0])}
                lastEntry[info[1]] = value
                lastEmplId = info[0]
                data.append(lastEntry)
            else:
                lastEntry[info[1]] = value
        dictionary['data'].append({
            "id": int(num),
            "number": int(number),
            "title": title,
            "desc": desc,
            "startdate": startdate,
            "duration": duration,
            "budget": budget,
            "customer": int(customer),
            "employee": data
        })
        self.db.writeFile('project.json', dictionary)
        return num

    def delete_project(self, num):
        dictionary = self.db.readFile('project.json')
        result = {"data": []}
        for entry in dictionary['data']:
            if entry['id'] != int(num):
                result['data'].append(entry)
                self.db.writeFile('project.json', result)
