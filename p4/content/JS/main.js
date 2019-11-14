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

APPUTIL.Util_cl = class {
    constructor() {
    }

    deleteBooking(booking_desc) {
        let entries = document.getElementsByClassName("day");
        for (var i = 0, row; row = entries[i]; i++) {
            if (document.getElementsByClassName('clSelected')[1].title == booking_desc) {
                let pos = document.getElementsByClassName('clSelected')[1].innerHTML.trim();
                this.updateBooking(pos.charAt(1), Number(pos.charCodeAt(0)) - 65, -1, 'Veranstalter', true);
            }
        }
    }

    updateBooking(x, y, exhibitor = undefined, desc = 'Veranstalter', deletion = false) {
        if (APPUTIL.cookie_o.getCookie('role') == 'v') {
            let selector = document.getElementById('bookingtypeSelect');
            let bookingType = selector.value;
            let eventId = selector.title;
            let planId = selector.name;
            let exhibitorid = exhibitor === undefined ? -1 : exhibitor

            let path = "booking";
            var data = new FormData();
            data.append("hallplanid", planId);
            data.append("eventid", eventId);
            data.append("exhibitorid", exhibitorid);
            data.append("x", x);
            data.append("y", y);
            data.append("desc", desc);
            data.append("bookingtype", bookingType);
            APPUTIL.es_o.publish_px("app.cmd", ['post', 'event', eventId, path, data, 'section', bookingType]);
        } else {
            if (exhibitor !== undefined) {
                let pos_field = document.getElementById('pos');
                let selector = document.getElementById('dataform');
                let bookingType = 4; // Ausstellerbuchung
                if (deletion) {
                    bookingType = -1;
                }
                let eventId = selector.title;
                let planId = selector.name;
                let exhibitorid = exhibitor

                let path = "booking";
                var data = new FormData();
                data.append("hallplanid", planId);
                data.append("eventid", eventId);
                data.append("exhibitorid", exhibitorid);
                if (!deletion) {
                    data.append("x", pos_field.name);
                    data.append("y", pos_field.title);
                } else {
                    data.append("x", x);
                    data.append("y", y);
                }
                data.append("desc", desc);
                data.append("bookingtype", bookingType);
                APPUTIL.es_o.publish_px("app.cmd", ['post', 'event', eventId, path, data, 'section', bookingType]);
            } else {
                let pos_field = document.getElementById('pos');
                let focused_tag = document.activeElement;
                let tmp = focused_tag.innerHTML.trim();
                if (tmp !== '' && tmp !== 'WC' && tmp.length == 2) {
                    pos_field.value = tmp;
                    pos_field.title = Number(pos.value.charCodeAt(0)) - 65;
                    pos_field.name = pos_field.value.charAt(1);
                    document.getElementById('buchenButton').disabled = false;
                } else {
                    document.getElementById('buchenButton').disabled = true;
                }
            }
        }

    }

    hideTableRowsNotContaining(searchItem) {
        let table = document.getElementById("searchtable");
        for (var i = 1, row; row = table.rows[i]; i++) {
            let rowContainsSearchWord = false;
            for (var j = 0, col; col = row.cells[j]; j++) {
                if (col.innerHTML.includes(searchItem)) {
                    rowContainsSearchWord = true;
                }
            }
            if (rowContainsSearchWord) {
                row.style.display = "table-row";
            } else {
                if (row.classList.contains('clSelected')) {
                    row.classList.remove('clSelected');
                    document.getElementsByTagName("section")[0].style.display = 'none';
                }
                row.style.display = 'none';
            }
        }
    }

    highlightBooking(booking_desc) {
        let entries = document.getElementsByClassName("day");
        for (var i = 0, entry; entry = entries[i]; i++) {
            if (entry.classList.contains('clSelected')) {
                entry.classList.remove('clSelected');
            }
            if (entry.title == booking_desc) {
                entry.classList.add('clSelected');
            }
        }
        entries = document.getElementsByClassName("info");
        for (i = 0, entry; entry = entries[i]; i++) {
            if (entry.classList.contains('clSelected')) {
                entry.classList.remove('clSelected');
            }
            if (entry.title == booking_desc) {
                entry.classList.add('clSelected');
            }
        }
    }

    getBookingEntryValue(array, x, y, targetValue) {
        var arrayLength = array.length;
        for (var i = 0; i < arrayLength; i++) {
            if (array[i]['x'] == x && array[i]['y'] == y) {
                return array[i][targetValue];
            }
        }
        return '';
    }

    getBookingEntryTargetValue(array, fieldName, id, targetValue) {
        var arrayLength = array.length;
        for (var i = 0; i < arrayLength; i++) {
            if (array[i][fieldName] == id) {
                return array[i][targetValue];
            }
        }
        return '';
    }

    getBookingEntryTargetValues(array, fieldName, id, targetValue) {
        var arrayLength = array.length;
        var list = []
        for (var i = 0; i < arrayLength; i++) {
            if (array[i][fieldName] == id) {
                list.push(array[i][targetValue]);
            }
        }
        return list;
    }

    getNameIdIn(array, id) {
        var arrayLength = array.length;
        for (var i = 0; i < arrayLength; i++) {
            if (array[i]['id'] == id) {
                return array[i]['name'];
            }
        }
    }

    getAllNamesWithIdIn(array, ids) {
        var arrayLength = array.length;
        var result = "";
        var collected = []
        if (ids === '') {
            return '';
        }

        for (let j = 0; j < ids.length; j++) {
            for (let i = 0; i < arrayLength; i++) {
                if (array[i]['id'] == ids[j]) {
                    if (!collected.includes(array[i]['name'])) {
                        result += array[i]['name'];
                        collected.push(array[i]['name']);
                        if (i != arrayLength - 1) {
                            result += "<br>";
                        }
                    }
                }
            }
        }

        return result;
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
        this.edit_o = new Edit_cl("main ");
        this.detail_o = new Detail_cl("main");

        this.section_o = new Section_cl("section");

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
                let nav_v = [
                    ["home", "Startseite"],
                    ["events", "Eigene Messen"],
                    ["bookings", "Aussteller Buchungen"],
                    ["event_new", "Neue Messe anlegen"]
                ];
                let nav_a = [
                    ["home", "Startseite"],
                    ["events", "Finde Messeevents"],
                    ["bookings", "Eigene Buchungen"],
                    ["exhibitor_new", "Neuen Aussteller anlegen"]
                ];
                let nav_b = [
                    ["home", "Startseite"],
                    ["events", "Messeevents"],
                    ["exhibitors", "Aussteller"]
                ];

                var nav_type;
                var role = APPUTIL.cookie_o.getCookie('role');
                switch (role) {
                    case 'v':
                        nav_type = nav_v;
                        break;
                    case 'a':
                        nav_type = nav_a;
                        break;
                    case 'b':
                        nav_type = nav_b;
                        break;
                    default:
                        nav_type = nav_b;
                }

                self.sideBar_o.render_px(nav_type);
                markup_s = APPUTIL.tm_o.execute_px("home.tpl.html", null);
                el_o = document.querySelector("main");
                if (el_o != null) {
                    //el_o.innerHTML = markup_s;
                    APPUTIL.es_o.publish_px("app.cmd", ['home']);
                }
                break;

            case "app.cmd":

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
                    case "events":
                        this.list_o.render_px("event");
                        if (APPUTIL.cookie_o.getCookie('role') == 'v') {
                            setTimeout(function () {
                                APPUTIL.util_o.hideTableRowsNotContaining(APPUTIL.cookie_o.getCookie('vuser'));
                            }, 100);
                        }
                        break;
                    case "event":
                        this.list_o.render_px("event");
                        if (APPUTIL.cookie_o.getCookie('role') == 'v') {
                            setTimeout(function () {
                                APPUTIL.util_o.hideTableRowsNotContaining(APPUTIL.cookie_o.getCookie('vuser'));
                            }, 100);
                        }
                        break;
                    case "organizer":
                        this.list_o.render_px("event");
                        break;
                    case "bookings":
                        this.list_o.render_px("booking");
                        setTimeout(function () {
                            if (APPUTIL.cookie_o.getCookie('role') == 'a') {
                                APPUTIL.util_o.hideTableRowsNotContaining(APPUTIL.cookie_o.getCookie('auser'));
                            }
                        }, 100);
                        break;
                    case "event_new":
                        this.edit_o.render_px('event', -2, 'event');
                        break;
                    case "exhibitors":
                        this.list_o.render_px("exhibitor");
                        break;
                    case "exhibitor":
                        this.list_o.render_px("exhibitor");
                        break;
                    case "exhibitor_new":
                        this.edit_o.render_px('exhibitor', -2, 'exhibitor');
                        break;
                    case "section":
                        if (APPUTIL.cookie_o.getCookie('role') == 'b') {
                            document.getElementsByTagName("section")[0].style.display = 'block';
                            let main = document.getElementsByTagName("main");
                            if (data_opl[1] == 'exhibitor') {
                                let row = document.getElementsByClassName("clSelected")[0].title;
                                let ids = row.split(',');
                                document.getElementsByTagName("section")[0].innerHTML = '';
                                for (var i = 0, index; index = ids[i]; i++) {
                                    this.section_o.create_tmp_px('event', index)
                                }
                            }

                            this.section_o.render_px(data_opl[1], data_opl[2]);
                        } else {
                            if (data_opl[1] == 'booking') {
                                let row = document.getElementsByClassName("clSelected")[0].title;
                                let section = document.getElementsByTagName("section")[0];
                                let ids = row.split(',');
                                document.getElementsByTagName("section")[0].innerHTML = '';
                                for (var i = 0, index; index = ids[i]; i++) {
                                    this.detail_o.render_px('event', index, 'section')
                                }
                                setTimeout(function () {
                                    try {
                                        APPUTIL.util_o.highlightBooking(document.getElementsByClassName("clSelected")[0].id);
                                        document.getElementById("buchungTool").style.display = 'none';
                                        section.innerHTML = section.innerHTML + '<input style="clear: left;margin-left: 30px;" type="button" value="Buchung löschen" onclick="APPUTIL.util_o.deleteBooking(document.getElementsByClassName(\'clSelected\')[0].id)"></input>';
                                    } catch (e) {
                                    }
                                }, 100);

                            } else {
                                try {
                                    if (document.getElementById('dimension_x') != undefined) {
                                        data_opl[2] = data_opl[2] + '/x/' + document.getElementById('dimension_x').value + '/' + document.getElementById('dimension_y').value + '/' + document.getElementById('layout_id').value;
                                        if (data_opl[3] === 'hallplan') {
                                            data_opl[2] = data_opl[2] + '/true';
                                        }
                                    }
                                } catch (err) {
                                }
                                document.getElementsByTagName("section")[0].style.display = 'block';
                                this.detail_o.render_px(data_opl[1], data_opl[2], 'section');
                            }

                        }
                        break;
                    case "edit":
                        this.edit_o.render_px(data_opl[1], data_opl[2], data_opl[3]);
                        break;
                    case "detail":
                        try {
                            if (document.getElementById('dimension_x') != undefined) {
                                data_opl[2] = data_opl[2] + '/x/' + document.getElementById('dimension_x').value + '/' + document.getElementById('dimension_y').value + '/' + document.getElementById('layout_id').value;
                            }
                        } catch (err) {
                        }

                        this.detail_o.render_px(data_opl[1], data_opl[2]);
                        break;
                    case "idBack":
                        this.list_o.render_px(this.list_o.last_object_type);
                        break;
                    case "post":
                        let requester_o = new APPUTIL.Requester_cl();
                        requester_o.post_px("/" + data_opl[3], data_opl[4], function (response) {
                        }, function (resp) {
                            console.log(resp);
                        });
                        this.detail_o.render_px(data_opl[1], data_opl[2], data_opl[5]);
                        setTimeout(function () {
                            try {
                                document.querySelector('#bookingtypeSelect [value="' + data_opl[6] + '"]').selected = true;
                            } catch (e) {
                            }
                        }, 100);
                        break;
                }
                break;
            case "login.cmd":
                if (APPUTIL.cookie_o.getCookie('role') == 'b') {
                    APPUTIL.cookie_o.setCookie('buser', 'BESUCHER', 2)
                } else if (APPUTIL.cookie_o.getCookie('role') == 'v') {
                    APPUTIL.cookie_o.setCookie('vuser', prompt('Geben Sie den Veranstalternamen an!'), 2)
                } else {
                    APPUTIL.cookie_o.setCookie('auser', prompt('Geben Sie den Ausstellernamen an!'), 2)
                }
                location.reload();
                break;
        }
    }


}

window.onload = function () {
    APPUTIL.es_o = new APPUTIL.EventService_cl();
    APPUTIL.cookie_o = new APPUTIL.Cookie_cl();
    APPUTIL.util_o = new APPUTIL.Util_cl();
    var app_o = new Application_cl();
    APPUTIL.createTemplateManager_px();
}
