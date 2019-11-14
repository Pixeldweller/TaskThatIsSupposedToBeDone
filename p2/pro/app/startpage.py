import cherrypy
import html

class StartPage(object):

    def __init__(self, view, db):
        self.db = db
        self.view = view
        self.pageCount = 0


    @cherrypy.expose
    def index(self):
        self.pageCount = self.pageCount + 1
        if cherrypy.session.get('user') == None:
            raise cherrypy.HTTPRedirect("/")
        else:
            return self.default_view()


    # Soll überschrieben werden in Kindklassen
    def default_view(self):
        return self.view.renderTemplate("greeting.mako", pageType = self)

    def getPageCount(self):
        return self.pageCount

    def escape(self, input, type=None):
        if type is not None:
            if type(input) is not type:
                raise self.view.renderTemplateWithSingleParam("page404.mako", 'Argument %s is not viable as type %s' %(input,type))
        return html.escape(input)
