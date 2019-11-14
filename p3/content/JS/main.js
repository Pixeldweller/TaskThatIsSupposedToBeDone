//------------------------------------------------------------------------------
//Demonstrator evs/tco/tmg
//------------------------------------------------------------------------------
// rev. 0, 21.11.2018, Bm
//------------------------------------------------------------------------------
// hier zur Vereinfachung (!) die Klassen in einer Datei

'use strict'

if (APPUTIL == undefined) {
    var APPUTIL = {};
}

APPUTIL.Cookie_cl = class {
    constructor() {
    }

    setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }

    getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
}

class Application_cl {

    constructor() {
        // Registrieren zum Empfang von Nachrichten
        APPUTIL.es_o.subscribe_px(this, "templates.loaded");
        APPUTIL.es_o.subscribe_px(this, "templates.failed");
        APPUTIL.es_o.subscribe_px(this, "app.cmd");
        APPUTIL.es_o.subscribe_px(this, "login.cmd");

        this.cookie_o = APPUTIL.cookie_o;

        this.sideBar_o = new SideBar_cl("aside", "sidebar.tpl.html");
        this.list_o = new List_cl("main");
        this.edit_o = new Edit_cl("main");
        this.detail_o = new Detail_cl("main");

        this.bug_o = new Bug_cl('main');
    }

    notify_px(self, message_spl, data_opl) {
        console.log(data_opl);
        switch (message_spl) {
            case "templates.failed":
                alert("Vorlagen konnten nicht geladen werden.");
                break;
            case "templates.loaded":
                // Templates stehen zur Verfügung, Bereiche mit Inhalten füllen
                // hier zur Vereinfachung direkt
                let markup_s;
                let el_o;
                markup_s = APPUTIL.tm_o.execute_px("header.tpl.html", null);
                el_o = document.querySelector("header");
                if (el_o != null) {
                    el_o.innerHTML = markup_s;
                }
                let nav_a = [
                    ["home", "Startseite"],
                    ["fehler", "Bearbeitung Fehlerdaten"],
                    ["projekt", "Pflege Projekte"],
                    ["komponente", "Pflege Komponenten"],
                    ["mitarbeiter", "Pflege Daten Mitarbeiter"],
                    ["kategorie", "Pflege Kategorien"],
                    ["report-pro", "Auswertung Projekte/Fehler"],
                    ["report-kat", "Auswertung Kategorien/Fehler"]
                ];
                self.sideBar_o.render_px(nav_a);
                markup_s = APPUTIL.tm_o.execute_px("home.tpl.html", null);
                el_o = document.querySelector("main");
                if (el_o != null) {
                    //el_o.innerHTML = markup_s;
                    APPUTIL.es_o.publish_px("app.cmd", ['home']);
                }
                break;

            case "app.cmd":

                // CHECK FOR LOGIN
                var username = this.cookie_o.getCookie("username");
                if (username === "" || username === undefined) {
                    document.querySelector('#currentLogin').setAttribute('hidden', '');
                    document.querySelector('aside').classList.add('disabled');
                    let markup_s = APPUTIL.tm_o.execute_px("login.tpl.html", []);
                    let el_o = document.querySelector("main");
                    if (el_o != null) {
                        el_o.innerHTML = markup_s;
                        let loginInput = document.querySelector("#login");
                        loginInput.addEventListener("click", function () {
                            APPUTIL.es_o.publish_px("login.cmd", [document.querySelector("#username").value]);
                        });
                    }
                    break;
                } else {
                    document.querySelector('#currentLogin').removeAttribute('hidden');
                    document.querySelector('#currentUser').innerHTML = this.cookie_o.getCookie('username') + ' (' + this.cookie_o.getCookie('role').substring(0, 2).toUpperCase() + ')';
                    document.querySelector('aside').classList.remove('disabled');
                }

                let form = document.querySelector("form");
                if (form != null && data_opl[3] !== 'saved') {
                    let doConfirm = false;
                    for (let index = 0; index < form.length; index++) {
                        if (doConfirm === true) {
                            break;
                        }
                        let element = form[index];
                        if (element.defaultValue === undefined || element.type === "hidden" || element.disabled) {
                            continue;
                        }
                        if (element.defaultValue !== element.value) {
                            doConfirm = true;
                        }
                    }
                    if (doConfirm === true) {
                        if (!confirm("Ihre Änderungen wurden noch nicht gespeichert.\nWollen Sie die Seite wirklich wechseln?")) {
                            break;
                        }
                    }
                }

                switch (data_opl[0]) {
                    case "home":
                        let markup_s = APPUTIL.tm_o.execute_px("home.tpl.html", null);
                        let el_o = document.querySelector("main");
                        if (el_o != null) {
                            el_o.innerHTML = markup_s;
                        }
                        break;
                    case "fehler":
                        this.list_o.render_px("fehler");
                        break;
                    case "fehler_type":
                        switch (data_opl[1]) {
                            case "-1":
                                this.list_o.render_px("fehler");
                                break;
                            case "0":
                                this.list_o.render_px("fehler/?type=erfasst", "fehler");
                                break;
                            case "1":
                                this.list_o.render_px("fehler/?type=behoben", "fehler");
                                break;
                        }
                        break;
                    case "projekt":
                        this.list_o.render_px("projekt");
                        break;
                    case "mitarbeiter":
                        this.list_o.render_px("mitarbeiter");
                        break;
                    case "mitarbeiter_type":
                        switch (data_opl[1]) {
                            case "-1":
                                this.list_o.render_px("mitarbeiter");
                                break;
                            case "0":
                                this.list_o.render_px("swentwickler", "mitarbeiter");
                                break;
                            case "1":
                                this.list_o.render_px("qsmitarbeiter", "mitarbeiter");
                                break;
                        }
                        break;
                    case "kategorie":
                        this.list_o.render_px("kategorie");
                        break;
                    case "komponente_type":
                        if (data_opl[1] == "-1") {
                            this.list_o.render_px("komponente");
                        } else {
                            this.list_o.render_px("projektkomponenten/" + data_opl[1], "komponente");
                        }

                        break;
                    case "komponente":
                        this.list_o.render_px("komponente");
                        break;
                    case "edit":
                        if (data_opl[1] == 'komponente' && data_opl[2] == "-1") {
                            let requester_ox = new APPUTIL.Requester_cl();
                            requester_ox.request_px("/projekt/",
                                function (responseText_spl) {
                                    let projects_o = JSON.parse(responseText_spl);
                                    let data_o = {'projects': projects_o};
                                    this.edit_o.doRender_p('komponente', data_o, true, 'komponente');
                                }.bind(this),
                                function (responseText_spl) {
                                    alert("New Component - render failed");
                                }
                            );

                        } else if (data_opl[1] == 'fehler') {
                            if (data_opl[2] == "-1") {
                                let requester_ox = new APPUTIL.Requester_cl();
                                requester_ox.request_px("/fehler/-1",
                                    function (responseText_spl) {
                                        let data_o = JSON.parse(responseText_spl);
                                        this.edit_o.doRender_template_p('fehler', data_o, true, 'fehler' + this.cookie_o.getCookie('role'));
                                    }.bind(this),
                                    function (responseText_spl) {
                                        alert("New Bug - render failed");
                                    }
                                );
                            } else {
                                let requester_ox = new APPUTIL.Requester_cl();
                                requester_ox.request_px("/fehler/" + data_opl[2],
                                    function (responseText_spl) {
                                        let data_o = JSON.parse(responseText_spl);
                                        this.edit_o.doRender_template_p('fehler', data_o, false, 'fehler' + this.cookie_o.getCookie('role'));
                                    }.bind(this),
                                    function (responseText_spl) {
                                        alert("New Bug - render failed");
                                    }
                                );
                            }

                        } else {
                            this.edit_o.render_px(data_opl[1], data_opl[2], data_opl[3]);
                        }

                        break;
                    case "detail":
                        this.detail_o.render_px(data_opl[1], data_opl[2]);
                        break;
                    case "approval":
                        let requester_ox = new APPUTIL.Requester_cl();
                        requester_ox.request_px("/fehler/" + data_opl[1],
                            function (responseText_spl) {
                                let data_o = JSON.parse(responseText_spl);
                                this.edit_o.doRender_template_p('fehler', data_o, false, 'fehlerprüfung');
                            }.bind(this),
                            function (responseText_spl) {
                                alert("Bug approval - render failed");
                            }
                        );
                        break;
                    case "idBack":
                        this.list_o.render_px(this.list_o.last_object_type);
                        break;
                    case "report-pro":
                        this.list_o.render_px("prolist");
                        break;
                    case "report-kat":
                        this.list_o.render_px("katlist");
                        break;
                }
                break;
            case 'login.cmd':
                if (data_opl[0] === undefined) {
                    this.cookie_o.setCookie("username", "", -1);
                    this.cookie_o.setCookie("role", "", -1);
                }
                let input = data_opl[0];
                let requester_ox = new APPUTIL.Requester_cl();
                requester_ox.request_px("/mitarbeiter/",
                    function (responseText_spl) {
                        let empl_o = JSON.parse(responseText_spl);
                        for (let x = 0; x < empl_o['data'].length; x++) {
                            if (empl_o['data'][x]['username'].toUpperCase() === input.toUpperCase()) {
                                this.cookie_o.setCookie("username", empl_o['data'][x]['firstname'].substring(0, 1) + '. ' + empl_o['data'][x]['lastname'], 1);
                                this.cookie_o.setCookie("role", empl_o['roles'][empl_o['data'][x]['roleId']]['internal'], 1);
                                document.querySelector('#currentUser').innerHTML = input + " (" + this.cookie_o.getCookie('role').substring(0, 2).toUpperCase() + ")"
                                document.querySelector('#currentLogin').removeAttribute("hidden");
                                break;
                            }
                        }
                        APPUTIL.es_o.publish_px("app.cmd", ['home']);
                    }.bind(this),
                    function (responseText_spl) {
                        alert("Login load - failed");
                    }
                );
                break;
        }
    }


}

window.onload = function () {
    APPUTIL.es_o = new APPUTIL.EventService_cl();
    APPUTIL.cookie_o = new APPUTIL.Cookie_cl();
    var app_o = new Application_cl();
    APPUTIL.createTemplateManager_px();
}