//------------------------------------------------------------------------------
class Detail_cl {
//------------------------------------------------------------------------------

    constructor(el_spl) {
        this.el_s = el_spl;
        this.last_object_type = "";
    }

    render_px(object_type, id_spl, tagToReplace=undefined) {
        // Daten anfordern
        let path_s = "/" + object_type + "/" + id_spl;
        let requester_o = new APPUTIL.Requester_cl();
        requester_o.request_px(path_s,
            function (responseText_spl) {
                let data_o = JSON.parse(responseText_spl);
                this.doRender_p(object_type, data_o, id_spl,tagToReplace);
            }.bind(this),
            function (responseText_spl) {
                alert("Detail - render failed");
            }
        );
    }

    doRender_p(object_type, data_opl,id_spl=undefined,tagToReplace='main') {
        this.last_object_type = object_type;
        let markup_s = APPUTIL.tm_o.execute_px(object_type + "detail.tpl.html", data_opl);
        this.el_s = tagToReplace;
        let el_o = document.querySelector(this.el_s);
        let main_o = document.querySelector(tagToReplace);
        //main_o.title = "ID "+id_spl;
        if (el_o != null) {
            el_o.innerHTML = markup_s;
            this.configHandleEvent_p();
        }
    }

    configHandleEvent_p() {
        let el_o = document.querySelector("main");
        if (el_o != null) {
            el_o.addEventListener("click", this.handleEvent_p);
        }
    }

    handleEvent_p(event_opl) {
        let el_o = document.querySelector("main");
        if (event_opl.target.id == "idDetailBack") {
            APPUTIL.es_o.publish_px("app.cmd", [el_o.title, null]);
            event_opl.preventDefault();
        } else if (event_opl.target.id == "idDetailEdit") {
            let id_val = document.querySelector("#id");
            APPUTIL.es_o.publish_px("app.cmd", ["edit", el_o.title, id_val.value]);
            event_opl.preventDefault();
        } else if (event_opl.target.id == "idDelete") {
            if (confirm("Wollen Sie wirklich den ausgewählten Eintrag löschen?")) {
                let form = document.querySelector('#dataform');
                let requester_o = new APPUTIL.Requester_cl();
                requester_o.delete_px("/" + el_o.title + "/" + form.id.value, function () {
                    APPUTIL.es_o.publish_px("app.cmd", [el_o.title, null]);
                }, function () {
                    alert("Delete Event Error.");
                });
            }
        }
    }
}


