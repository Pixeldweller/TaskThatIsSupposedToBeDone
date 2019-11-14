import os.path
import cherrypy

from mako import exceptions
from mako.lookup import TemplateLookup

class View(object):
    def __init__(self, path):
        self.templatesPath = os.path.join(path, 'templates')
        self.myLookup = TemplateLookup(directories=[self.templatesPath])

    def create(self, templateName, pageType):
        myTemplate = self.myLookup.get_template(templateName)
        return myTemplate.render(page = pageType)
    create.exposed = True

    def renderTemplate(self, templateName, pageType):
        myTemplate = self.myLookup.get_template(templateName)
        return myTemplate.render(page = pageType)

    def renderTemplateWithSingleParam(self, templateName, arg_p):
        myTemplate = self.myLookup.get_template(templateName)
        return myTemplate.render(arg = arg_p)

    def renderTemplateWithDictionary(self, templateName, data_op):
        try:
            myTemplate = self.myLookup.get_template(templateName)
            return myTemplate.render(data_o = data_op)
        except:
            return exceptions.html_error_template().render()

    def renderTemplateWithTwoDictionaries(self, templateName, data_0p, data_1p):
        try:
            myTemplate = self.myLookup.get_template(templateName)
            return myTemplate.render(data_0=data_0p, data_1=data_1p)
        except:
            return exceptions.html_error_template().render()
