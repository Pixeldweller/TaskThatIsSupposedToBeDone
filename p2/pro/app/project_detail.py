import cherrypy
import datetime

from .startpage import StartPage


class ProjectDetail(StartPage):

    def __init__(self, view,db):
        StartPage.__init__(self,view,db)

    def default_view(self):
        raise cherrypy.HTTPRedirect("/projects")

    @cherrypy.expose
    def show(self, project_id):
        pro_dict = self.db.findId('project.json', project_id)
        c = self.db.findId('customer.json',  pro_dict['customer'])
        pro_dict['customer'] = c['name']
        pro_dict['possible_employees'] = self.db.get_employees()
        detail =  self.find_project_detail_by_id(project_id)
        if detail is None:
            detail = {
                "id": project_id,
                "entry": []
            }
        detail_dict = detail['entry']

        return self.view.renderTemplateWithTwoDictionaries("projects/p_detail_time.mako", data_0p=pro_dict, data_1p=detail_dict)

    @cherrypy.expose
    def add(self, project_id, employee_id, **pw_list):
        data = self.find_project_detail_by_id(project_id)
        try:
            if data is not None:
                updated = self.update_project_detail(project_id, employee_id, pw_list)
                return updated
            else:
                added = self.add_project_detail(project_id, employee_id, pw_list)
                return self.show(project_id)
        except Exception as e:
           return self.show(project_id) +str(e)



    @cherrypy.expose
    def delete(self, num=None):
        ##self.delete_project(num=num)
        raise cherrypy.HTTPRedirect("/projects_detail")

    def get_project_details(self):
        return self.db.readFile('project_employee_data.json')['data']

    def find_project_detail_by_id(self, num):
        return self.db.findId('project_employee_data.json', num)

    def update_project_detail(self, project_id, employee_id, pw_list):
        dictionary = self.db.readFile('project_employee_data.json')

        element = {
            'employee_id': int(employee_id)
        }

        for i in range(len(pw_list)):
            if not pw_list['pw' + str(i)] == '':
                element['pw'+str(i)] = int(pw_list['pw'+str(i)])

        for entry in dictionary['data']:
            if entry['id'] == int(project_id):
                already_known = False
                i = 0
                for employee in entry['entry']:
                    if employee['employee_id'] == int(employee_id):
                        already_known = True
                    elif not already_known:
                        i += 1
                if already_known:
                    del entry['entry'][i]
                entry['entry'].append(element)


        self.db.writeFile('project_employee_data.json', dictionary)
        return self.show(project_id)

    def add_project_detail(self, project_id, employee_id, pw_list):
        dictionary = self.db.readFile('project_employee_data.json')

        element = {
            'employee_id': int(employee_id)
        }

        for i in range(len(pw_list)):
            if not pw_list['pw' + str(i)] == '':
             element['pw' + str(i)] = int(pw_list['pw' + str(i)])

        data = []
        data.append(element)
        dictionary['data'].append({
            "id": int(project_id),
            "entry": data
        })
        self.db.writeFile('project_employee_data.json', dictionary)
        return project_id




