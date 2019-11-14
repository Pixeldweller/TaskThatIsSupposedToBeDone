import cherrypy
from app.startpage import StartPage

class Customers(StartPage):

    def __init__(self, view, db):
        StartPage.__init__(self,view,db)

    def default_view(self):
        return self.view.renderTemplateWithDictionary("customers/c_table.mako", data_op=self.get_customers())

    def body_feedback(self, error_msg):
        data_o = self.get_customers()
        data_o['error'] = error_msg
        return self.view.renderTemplateWithDictionary("customers/c_table_error.mako", data_op=data_o)

    @cherrypy.expose
    def show(self, num):
        data = self.get_customer_by_id(num)
        if data is not None:
            return self.view.renderTemplateWithDictionary("customers/c_show.mako", data_op=data)
        else:
            return self.body_feedback('Datensatz nicht gefunden.')

    @cherrypy.expose
    def add(self, id, name, number, contact, address, email, phn):
        data = self.get_customer_by_id(id)
        id = self.escape(id)
        name = self.escape(name)
        number = self.escape(number)
        contact = self.escape(contact)
        address = self.escape(address)
        email = self.escape(email)
        phn = self.escape(phn)
        try:
            if data is not None:
                updated = self.update_customer(id, name, number, contact, address, email, phn)
                return self.body_feedback('Update erfolgreich.')
            else:
                added = self.add_customer(name, number, contact, address, email, phn)
                return self.body_feedback('Hinzufügen erfolgreich.')
        except Exception as e:
            return self.re_edit( str(e), id, name, number, contact, address, email, phn)

    @cherrypy.expose
    def edit(self, num):
        data = self.get_customer_by_id(num)
        if data is not None:
            return self.view.renderTemplateWithDictionary("customers/c_edit.mako", data_op=data)
        else:
            data = {
                "id": self.db.getMaxId("customer.json") + 1,
                "number": self.db.getMaxId("customer.json") + 1,
                "name": '-Neuer Kundenname-',
                'contact': '-Neuer Ansprechpartner-',
                'address': '-Neue Adresse-',
                'phn': '-Neue Telefonnummer-',
                'email': '-neue@email.com-'
            }
            return self.view.renderTemplateWithDictionary("customers/c_edit.mako", data_op=data)

    def re_edit(self, error_msg, id, name, number, contact, address, email, phn):
        data = {
            "id": id,
            "number": number,
            "name": name,
            'contact': contact,
            'address': address,
            'phn': email,
            'email': phn
        }
        data['msg'] = error_msg
        return self.view.renderTemplateWithDictionary("customers/c_edit_error.mako", data_op=data)

    @cherrypy.expose
    def delete(self, num=None):
        return self.delete_customer(id=num)

    def get_customers(self):
        return self.db.readFile('customer.json')

    def get_customer_by_id(self, id):
        return self.db.findId('customer.json', id)

    def update_customer(self, id, name, number, contact, address, email, phn):
        dictionary = self.db.readFile('customer.json')

        for entry in dictionary['data']:
            if entry['id'] == int(id):
                entry['name'] = name
                entry['number'] = int(number)
                entry['contact'] = contact
                entry['address'] = address
                entry['email'] = email
                entry['phn'] = phn
                self.db.writeFile('customer.json', dictionary)
                return True
        return False

    def add_customer(self, name, number, contact, address, email, phn):
        dictionary = self.db.readFile('customer.json')
        id = int(self.db.getMaxId('customer.json') + 1)
        dictionary['data'].append({
            "id": int(id),
            "number": int(number),
            "name": name,
            "contact": contact,
            "address": address,
            "phn": phn,
            "email": email
        })
        self.db.writeFile('customer.json', dictionary)
        return id

    def delete_customer(self, id):
        dictionary = self.db.readFile('customer.json')
        dictionary_project = self.db.readFile('project.json')

        for packet in dictionary_project['data']:
            if packet['customer'] == int(id):
                return self.body_feedback('Dieser Datensatz wird noch in einem Projektobjekt referenziert und kann daher nicht gelöscht werden.')

        result = {"data": []}
        for entry in dictionary['data']:
            if entry['id'] != int(id):
                result['data'].append(entry)
        self.db.writeFile('customer.json', result)
        return self.body_feedback('Der Datensatz wurde gelöscht.')
