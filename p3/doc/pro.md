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

###Datenhaltung
Gespeichert werden die Anwendungsdaten in JSON-Dateien. Projektinformationen landen in der `projects.json`, die Mitarbeiterdaten werden in der Datei `employee.json`, die Komponenten in `component.json`, die Kategorien in `bug_category.json` bzw. `cause_category.json` und die Fehlerobjekte werden in der Datei `bug.json` abgelegt. Die Daten werden als Dictionary mit Eintrag `data` gespeichert. Der Eintrag `data` ist ein Array und beinhaltet eine Anzahl von JSON-Objekten. Jedes dieser Objekte beinhaltet die Daten des entsprechenden Objekttyps.


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

### Templateverarbeitung
Alle Fachobjekt Templates folgen dem Muster: ***fachobjektname*-[*list/edit/detail*].tpl.html**.

Diese werden dann auch entsprechend zu den angeforderten Ansichtstypen mit den passenden Fachobjektdaten vom Generator eingesetzt.

## Prüfung MarkUp und Stilregeln
| Hilfsmittel / Validatoren | Ergebnisse | Warnungen |
| --- | :---: | --- |
| w3c-Validator-Dienste (Markup)  | Keine Fehler | <ul><li>The type attribute is unnecessary for JavaScript resources.</li><li>The date input type is not supported in all browsers. Please be sure to test, and consider using a polyfill.</li></ul> |
| w3c-Validator-Dienste (CSS)     | Keine Fehler | <p style="text-align:center;">-</p> 







### Aufgabe der Anwendung
Die zu entwickelnde Anwendung ist eine Projektverwaltungssoftware, welche als Webanwendung realisiert wird. Nach seiner Anmeldung wird es einem Nutzer ermöglicht Projektdaten, Mitarbeiterinformationen und Kundeneinträge einzusehen, zu editieren, entfernen oder neu anzulegen und zusätzlich eine Auswertung zu den vorhandenen Projekten zu erhalten. Bei dem Anlegen von Projekten wird dann immer ein Kunde zugeordnet und die zugehörigen Mitarbeiter durch das Eintragen von Stundenanteilen im Projektplan zugeteilt.
### Fachliche Funktion
Die Anwendung hat eine Administrations- und Auswertungsfunktion für die Plaunung und Verwaltung von simplen Projekten jeglicher Art. Daher gibt es auch zusätzlich eine Kunden- und Mitarbeiterverwaltung. Diese  können dann einem Projekt zugewiesen bzw. durch Arbeitszeit-Angaben in diversen Projektwochen zugeordnet werden.

## Beschreibung der Komponenten des Servers

### `server.py`
Setzt das Anwendungsroot Verzeichnis, lädt die Serverkonfiguration und startet die CherryPy-Anwendung.

### `application.py`
Das ist das Root-Modul des CherryPy-Servers, welcher hauptsächlich die HTTP Anfragen an seine Member delegiert und nur für unbekannte Anfragen bzw. Login-Anfragen zuständig ist.

####Member:
___  
    view : View
        Template Rendering Modul
    db : Database
        I/O Modul für .json Dateien
    startPage : StartPage
        Standard '/' -Seitenmodul
    projects : ProjectsPage
        '/projects/' - Seitenmodul
    employees : EmployeesPage
        '/employees/' - Seitenmodul
    customers : CustomersPage
        '/customers/' - Seitenmodul
    report : ReportPage
        '/report/' - Seitenmodul

####Methoden:
___   
    index()
       '/' - Aufruf: Prüft, ob Session User besitzt und ruft das Login auf,
        sonst wird an die index() der StartPage delegiert...
    
    default(*arguments, **kwargs)
        Unbekannter Aufruf: wird mit "404 NOT FOUND"-Seite abgefangen.
    
    login(username, password=None)
       '/login' - POST-REQUEST: Fügt Usernamen der Session hinzu und leitet an StartPage weiter.
    


### `view.py`
Rendert die HTML Seiten mit Aufrufen der Mako-Template-Engine und erhält entsprechende Daten für die Dokumente per Parameterübergabe von den aufrufenden Seiten-Modulen.
Dieses Modul wird von der `application.py` weitergegeben an die Seitenmodule, sodass diese die Rendermethoden aufrufen können.

####Member:
___  
    templatesPath : str
        Verzeichnispfad zu den Mako-Template-Dateien
    myLookup : TemplateLookup
        Mako Template Loader Objekt

####Methoden
___       
    renderTemplate(templateName, pageType)
        Erzeugt ein HTML-Dokument und übergibt dem Template Renderer eine Seitenmodulreferenz.
    renderTemplateWithDictionary(templateName, data_o):
        Erzeugt ein HTML-Dokument und übergibt dem Template Renderer ein Dictonary-Objekt.
        
        
### `database.py`
Das Database Modul liefert die Schnittstelle zu den JSON-Dateien, in welcher die Anwendungsinformationen persistiert werden. Es ließt bzw. schreibt die Anwendungsdaten in die jeweiligen Objekt-Dateien.
Dieses Modul wird von der `application.py` weitergegeben an die Seitenmodule, sodass diese die Datenbankmethoden von den einzelnen Seitentypen aufgerufen werden können.

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
        
### `startpage.py`
Das StartPage-Modul ist die Elternklasse sonstiger Seitenmodule. Hier ist für jeden Seitentyp die `index()` Methode definiert, welche überprüft, dass bei ablaufender Session wieder zum Login umleitet wird. Sonst wird dieser Aufruf weiter an die Methode `default_view()` umleitet.

####Member:
___  
    db : Database
        I/O Modul für .json Dateien
    view : View
        Template Rendering Modul

####Methoden: 
___ 
    index()
        '/[membername in application.py]/'- Aufruf: Ruft `default_view()` Methode oder Login-Maske auf, falls die Session abgelaufen ist.
    
    default_view():
        Standardansicht des Seitentyps: Im Fall StartPage wird eine Begrüßung gerendert.
    
    escape(input, type=None):
        Gibt bei HTML-Zeichen im input einen "gereinigten" Text zurück, um Injections zu verhindern
####Sonstiges:
Bei der Struktur der Mako-Templates wurde eine Basisklassen Hierarchie eingesetzt, bei welcher jedes Template eine `basepage.mako` inkludiert, welche Platzhalterblöcke besitzt, die dann von den entsprechenden spezialisierten Templates von den Seitenmodulen dann gefüllt bzw. überschrieben werden.

### `projectspage.py`
Die ProjectPage ist eine abgeleitete Klasse der StartPage. Hier liefert die `default_view()` Methode eine Projektübersicht, bei welcher das Anzeigen, Editieren, Löschen und neu Anlegen von Projektdaten zur Verfügung gestellt wird.
Außerdem liefert diese Seite die Hauptschnittstellen `.../show/...`,`.../edit/...`,`.../add/...`, und `.../delete/...` an. Bei jeder dieser Methoden werden entsprechende Dictionaries aus der `Database` geladen, aufbereitet und anschließend der `View` für das Rendering übergeben.
####Member:
___  
    db : Database
        I/O Modul für .json Dateien
    view : View
        Template Rendering Modul

####Hauptmethoden: 
___     
    default_view(feedbackmessage = ''):
        '/projects/'- Aufruf: Zeigt Projektübersicht mit Verwaltungsoptionen an. Falls 'feedbackmessage' gesetzt wurde, wird ein Feedbackpanel mit entsprechender Nachricht angezeigt. Die Session Variable 'p_table_view' entscheidet darüber, ob das Kachelansicht Template oder das Tebellenansicht Template der View übergeben wird.
   
    show(input, project_id):
        '/projects/show/...': Wechselt in die Einzelansicht für nur ein Projekt mit ID = 'project_id'
        
    edit(p_id, reloaded=False, num=-1, title='-Neuer Titel-', desc='-Neue Beschreibung-', startdate='',
             duration=1, budget=0.0, customer=0):
         '/projects/edit/...': Wechselt in den Bearbeitungsmodus bzw. in das neu Anlegen eines Projektes, je nachdem, wie diese Methode aufgerufen wird.   
    
    re_edit(error_msg, id, number,title,desc,startdate, duration, budget,customer,**args):
         Bleibt im Bearbeitungsmodus, falls beim Speichern einer Aktualisierung ein Fehler aufgetreten ist. Zusätzlich wird noch eine Fehlermeldung 'error_msg' in einem Feedbackpanel präsentiert.  
    
    add(id, number,title,desc,startdate, duration,budget,customer,**args):
        '/projects/add/...': Aktualisiert oder legt einen neuen Datensatz mit der ID 'id' und den dem entsprechenden Parametern an. Das '**args' Argument enthält eine Liste mit Zuordnungen zwischen Mitarbeiter-Zeiten zu Projektwochen und wird in dieser Methode geparst.
        Danach wird auf die 'default_view' mit entsprechender Statusmeldung weitergeleitet.
       
    delete(num)
        '/projects/delete/...': Löscht ein Projekteintrag mit der ID 'num' und leitet auf 'default_view' mit Löschmeldung weiter.
    
    table_view(changeMode = False):
        '/projects/table_view/[changeMode]': Wechselt zwischen Kachelansicht und Tabellenansicht und speichert Information in Session-Objekt, damit Präferenz gespeichert wird.

### `employeespage.py`
Die EmployeesPage ist eine abgeleitete Klasse der StartPage. Hier zeigt die `default_view()` Methode eine Mitarbeiterübersicht an, bei welcher das Anzeigen, Editieren, Löschen und neu Anlegen von Mitarbeitereinträgen zur Verfügung gestellt wird.
Außerdem liefert diese Seite die Hauptschnittstellen `.../show/...`,`.../edit/...`,`.../add/...`, und `.../delete/...` an. Bei jeder dieser Methoden werden entsprechende Dictionaries aus der `Database` geladen, aufbereitet und anschließend der `View` für das Rendering übergeben.
####Member:
___  
    db : Database
        I/O Modul für .json Dateien
    view : View
        Template Rendering Modul

####Hauptmethoden: 
___     
    default_view(feedbackmessage = ''):
        '/employees/'- Aufruf: Zeigt Mitarbeiterübersicht mit Verwaltungsoptionen an. Falls 'feedbackmessage' gesetzt wurde, wird ein Feedbackpanel mit entsprechender Nachricht angezeigt.
   
    show(input, num):
         '/employees/show/...': Wechselt in die Einzelansicht für nur ein Mitarbeiter mit ID = 'num'
        
    edit(num):
         '/employees/edit/...': Wechselt in den Bearbeitungsmodus bzw. in das neu Anlegen eines Mitarbeitereintrags, je nachdem, wie diese Methode aufgerufen wird bzw. falls der num Wert in .json-Datei vorhanden ist.
    
    re_edit(error_msg, id, lastname, firstname, address, email, role):
         Bleibt im Bearbeitungsmodus, falls beim Speichern einer Aktualisierung ein Fehler aufgetreten ist. Zusätzlich wird noch eine Fehlermeldung 'error_msg' in einem Feedbackpanel präsentiert.  
    
    add(id, lastname, firstname, address, email, role):
        '/employees/add/...': Aktualisiert oder legt einen neuen Datensatz mit der ID 'id' und den dem entsprechenden Parametern an.
        Danach wird auf die 'default_view' mit entsprechender Statusmeldung weitergeleitet.
       
    delete(num)
        '/employees/delete/...': Löscht einen Mitarbeitereintrag mit der ID 'num' und leitet bei erfolgreichem Speichern auf 'default_view' mit Löschmeldung weiter, sonst wird eine Fehlermeldung gegeben.

### `customerspage.py`
Die CustomersPage ist eine abgeleitete Klasse der StartPage. Hier bietet die `default_view()` Methode ein Kundenregister an, bei welcher das Anzeigen, Editieren, Löschen und neu Anlegen von Mitarbeitereinträgen zur Verfügung gestellt wird.
Außerdem liefert diese Seite die Hauptschnittstellen `.../show/...`,`.../edit/...`,`.../add/...`, und `.../delete/...` an. Bei jeder dieser Methoden werden entsprechende Dictionaries aus der `Database` geladen, aufbereitet und anschließend der `View` für das Rendering übergeben.
####Member:
___  
    db : Database
        I/O Modul für .json Dateien
    view : View
        Template Rendering Modul

####Hauptmethoden: 
___     
    default_view(feedbackmessage = ''):
        '/customers/'- Aufruf: Zeigt Kundenregister mit Verwaltungsoptionen an. Falls 'feedbackmessage' gesetzt wurde, wird ein Feedbackpanel mit entsprechender Nachricht angezeigt.
   
    show(input, num):
        '/customers/show/...': Wechselt in die Einzelansicht für nur einen Kunden mit ID = 'num'
        
    edit(num):
        '/customers/edit/...': Wechselt in den Bearbeitungsmodus bzw. in das neu Anlegen eines Kundeneintrags, je nachdem, wie diese Methode aufgerufen wird bzw. falls der 'num' Wert in .json-Datei vorhanden ist.
    
    re_edit(error_msg, id, name, number, contact, address, email, phn):
         Bleibt im Bearbeitungsmodus, falls beim Speichern einer Aktualisierung ein Fehler aufgetreten ist. Zusätzlich wird noch eine Fehlermeldung 'error_msg' in einem Feedbackpanel präsentiert.  
    
    add(id, name, number, contact, address, email, phn):
        '/customers/add/...': Aktualisiert oder legt einen neuen Datensatz mit der ID 'id' und den dem entsprechenden Parametern an.
        Danach wird auf die 'default_view' mit entsprechender Statusmeldung weitergeleitet.
       
    delete(num)
        '/customers/delete/...': Löscht einen Kunden aus dem Register mit der ID 'num' und leitet bei erfolgreichem Speichern auf 'default_view' mit Löschmeldung weiter, sonst wird eine Fehlermeldung gegeben.

### `reportpage.py`
Die ReportPage ist eine abgeleitete Klasse der StartPage. Hier gibt die `default_view()` Methode eine Auswertungsansicht zurück, bei welcher entsprechende Daten aus der `Database` gelesen werden, aufbereitet und dann der `View` mit entsprechendem Templatepfad und Datensatz übergeben wird.
Die Übersicht zeigt, wie in der Aufgabenstellung formuliert, eine Projektübersicht mit allen Projekten nach Projekttitle sortiert und mit der Auflistung der Projektmitarbeiter, sortiert nach Nachname und Vorname und den entsprechenden wöchentlichen Aufwänden.
####Member:
___  
    db : Database
        I/O Modul für .json Dateien
    view : View
        Template Rendering Modul

####Hauptmethoden: 
___     
    default_view(feedbackmessage = ''):
        '/report/'- Aufruf: Zeigt Projektübersichtsauswertung nach definierten Kriterien der Aufgabenstellung.
   

## Datenablage
Gespeichert werden die Anwendungsdaten in JSON-Dateien. Projektinformationen landen in der `projects.json`, die Mitarbeiterdaten werden in der Datei `employee.json` und die Kundenregister werden in der Datei `customer.json` abgelegt. Die Daten werden als Dictionary im Eintrag `data` gespeichert. Der Eintrag `data` ist ein Array und beinhaltet eine Anzahl von Dictionaries. Jedes dieser Dictionaries beinhaltet die Daten pro Kunden/Mitarbeiter/Projekt.
## Durchführung und Ergebnis der geforderten Prüfungen:
| Hilfsmittel / Validatoren | Ergebnisse | Warnungen |
| --- | :---: | --- |
| w3c-Validator-Dienste (Markup)  | Keine Fehler | <ul><li>The type attribute is unnecessary for JavaScript resources.</li><li>The date input type is not supported in all browsers. Please be sure to test, and consider using a polyfill.</li></ul> |
| w3c-Validator-Dienste (CSS)     | Keine Fehler | <p style="text-align:center;">-</p> 