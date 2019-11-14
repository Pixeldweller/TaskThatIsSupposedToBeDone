import cherrypy
import html
from app.view import View
from app.database import Database
from app.startpage import StartPage
from app.employees import Employees
from app.customers import Customers
from app.projects import Projects
from app.project_detail import ProjectDetail

class Application(object):

    def __init__(self, path):
        self.view = View(path)
        self.database = Database(path)
        self.startPage = StartPage(self.view,self.database)
        self.employees = Employees(self.view,self.database)
        self.projects = Projects(self.view,self.database)
        self.customers = Customers(self.view,self.database)
        self.project_detail = ProjectDetail(self.view, self.database)


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
        else:
            output="Uhhhm..."
        return self.index()
