//------------------------------------------------------------------------------
//Demonstrator evs/tco/tmg
//------------------------------------------------------------------------------
// rev. 0, 21.11.2018, Bm
//------------------------------------------------------------------------------
// hier zur Vereinfachung (!) die Klassen in einer Datei

'use strict'


class Bug_cl {
//------------------------------------------------------------------------------

    constructor(el_spl, template_spl) {
        this.el_s = el_spl;
        this.template_s = template_spl;
        this.configHandleEvent_p();
    }

    configHandleEvent_p() {
        let el_o = document.querySelector(this.el_s);
        if (el_o != null) {
            el_o.addEventListener("click", this.handleEvent_p);
        }
    }

    handleEvent_p(event_opl) {
        let elx_o = document.querySelector(".clSelected");
        if (event_opl.target.id == "idPrüfung" && elx_o != null) {
            APPUTIL.es_o.publish_px("app.cmd", ["approval", elx_o.id]);
            event_opl.preventDefault();
        } else {
            let id_o = document.querySelector("#id");
            let requester_o = new APPUTIL.Requester_cl();
            if (event_opl.target.id == "idFreigeben") {
                requester_o.put_px("/fehler/?id="+id_o.value+"&approval=1", [], function () {
                    APPUTIL.es_o.publish_px("app.cmd", ["fehler", null]);
                }, function () {
                    alert("Freigabe Error.");
                });
            } else if (event_opl.target.id == "idAblehnen") {
                requester_o.put_px("/fehler/?id="+id_o.value+"&approval=0", [], function () {
                    APPUTIL.es_o.publish_px("app.cmd", ["fehler", null]);
                }, function () {
                    alert("Freigabe Error.");
                });
            }
        }
    }
}

