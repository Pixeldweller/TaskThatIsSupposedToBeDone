# coding: utf-8

# Demonstrator / keine Fehlerbehandlung

import cherrypy

from p3.app.database import Database_cl
from p3.app.view import View_cl

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
class Custom_cl(object):
#----------------------------------------------------------

   exposed = True # gilt für alle Methoden

   #-------------------------------------------------------
   def __init__(self, path):
   #-------------------------------------------------------
      # spezielle Initialisierung können hier eingetragen werden
      self.db_o = Database_cl(path)
      self.view_o = View_cl()

   #-------------------------------------------------------
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
      data_a = self.db_o.read_px()
      # default-Werte entfernen
      ndata_a = data_a[1:]
      return self.view_o.createList_px(ndata_a)
   
   #-------------------------------------------------------
   def getDetail_p(self, id_spl):
   #-------------------------------------------------------
      data_o = self.db_o.read_px(id_spl)
      return self.view_o.createDetail_px(data_o)
# EOF