# coding: utf-8

import json
import cherrypy

#----------------------------------------------------------
class View_cl(object):
#----------------------------------------------------------

   #-------------------------------------------------------
   def __init__(self):
   #-------------------------------------------------------
      pass

   #-------------------------------------------------------
   def createList_px(self, data_opl):
   #-------------------------------------------------------
      
      retVal_o = {
         'data': data_opl
      }
      return json.dumps(data_opl)

   #-------------------------------------------------------
   def createDetail_px(self, data_opl):
   #-------------------------------------------------------

      retVal_o = {
         'data': data_opl
      }
      return json.dumps(data_opl)

   def createAlert(self, alert_msg, code = None):
      if code is None:
         cherrypy.response.status = "405"
      else:
         cherrypy.response.status = code
      alert = {
         'alert': ''+alert_msg
      }
      return alert

   # 200 : OK / 201 : Created / 204 : No Content
   def createFeedbackMessage(self, feedback_msg, code = None):
      if code is None:
         cherrypy.response.status = "202"
      else:
         cherrypy.response.status = code
      feedback = {
         'feedback': ''+feedback_msg
      }
      return feedback

# EOF