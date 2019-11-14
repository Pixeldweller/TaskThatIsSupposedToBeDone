import cherrypy
import html
from app.view import View
from app.database import Database
from app.startpage import StartPage
from app.employeespage import EmployeesPage
from app.customerspage import CustomersPage
from app.projectspage import ProjectsPage
from app.reportpage import ReportPage

class Application(object):

    def __init__(self, path):
        self.view = View(path)
        self.database = Database(path)
        self.startPage = StartPage(self.view,self.database)
        self.employees = EmployeesPage(self.view,self.database)
        self.projects = ProjectsPage(self.view,self.database)
        self.customers = CustomersPage(self.view,self.database)
        self.report = ReportPage(self.view, self.database)


    # HOMEPAGE / MAIN PAGE
    @cherrypy.expose
    def index(self):
        #cherrypy.session['user'] = 'TestUser'
        if cherrypy.session.get('user') == None:
            return self.view.create("homepage_login.mako",self.startPage)
        else:
            return self.startPage.index()


    @cherrypy.expose
    def default(self, *arguments, **kwargs):
        msg_s = "unbekannte Anforderung: " + \
            str(arguments) + \
            ' ' + \
            str(kwargs)
        return self.view.renderTemplateWithSingleParam("page404.mako", msg_s)


    @cherrypy.expose
    def login(self, username=None, password=None):
        if username:
            output="Great %s !" % html.escape(username)
            cherrypy.session['user'] = html.escape(username)
            cherrypy.session['p_table_view_active'] = False
        else:
            output="Uhhhm..."
        return self.index()
