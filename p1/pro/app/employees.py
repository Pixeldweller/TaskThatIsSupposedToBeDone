import cherrypy
from .startpage import StartPage


class Employees(StartPage):

    def __init__(self, view,db):
        StartPage.__init__(self,view,db)

    def default_view(self):
        return self.view.renderTemplateWithDictionary("employees/e_table.mako", data_op=self.get_employees())

    def body_feedback(self, error_msg):
        data_o = self.get_employees()
        data_o['error'] = error_msg
        return self.view.renderTemplateWithDictionary("employees/e_table_error.mako", data_op=data_o)

    @cherrypy.expose
    def edit(self, num):
        data = self.find_employee_by_id(num)
        if data is not None:
            return self.view.renderTemplateWithDictionary("employees/e_edit.mako", data_op=data)
        else:
            data = {
                "id": self.db.getMaxId("employee.json") + 1,
                "number": self.db.getMaxId("employee.json") + 1,
                "firstname": '-Neuer Vorname-',
                'lastname': '-Neuer Nachname-',
                'address': '-Neue Adresse-',
                'email': '-neue@email.com-',
                'role': '-Eine Role-'
            }
            return self.view.renderTemplateWithDictionary("employees/e_edit.mako", data_op=data)

    @cherrypy.expose
    def show(self, num):
        data = self.find_employee_by_id(num)
        if data is not None:
            return self.view.renderTemplateWithDictionary("employees/e_show.mako", data_op=data)
        else:
            return self.body_feedback('Datensatz nicht gefunden.')

    @cherrypy.expose
    def add(self,  id, lastname, firstname, address, email, role):
        data = self.find_employee_by_id(id)
        id = self.escape(id)
        lastname = self.escape(lastname)
        firstname = self.escape(firstname)
        address = self.escape(address)
        email = self.escape(email)
        role = self.escape(role)

        try:
            if data is not None:
                updated = self.update_employee( id, lastname, firstname, address, email, role)
                return self.body_feedback('Update erfolgreich.')
            else:
                added = self.add_employee(lastname, firstname, address, email, role)
                return self.body_feedback('Hinzufügen erfolgreich.')
        except Exception as e:
            return self.re_edit(id, str(e), lastname, firstname, address, email, role)

    def re_edit(self, error_msg, id, lastname, firstname, address, email, role):
        data = {
            "id": id,
            "number": id,
            "firstname": firstname,
            'lastname': lastname,
            'address': address,
            'email': email,
            'role': role
        }
        data['msg'] = error_msg
        return self.view.renderTemplateWithDictionary("employees/e_edit_error.mako", data_op=data)

    @cherrypy.expose
    def delete(self, num=None):
        return self.delete_employee(id=num)

    def get_employees(self):
        return self.db.readFile('employee.json')

    def find_employee_by_id(self, id):
        return self.db.findId('employee.json', id)

    def update_employee(self, id, lastname, firstname, address, email, role):
        dictionary = self.db.readFile('employee.json')

        for entry in dictionary['data']:
            if entry['id'] == int(id):
                entry['lastname'] = lastname
                entry['firstname'] = firstname
                entry['address'] = address
                entry['email'] = email
                entry['role'] = role
                self.db.writeFile('employee.json', dictionary)
                return True
        return False

    def add_employee(self, lastname, firstname, address, email, role):
        dictionary = self.db.readFile('employee.json')
        id = int(self.db.getMaxId('employee.json') + 1)
        dictionary['data'].append({
            "id": int(id),
            "lastname": lastname,
            "firstname": firstname,
            "address": address,
            "email": email,
            "role": role
        })
        self.db.writeFile('employee.json', dictionary)
        return id

    def delete_employee(self, id):
        dictionary = self.db.readFile('employee.json')
        dictionary_project = self.db.readFile('project.json')

        for packet in dictionary_project['data']:
            pro_result = []
            for entry in packet['employee']:
                if entry['employee_id'] == int(id):
                    return self.body_feedback(
                        'Dieser Datensatz wird noch in einem Projektobjekt referenziert und kann daher nicht gelöscht werden.')


        result = {"data": []}
        for entry in dictionary['data']:
            if entry['id'] != int(id):
                result['data'].append(entry)
        self.db.writeFile('employee.json', result)
        return self.body_feedback(
            'Datensatz gelöscht.')

