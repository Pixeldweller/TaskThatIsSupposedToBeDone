import json
import os.path

# coding: utf-8
#----------------------------------------------------------
class Database_cl(object):
#----------------------------------------------------------

   #-------------------------------------------------------
   def __init__(self, path):
      self.path = os.path.join(path, "data")
   #-------------------------------------------------------

   def readFile(self, file):
      myfile = os.path.join(self.path, file)
      if os.path.isfile(myfile):
         with open(myfile, 'r', encoding='utf8') as f:
            return json.load(f)
      else:
         data = {"data": []}
         with open(myfile, 'w') as f:
            json.dump(data, f)
         return data


   def writeFile(self, file, dict):
      myfile = os.path.join(self.path, file)
      with open(myfile, 'w', encoding='utf8') as f:
         json.dump(dict, f, ensure_ascii=False)


   def getMaxId(self, file):
      dictionary = self.readFile(file)['data']
      if len(dictionary) is 0:
         return 0
      return dictionary[-1]['id']

   def isNumber(self, s):
      try:
         int(s)
         return True
      except ValueError:
         return False


   def findId(self, file, id):
      if not self.isNumber(id):
         return None

      jsonFile = self.readFile(file)

      for entry in jsonFile['data']:
         if int(id) is int(entry['id']):
            return entry
      return None

   def findIdInData(self, data, id):
      if not self.isNumber(id):
         return None

      for entry in data:
         if int(id) is int(entry['id']):
            return entry
      return None


   # -- Hilfreich Listenobjekte

   def get_projects(self):
      return self.readFile('project.json')['data']

# EOF