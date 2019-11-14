# coding: utf-8

# Demonstrator / keine Fehlerbehandlung

import cherrypy

from .database import Database_cl
from .view import View_cl

# Method-Dispatching!

# Übersicht Anforderungen / Methoden

"""

Anforderung       GET    
-------------------------
/                 Liste  
                  liefern

/{id}             Detail  
                  mit {id}
                  liefern
"""

#----------------------------------------------------------
class Application_cl(object):
#----------------------------------------------------------

   exposed = True # gilt für alle Methoden

   #-------------------------------------------------------
   def __init__(self,path):
   #-------------------------------------------------------
      # spezielle Initialisierung können hier eingetragen werden
      self.db_o = Database_cl(path)
      self.view_o = View_cl()

   #-------------------------------------------------------
   @cherrypy.tools.json_out()
   def GET(self, id=None):
   #-------------------------------------------------------
      retVal_s = ''
      if id == None:
         # Anforderung der Liste
         retVal_s = self.getList_p()
      else:
         # Anforderung eines Details
         retVal_s = self.getDetail_p(id)
      return retVal_s
      
   #-------------------------------------------------------
   def getList_p(self):
   #-------------------------------------------------------
      # default-Werte entfernen
      #ndata_a = data_a[1:]
      return self.db_o.readFile('data_a.json')['data']
      #return self.view_o.createList_px(ndata_a)
   #-------------------------------------------------------
   def getDetail_p(self, id_spl):
   #-------------------------------------------------------
      #return self.view_o.createFeedbackMessage("Hah, it works.")
      #return self.view_o.createAlert("TEST")
      return self.db_o.findId("data_a.json",id_spl)
# EOF