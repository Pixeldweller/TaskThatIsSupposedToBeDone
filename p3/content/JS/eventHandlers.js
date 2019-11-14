//------------------------------------------------------------------------------
//Demonstrator evs/tco/tmg
//------------------------------------------------------------------------------
// rev. 0, 21.11.2018, Bm
//------------------------------------------------------------------------------
// hier zur Vereinfachung (!) die Klassen in einer Datei

'use strict'

function objectifyForm(formArray) {//serialize data function

    var returnArray = {};
    for (var i = 0; i < formArray.length; i++) {
        returnArray[formArray[i]['name']] = formArray[i]['value'];
    }
    return returnArray;
}

class Custom_cl {
//------------------------------------------------------------------------------

    constructor(el_spl, template_spl) {
        this.el_s = el_spl;
        this.template_s = template_spl;
        this.configHandleEvent_p();
    }

    render_px() {
        // Daten anfordern
        let path_s = "/custom/";
        let requester_o = new APPUTIL.Requester_cl();
        requester_o.request_px(path_s,
            function (responseText_spl) {
                let data_o = JSON.parse(responseText_spl);
                this.doRender_p(data_o);
            }.bind(this),
            function (responseText_spl) {
                alert("List - render failed");
            }
        );
    }

    doRender_p(data_opl) {
        let markup_s = APPUTIL.tm_o.execute_px(this.template_s, data_opl);
        let el_o = document.querySelector(this.el_s);
        if (el_o != null) {
            el_o.innerHTML = markup_s;
        }
    }

    configHandleEvent_p() {
        let el_o = document.querySelector(this.el_s);
        if (el_o != null) {
            el_o.addEventListener("click", this.handleEvent_p);
        }
    }

    handleEvent_p(event_opl) {
        if (event_opl.target.tagName.toUpperCase() == "TD") {
            let elx_o = document.querySelector(".clSelected");
            if (elx_o != null) {
                elx_o.classList.remove("clSelected");
            }
            event_opl.target.parentNode.classList.add("clSelected");
            event_opl.preventDefault();
        } else if (event_opl.target.id == "idShowListEntry") {
            let elx_o = document.querySelector(".clSelected");
            if (elx_o == null) {
                alert("Bitte zuerst einen Eintrag auswählen!");
            } else {
                APPUTIL.es_o.publish_px("app.cmd", ["detail", elx_o.id]);
            }
            event_opl.preventDefault();
        }
    }
}

//------------------------------------------------------------------------------
class Projects_cl {
//------------------------------------------------------------------------------

    constructor(el_spl, template_spl) {
        this.el_s = el_spl;
        this.template_s = template_spl;
        this.configHandleEvent_p();
    }

    render_px() {
        // Daten anfordern
        let path_s = "/projekt/";
        let requester_o = new APPUTIL.Requester_cl();
        requester_o.request_px(path_s,
            function (responseText_spl) {
                let data_o = JSON.parse(responseText_spl);
                this.doRender_p(data_o);
            }.bind(this),
            function (responseText_spl) {
                alert("List - render failed");
            }
        );
    }

    doRender_p(data_opl) {
        let markup_s = APPUTIL.tm_o.execute_px(this.template_s, data_opl);
        let el_o = document.querySelector(this.el_s);
        if (el_o != null) {
            el_o.innerHTML = markup_s;
        }
    }

    configHandleEvent_p() {
        let el_o = document.querySelector(this.el_s);
        if (el_o != null) {
            el_o.addEventListener("click", this.handleEvent_p);
        }
    }

    handleEvent_p(event_opl) {
        if (event_opl.target.tagName.toUpperCase() == "TD") {
            let elx_o = document.querySelector(".clSelected");
            if (elx_o != null) {
                elx_o.classList.remove("clSelected");
            }
            event_opl.target.parentNode.classList.add("clSelected");
            event_opl.preventDefault();
        } else if (event_opl.target.id == "idShowListEntry") {
            let elx_o = document.querySelector(".clSelected");
            if (elx_o == null) {
                alert("Bitte zuerst einen Eintrag auswählen!");
            } else {
                APPUTIL.es_o.publish_px("app.cmd", ["edit","projekt", elx_o.id]);
            }
            event_opl.preventDefault();
        }
    }
}

//------------------------------------------------------------------------------
class ProjectDetailView_cl {
//------------------------------------------------------------------------------

    constructor(el_spl, template_spl) {
        this.el_s = el_spl;
        this.template_s = template_spl;
    }

    render_px(id_spl) {
        // Daten anfordern
        let path_s = "/projekt/" + id_spl;
        let requester_o = new APPUTIL.Requester_cl();
        requester_o.request_px(path_s,
            function (responseText_spl) {
                let data_o = JSON.parse(responseText_spl);
                this.doRender_p(data_o);
            }.bind(this),
            function (responseText_spl) {
                alert("Detail - render failed");
            }
        );
    }

    doRender_p(data_opl) {
        let markup_s = APPUTIL.tm_o.execute_px(this.template_s, data_opl);
        let el_o = document.querySelector(this.el_s);
        if (el_o != null) {
            el_o.innerHTML = markup_s;
            this.configHandleEvent_p();
        }
    }

    configHandleEvent_p() {
        let el_o = document.querySelector("form");
        if (el_o != null) {
            el_o.addEventListener("click", this.handleEvent_p);
        }
    }

    handleEvent_p(event_opl) {
        if (event_opl.target.id == "idBack") {
            APPUTIL.es_o.publish_px("app.cmd", ["projects", null]);
            event_opl.preventDefault();
        } else if (event_opl.target.id == "idConfirm") {
            let form = document.querySelector('#project_form');
            let formData = new FormData(form);
            let requester_o = new APPUTIL.Requester_cl();
            requester_o.put_px("/projekt/", formData, function () {
                APPUTIL.es_o.publish_px("app.cmd", ["projects", null]);
            }, function () {
                alert("FAIL.");
            });

            event_opl.preventDefault();
        }
    }
}


