# Interaktive Systeme Praktikum
## Aufgabenstellung: Messehallenplaner

## 1. Einleitung: allgemeine Beschreibung der Aufgabenstellung
Es soll ein Prototyp einer Weblösung für die Bereitstellung einer Messehallenorganisationsanwendung erstellt werden.
**Messeveranstalter**, **Aussteller** und **Besucher** sollen dort auf Messehalleninformationen zugreifen können. 
Sodass Messeveranstalter Ausstellungsflächen anbieten können und Austeller selbstständig ihren Stand dort anmelden können. 
Außerdem erhalten Messebesucher die Möglichkeit sich die aktuellen Messen inklusive Hallenplan angeben zu lassen.

### Dokumentationsstand
Die Dokumentation wurde am 17.05.19 erstellt.

### Aufbau
Für eine mehrzahl von Interaktionen wird ein 3 Komponenten Aufbau mit entsprechenden Hierachie Ebenen genutzt. Eine Navigation, eine Listenansicht und eine Detailansicht bzw. Bearbeitungsansicht
 werden gleichzeitig innerhalb einer Seite vorhanden sein und über Events mit einander Kommunizieren.
 
![](./core/grob.png)
*Desktop Ansicht*


![](./core/mobile.png)
*Mobile Ansicht*

##### Zustandsdiagramm
![](./core/activity.png)


## 2. Nutzungsszenario "Messeveranstaler"
 
### 2.1 Allgemeine Beschreibung
Der Messeveranstalter soll die Möglichkeit haben seine Messen inklusive Hallenauslegung der Standorte im Messehallenplaner einzupflegen.

### 2.2 Benutzergruppe "Messeveranstaler": Beschreibung Persona
Der Veranstalter einer Messe möchte möglichst mit wenig Aufwand seine verfügbaren Messestände den Ausstellern kommunizieren.
Außerdem will er entsprechend der Sicherheitsbestimmungen und Messeveranstaltungsauflagen eine passende Hallenaufteilung haben,
 damit die Messe reibunglos stattfinden kann.

### 2.3 Interaktionsdesign  
### 2.3.1 Übersicht Interaktionen
- Anlegen einer Messeveranstaltung
- Übersicht der eigenen Messen
- Übersicht der angemeldeten Ausstellern + Hallenplan Bearbeitung
### 2.3.2 Anlegen einer Messeveranstaltung
#### Ablaufdiagramm
![](./host/messe_erstellung.png)

#### Wireframes
![](./host/daten_erfassung.png)
![](./host/auswahl_aufteilung.png)
![](./host/freigabe.png)

#### Erläuterungen
######Benötigte Angaben:
- Veranstaltungsname
- Hallen-Typ (Typenliste von Server bereitgestellt)
- Kurz Bezeichnung
- Datum
######Benötigte Auswahl:
- Auswahl der Hallenaufteilung (Auswahl zwischen verschiedenen vorgeschlagenen Varianten der Hallenauteilung)
- Auswahl für die Anmeldung gesperrte Flächen:
    - (Bei der Sperrung der Flächen können in einem Dropdown-Menü Symbole ausgewählt werden für den Grund der Sperrung)
    
###### Erläuterung Sperrungsgrund:
Bei der Sperrung einer Fläche sind folgende Sperrungsgründe möglich:
- Toiletten
- Restaurant
- Büro des Hallenmeisters

######Bespiel Hallenaufteilungen:
![](./host/hallenaufteilung_01.png)
![](./host/hallenaufteilung_02.png)

### 2.3.3 Übersicht der eigenen Messen
#### Wireframes
![](./host/bersicht.png)

#### Erläuterungen 
Hier kann innerhalb einer Liste eine Messe ausgewählt werden (per Klick) und eine **Übersicht der Anmeldungen + Hallenplan** erhalten werden.
Auserdem existiert eine volltext Suche um angezeigte Messen filtern zu können.

######Volltext Suche:
- Textsuche über alle angezeigten Tabellenfelder

### 2.3.4 Übersicht der angemeldeten Ausstellern + Hallenplan Bearbeitung
#### Wireframes
![](./host/bearbeitung_messe.png)

#### Erläuterungen 
In dieser Ansicht können zusätzlich freie Hallenflächen gesperrt werden, Anmeldungen bearbeitet 
und gesperrte Flächen wieder freigegeben werden.
######Bearbeitung:
- Die Bearbeitung erfolgt über Schaltflächen innerhalb des Hallenplans

## 3. Nutzungsszenario "Aussteller"
 
### 3.1 Allgemeine Beschreibung
Der Aussteller soll die Möglichkeit haben eine Übersicht der stattfindenen Messen zu erhalten 
und in welcher er dann selbstständig über eine interaktive Hallenplanansicht einen freien Ausstellungstand anmelden kann. 

### 3.2 Benutzergruppe "Aussteller": Beschreibung Persona
Der Aussteller möchte über anstehende Messeveranstaltungen mit freien Austellungständen informiert werden.
Außerdem will er die Anmeldung möglichst einfach durchführen ohne zu viel Informationen angeben zu müssen bzw. mehrfach bei weiteren Messe Anmeldungen.
Der Austeller sollte einmalig Informationen zu seiner Organisation angeben müssen.

### 3.3 Interaktionsdesign  
### 3.3.1 Übersicht Interaktionen
- Übersicht / Suche von Messen mit verfügbaren Austellungsständen
- Auswahl eines Austellungsstands + Anmeldung an Messe

### 3.3.2 Übersicht / Suche von Messen mit verfügbaren Austellungsständen
#### Wireframe
![](./presenter/Austeller_Messe_Ansicht.png)

#### Erläuterungen
Es wird eine Liste mit anstehenden Messen mit verfügbaren Messeständen angezeigt. Einzelne Messen können per Klick gewählt werden.
Daraufhin wird eine Hallenplan-Ansicht geöffnet. Auserdem existiert eine volltext Suche um angezeigte Messen filtern zu können.

######Volltext Suche:
- Textsuche über alle angezeigten Tabellenfelder

### 3.3.3 Auswahl eines Austellungsstands + Anmeldung an Messe
#### Wireframe
![](./presenter/Austeller_Messe_Ansicht_Anmeldung.png)

#### Erläuterungen
Diese Ansicht wird and die Messeübersichts Seite angehangen. Hier kann eine noch freie Fläche im Hallenplan selektiert werden.
Sobald diese selektiert wird, werden Eingabemasken für die Anmeldung freigeschaltet. Sollte bei der ausgewählten Messe bereits ein Platz gebucht sein,
wird anstatt der Anmeldungsoption eine **Stornierungs**-Option angeboten.
######Benötigte Angaben:
- Austellername
- Beschreibung des Stands

## 4. Nutzungsszenario "Besucher"
 
### 4.1 Allgemeine Beschreibung
Besucher sollen über anstehende Messen Hallenpläne samt Austeller Buchungen einsehen können.

### 4.2 Benutzergruppe "Besucher": Beschreibung Persona
Besucher haben hauptsächlich den Wunsch für eine Messe eine schnelle und einfache Übersicht über die Austeller und dessen
 Standpositionen einer Messe zu erfahren, um diese dann tatsächlich auch dort auffinden zu können.

### 4.3 Interaktionsdesign  
### 4.3.1 Übersicht Interaktionen
- Übersicht / Suche zu stattfindenden Messen
- Hallen-/Austellerplan Übersicht
### 4.3.2  Übersicht / Suche zu stattfindenden Messen
#### Wireframe
![](./visitor/Besucher_Messe_Suche.png)

#### Erläuterungen
Dem Bseucher wird eine Liste mit anstehenden Messen angezeigt. Diese kann er über eine Filtermaske auf bestimmte Messeangaben und Aussteller filtern.
Wenn ein Messe Element ausgewählt wird, erscheint eine **Hallenplan Ansicht** mit insprechender Austeller Information.

### 4.3.3  Hallen- / Ausstellerplan Übersicht
#### Wireframe
![](./visitor/Besucher_Messe_Ansicht.png)

#### Erläuterungen
Es wird entsprechend der ausgewählten Messeveranstaltung der Hallenplan mit bereits existierenden Anmeldungen, eine Legende dazu und die entsprechenden Austeller mit Platz-Nr. angezeigt.
*Sollte bei der Suche ein Austeller ausgewählt sein*, wird dieser im Hallenplan besonders markiert und in der Austellerübersicht hervorgehoben.
 