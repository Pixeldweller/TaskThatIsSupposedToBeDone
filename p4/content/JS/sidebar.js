//------------------------------------------------------------------------------
class SideBar_cl {
//------------------------------------------------------------------------------

    constructor(el_spl, template_spl) {
        this.el_s = el_spl;
        this.template_s = template_spl;
        this.configHandleEvent_p();
    }

    render_px(data_opl) {
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
        let cmd_s = event_opl.target.dataset.action;
        APPUTIL.es_o.publish_px("app.cmd", [cmd_s, null]);
    }
}
