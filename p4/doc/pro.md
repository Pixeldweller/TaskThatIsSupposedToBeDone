# Web Praktikum P3
## Aufgabenstellung 2: Bug-Tracker

## Einleitung

### Dokumentationsstand
Die Dokumentation für P3 wurde am 13.11.18 erstellt.

###Gruppenzugehörigkeit
Die Gruppe bestand aus den Teilnehmern XXX und YYY.
Dementsprechend haben wir erstmal zwei von einander unabhängige Anwendungen geschrieben, da wir der Meinung waren, dass jeder selbst mit dem eigenem Aufbau seiner Anwendung vertraut sein sollte und wir haben uns lediglich bei Schwierigkeiten gegenseitig unterstützt.
Daraufhin haben wir dann aus beiden Projekten das Optimum zusammengefügt.

## Implementierung des Servers
###REST-Interface
Die REST-Schnittstellen wurden entsprechend der API von Punkt 2.4 aus der Aufgabenstellung übernommen. Es wurden nur einzelne Erweiterungen vorgenommen:
#### 
| Methode | URI| Reaktion|
| --- | :---: | --- |
| GET  | /mitarbeiter/:mitarbeiter-id  | einzelnes Mitarbeiter-Objekt anfordern |
| DELETE     | /mitarbeiter/:mitarbeiter-id   | Mitarbeiter mit der Id :mitarbeiter-id löschen|
| GET  | /kategorie/:kategorie-id  | einzelnes Kategorie-Objekt anfordern |
| DELETE     | /kategorie/:kategorie-id   | Kategorie mit der Id :kategorie-id löschen|
 
###Module
Auf der Serverseite wurden folgende Module eingesetzt:

#### `server.py`
Setzt das Anwendungsroot Verzeichnis, lädt die Serverkonfiguration, setzt die Dispatcherpfade und startet die CherryPy-Anwendung.

#### `database.py`
Das Database Modul liefert die Schnittstelle zu den JSON-Dateien, in welcher die Anwendungsinformationen persistiert werden. Es ließt bzw. schreibt die Anwendungsdaten in die jeweiligen Objekt-Dateien.
Dieses Modul ist member von allen API-Modulen, sodass diese die Datenbankmethoden von den einzelnen Schnittstellen aufgerufen werden können.

####Member:
___  
    path : str
        Verzeichnispfad zu den JSON-Dateien

####Methoden: 
___ 
    readFile(file)
        Liest eine Datei vom Pfad 'file' ein und liefert ein Listenobjekt mit inneren JSON-Objekten zurück.
    writeFile(file, dict):
        Schreibt eine JSON-Objekt-Liste in die datei 'file'. 
    getMaxId(file):
        Gibt den höchsten vorhandenen 'id' Eintrag eines JSON-Objekts in 'file' zurück.
    isNumber(s):
        Prüft, ob 's' vom Typen Integer ist.
    findId(file,id):
        Gibt ein JSON-Objekt mit 'id' aus 'file' zurück.
    findIdInData(data,id):
        Gibt ein JSON-Objekt mit 'id' aus dict 'data' zurück.
                
#### `template.py`
(Vom Demonstrator übernommen)

#### `view.py`
Ist member in allen API-Modulen und hat Methoden zur Erstellung von JSON-Strings, welche Feedbackmessages beinhalten.
 
#### `object/bugs.py`
Ein Modul, welches das REST-Interface für Aufrufe `/fehler` implementiert und für um die Datenkonsistenz der Fehler-Objekte zuständig ist.

#### `object/categories.py`
Ein Modul, welches das REST-Interface für Aufrufe `/kategorie`, `/katfehler` und `/katursache`  implementiert und für um die Datenkonsistenz der Kategorie-Objekte zuständig ist.

#### `object/components.py`
Ein Modul, welches das REST-Interface für Aufrufe `/komponente` implementiert und für um die Datenkonsistenz der Komponenten-Objekte zuständig ist.

#### `object/employees.py`
Ein Modul, welches das REST-Interface für Aufrufe `/mitarbeiter`, `/qsmitarbeiter` und `/swentwickler` implementiert und für um die Datenkonsistenz der Mitarbeiter-Objekte zuständig ist.

#### `object/projects.py`
Ein Modul, welches das REST-Interface für Aufrufe `/projekt` und `/projektkomponenten` implementiert und für um die Datenkonsistenz der Projekt-Objekte zuständig ist.

#### `object/report.py`
Ein Modul, welches das REST-Interface für Aufrufe `/prolist` und `/katlist` implementiert und für die Auswertungserstellung zuständig ist.

#### `object/[...].py`
Alle diese Module implementieren das REST-Interface und implementieren folgende Schnittstellen:

___ 
    GET(id = None, ...)
        Gibt entweder eine Liste des entsprechenden Fachobjekts zurück oder bei übergebenen 'id' das entsprechende Objekt
    PUT(id, ...):
        Aktualisiert ein entsprechendes Fachobjekt und schreibt die Aktualisierung in das entsprechende json-file.
    POST(...):
        Erzeugt ein entsprechendes Fachobjekt mit übergebenen Daten und speichert es in dem entsprechenden json-file.
    DELETE(id, ...):
        Löscht ein Fachobjekt und aktualisiert bzw. entfernt weitere Fachobjekte mit Abhängigkeiten zu diesem Objekt und aktualisiert alle betroffenen json-files.
    
###Datenhaltung
Gespeichert werden die Anwendungsdaten in JSON-Dateien. Projektinformationen landen in der `projects.json`, die Mitarbeiterdaten werden in der Datei `employee.json`, die Komponenten in `component.json`, die Kategorien in `bug_category.json` bzw. `cause_category.json` und die Fehlerobjekte werden in der Datei `bug.json` abgelegt. Die Daten werden als Dictionary mit Eintrag `data` gespeichert. Der Eintrag `data` ist ein Array und beinhaltet eine Anzahl von JSON-Objekten. Jedes dieser Objekte beinhaltet die Daten des entsprechenden Objekttyps.

####Fehler-Objekt:
___ 
      "id": [Fachobjekt ID]
      "startdesc": [Fehlerbeschreibung]
      "causedesc": [Behebungsbemerkung]
      "startdate": [Erfassungsdatum]
      "enddate": [Behebungsdatum]
      "qsemployee": [QS-Mitarbeiter]
      "swemployee": [SW-Entwickler]
      "component": [Komponenten ID]
      "bug_category": [Liste der Fehlerkategorien (mit IDs)]
      "cause_category": [Ursachen Kategorie ID]
      "type": [Status]
      
####Fehler-Kategorie-Objekt / Ursachen-Kategorie-Objekt:
___ 
      "id": [Fachobjekt ID]
      "title": [Kategoriename]
      
####Komponenten-Objekt:
___ 
      "id": [Fachobjekt ID]
      "name": [Komponentenname]
      "project": [Projekt ID]
      "desc": [Komponenten Beschreibung]
####Mitarbeiter-Objekt:
___ 
      "id": [Fachobjekt ID]
      "username": [Anmeldename]
      "lastname": [Nachname]
      "firstname": [Vorname]
      "email": [Email]
      "roleId": [Rolle: 0: QS / 1: SW]
####Projekt-Objekt:
___ 
      "id": [Fachobjekt ID]
      "title": [Projekttitel]
      "desc": [Projekt Beschreibung]
      "component": [Liste der Projektkomponenten]


## Implementierung des Clients
### Klassen
- ###Application_cl:
    Hauptanwendungsklasse. Diese Klasse reagiert auf die veröffentlichten Events des EventServiceHandlers und leitet die Aufforderungen an die entsprechenden Reaktionsverhalten weiter in ihrer `notify_px(...)` funktion.
- ###Cookie_cl:
    Helferklasse für das lesen und schreiben von Cookie-Daten.
- ###SideBar_cl:
    Zuständig für das rendern der Seitennavigation und weiterleiten der Eintragsklick Events.
- ###List_cl:
    Zuständig für das rendern der Listenansichten und das entgegennehmen der Listenansichts Events. 
- ###Detail_cl:
    Zuständig für das rendern der Detailansichten und das entgegennehmen der Detailnansichts Events. 
- ###Edit_cl:
    Zuständig für das rendern der Bearbeitungsmasken und das entgegennehmen der Bearbeitungs Events und validierung der Inputfelder. 
- ###Bug_cl:
    Helferklasse für Bug spezifische Button Events (z.B. Fehler-Prüfung / Lösungsfreigabe / Lösungsablehnung)

Übernommen vom Demonstrator:
- EventServiceHandler_cl:
- Requester_cl
- Generator_cl
- TemplateManager_cl

### Eventservice

In der Eventverarbeitung der diversen Ansichtstypen werden hauptsächlich `app.cmd` Events erzeugt, welche JSON-Objekte gefüllt mit spezifischen Anweisungen enthalten.
Der einzige Subscriber ist hier die `Application_cl` und diese verarbeitet die Anweisungsdaten entsprechend eines `switch-case` Kontrukts, um die konkrete Anforderung durchzuführen.

Es wurde auch das Event `login.cmd` ergänzt, um ein Login-Aufruf zu verarbeiten.

### Templateverarbeitung
Alle Fachobjekt Templates folgen dem Muster: **[*fachobjektname*][*list/edit/detail*].tpl.html**.
Die Bezeichnungen der [*fachobjektnamen*] entsprechen auch den REST-Schnittstellen

Diese werden dann auch entsprechend zu den angeforderten Ansichtstypen mit den passenden Fachobjektdaten vom Generator eingesetzt.

## Prüfung MarkUp und Stilregeln
| Hilfsmittel / Validatoren | Ergebnisse | Warnungen |
| --- | :---: | --- |
| w3c-Validator-Dienste (Markup)  | Keine Fehler | <ul><li>The type attribute is unnecessary for JavaScript resources.</li><li>The date input type is not supported in all browsers. Please be sure to test, and consider using a polyfill.</li></ul> |
| w3c-Validator-Dienste (CSS)     | Keine Fehler | <p style="text-align:center;">-</p> 




