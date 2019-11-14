//------------------------------------------------------------------------------
class List_cl {
//------------------------------------------------------------------------------

    constructor(el_spl) {
        this.el_s = el_spl;
        this.last_object_type = "";
    }

    render_px(object_type, template_target = undefined) {
        // Daten anfordern
        let path_s = "/" + object_type + "";
        let requester_o = new APPUTIL.Requester_cl();
        requester_o.request_px(path_s,
            function (responseText_spl) {
                let data_o = JSON.parse(responseText_spl);
                if (template_target === undefined) {
                    this.doRender_p(object_type, data_o);
                } else {
                    this.doRender_p(template_target, data_o);
                }
            }.bind(this),
            function (responseText_spl) {
                alert("Detail - render failed");
            }
        );
    }

    doRender_p(object_type, data_opl) {
        this.last_object_type = object_type;
        let markup_s = APPUTIL.tm_o.execute_px(object_type + "list.tpl.html", data_opl);
        let el_o = document.querySelector(this.el_s);
        if (el_o != null) {
            el_o.innerHTML = markup_s;
            window.scrollTo(0, 0);
            this.configHandleEvent_p(object_type);
        }
    }

    configHandleEvent_p(object_type) {
        let headElements = document.querySelectorAll('thead.table-head tr th');
        for (let index = 0; index < headElements.length; index++) {
            if (headElements[index].classList.contains('clickable')) {
                let element = headElements[index];
                element.dataset.target = index;
                element.insertAdjacentHTML('beforeend', " &#8645;");
                element.addEventListener('click', this.handleEventSort);
            }
        }


        let el_o = document.querySelector(this.el_s);
        el_o.title = object_type;
        if (el_o != null) {
            el_o.addEventListener("click", this.handleEvent_p);
        }
    }

    handleEvent_p(event_opl) {
        let el_o = document.querySelector("main");
        if (event_opl.target.tagName.toUpperCase() == "TD" && event_opl.target.parentNode.id != '-1') {
            let elx_o = document.querySelector(".clSelected");
            if (elx_o != null) {
                elx_o.classList.remove("clSelected");
            }
            if (event_opl.target.parentNode.classList.contains("clSelected")) {
                event_opl.target.parentNode.classList.remove("clSelected");
            } else {
                event_opl.target.parentNode.classList.add("clSelected");
                APPUTIL.es_o.publish_px("app.cmd", ["section", el_o.title, event_opl.target.parentNode.id]);
            }

            elx_o = document.querySelector(".clSelected");
            let swap_buttons = document.querySelectorAll(".needsSelection");
            for (var i = 0; i < swap_buttons.length; i++) {
                swap_buttons[i].disabled = elx_o == null;
            }
            event_opl.preventDefault();
        } else {
            let elx_o = document.querySelector(".clSelected");
            if (event_opl.target.value == "listView" && elx_o == null && !event_opl.target.id.startsWith('idAdd')) {
                alert("Bitte zuerst einen Eintrag auswählen!");
                event_opl.preventDefault();
            } else if (event_opl.target.id == "idAddEntry") {
                APPUTIL.es_o.publish_px("app.cmd", ["edit", el_o.title, -1]);
                event_opl.preventDefault();
            } else {
                let target_path = el_o.title;
                if (el_o.title == "kategorie") {
                    if (elx_o.id.startsWith("bug")) {
                        target_path = "katfehler";
                        elx_o.id = elx_o.id.replace("bug-", "");
                    } else {
                        target_path = "katursache";
                        elx_o.id = elx_o.id.replace("cause-", "");
                    }
                }

                if (event_opl.target.id == "idEditEntry") {
                    APPUTIL.es_o.publish_px("app.cmd", ["edit", el_o.title, elx_o.id, target_path]);
                    event_opl.preventDefault();
                } else if (event_opl.target.id == "idShowListEntry") {
                    APPUTIL.es_o.publish_px("app.cmd", ["detail", el_o.title, elx_o.id]);
                    event_opl.preventDefault();
                } else if (event_opl.target.id == "idDeleteEntry") {
                    if (confirm("Wollen Sie wirklich den ausgewählten Eintrag löschen?")) {
                        let requester_o = new APPUTIL.Requester_cl();
                        requester_o.delete_px("/" + target_path + "/" + elx_o.id, function () {
                            APPUTIL.es_o.publish_px("app.cmd", [el_o.title, null]);
                        }, function () {
                            alert("Delete Event Error.");
                        });
                    }
                }
            }
        }
    }

    handleEventSort(event) {
        event.stopPropagation();
        event.preventDefault();

        let choice = event.srcElement.dataset.target;
        var tbody, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
        tbody = document.querySelector("tbody.table-body");
        switching = true;
        // Set the sorting direction to ascending:
        dir = "asc";
        // Make a loop that will continue until no switching has been done
        while (switching) {
            // Start by saying: no switching is done:
            switching = false;
            rows = tbody.rows;
            // Loop through all table rows
            for (i = 0; i < (rows.length - 1); i++) {
                // Start by saying there should be no switching:
                shouldSwitch = false;
                // two elements compare, current and next row
                x = rows[i].getElementsByTagName("td")[choice];
                y = rows[i + 1].getElementsByTagName("td")[choice];
                // Check if the two rows should switch place, based on the direction, asc or desc: */
                if (dir == "asc") {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == "desc") {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
            }
            if (shouldSwitch) {
                // If a switch has been marked, make the switch and mark that a switch has been done
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
                // Each time a switch is done, increase this count by 1:
                switchcount++;
            } else {
                // If no switching has been done AND the direction is "asc", set the direction to "desc" and run the while loop again.
                if (switchcount == 0 && dir == "asc") {
                    dir = "desc";
                    switching = true;
                }
            }
        }

    }
}


