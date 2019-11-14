//------------------------------------------------------------------------------
class Edit_cl {
//------------------------------------------------------------------------------

    constructor(el_spl) {
        this.el_s = el_spl;
        this.last_object_type = "";
    }

    render_px(object_type, id_spl, target_path = undefined) {
        if (id_spl === -1) {
            // Neues Objekt
            this.doRender_p(object_type, [], true, target_path);
        } else {
            // Daten anfordern
            if (target_path === undefined) {
                target_path = object_type;
            }
            let path_s = "/" + target_path + "/" + id_spl;
            let requester_o = new APPUTIL.Requester_cl();
            requester_o.request_px(path_s,
                function (responseText_spl) {
                    let data_o = JSON.parse(responseText_spl);
                    this.doRender_p(object_type, data_o, false, target_path);
                }.bind(this),
                function (responseText_spl) {
                    alert("Detail - render failed");
                }
            );
        }
    }

    doRender_p(object_type, data_opl, addNewEntry, target_path) {
        this.last_object_type = object_type;
        let markup_s = APPUTIL.tm_o.execute_px(object_type + "edit.tpl.html", data_opl);
        let el_o = document.querySelector(this.el_s);
        if (el_o != null) {
            el_o.innerHTML = markup_s;
            this.configHandleEvent_p(object_type, addNewEntry, target_path);
        }
    }

    // Nur fuer Fehler Edit
    doRender_template_p(object_type, data_opl, addNewEntry, template_path) {
        this.last_object_type = object_type;
        let markup_s = APPUTIL.tm_o.execute_px(template_path + "edit.tpl.html", data_opl);
        let el_o = document.querySelector(this.el_s);
        if (el_o != null) {
            el_o.innerHTML = markup_s;
            this.configHandleEvent_p(object_type, addNewEntry, object_type);
        }
    }

    configHandleEvent_p(object_type, addNewEntry, target_path) {
        let main_o = document.querySelector("main");
        main_o.title = object_type;
        main_o.target = target_path;
        let form_o = document.querySelector("form");
        if (form_o != null) {
            form_o.name = addNewEntry ? "new" : "edit";
            if (main_o != null) {
                main_o.addEventListener("click", this.handleEvent_p);
            }
        }
    }

    handleEvent_p(event_opl) {
        let el_o = document.querySelector("main");

        if (event_opl.target.id == "idBack") {
            APPUTIL.es_o.publish_px("app.cmd", [el_o.title, null]);
            event_opl.preventDefault();
        } else if (event_opl.target.id == "idEdit") {
            let form = document.querySelector('#dataform');
            let target_path = el_o.title;
            if (el_o.title === "mitarbeiter" || el_o.title === "kategorie") {
                if (el_o.title === "mitarbeiter") {
                    if (form.roleid.value == "0") {
                        target_path = "swentwickler";
                    } else if (form.roleid.value == "1") {
                        target_path = "qsmitarbeiter";
                    }
                } else if (el_o.title === "kategorie") {
                    target_path = el_o.target;
                }
            }

            let requiredInputNotFilled = false;
            for (let index = 0; index < form.length; index++) {
                if (!form[index].disabled && [index].required && form[index].value === "") {
                    document.querySelector('#alert-box').removeAttribute("hidden");
                    document.querySelector('#alert-text').innerText = "Es sind nicht alle Felder ausgefüllt.";
                    requiredInputNotFilled = true;
                    break;
                }
            }
            if (!requiredInputNotFilled) {
                let formData = new FormData(form);
                let requester_o = new APPUTIL.Requester_cl();

                if (form.name !== "new") {
                    requester_o.put_px("/" + target_path + "/", formData, function () {
                        if (el_o.title != 'kategorie') {
                            APPUTIL.es_o.publish_px("app.cmd", ["detail", el_o.title, form.id.value, 'saved']);
                        } else {
                            APPUTIL.es_o.publish_px("app.cmd", [el_o.title, undefined, undefined, 'saved']);
                        }
                    }, function () {
                        alert("Edit Event Error.");
                    });
                } else {
                    form.removeChild(form.id);
                    if (form.roleid != undefined) {
                        form.removeChild(form.roleid);
                    }
                    formData = new FormData(form);
                    requester_o.post_px("/" + target_path + "/", formData, function (response) {
                        if (el_o.title != 'kategorie') {
                            APPUTIL.es_o.publish_px("app.cmd", ["detail", el_o.title, JSON.parse(response)["id"], 'saved']);
                        } else {
                            APPUTIL.es_o.publish_px("app.cmd", [el_o.title, undefined, undefined, 'saved']);
                        }
                    }, function () {
                        alert("Edit Event Error.");
                    });
                }
            }
            event_opl.preventDefault();
        }
    }
}


