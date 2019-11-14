//------------------------------------------------------------------------------
// Einfache Anforderungen per Fetch-API
//------------------------------------------------------------------------------
// rev. 1, 21.11.2018, Bm
//------------------------------------------------------------------------------

'use strict'

if (APPUTIL == undefined) {
    var APPUTIL = {};
}

APPUTIL.Requester_cl = class {
    constructor() {
    }

    request_px(path_spl, success_ppl, fail_ppl) {
        if (path_spl == undefined) {
            console.log("error");
            return;
        }
        console.log(path_spl);
        fetch(path_spl)
            .then(function (response_opl) {
                let retVal_o = null;
                if (response_opl.ok) { // 200er-Status-Code
                    retVal_o = response_opl.text().then(function (text_spl) {
                        if (JSON.parse(text_spl)['feedback'] != undefined) {
                            document.querySelector('#feedback-box').removeAttribute("hidden");
                            document.querySelector('#feedback-box-text').innerText = JSON.parse(text_spl)['feedback'];
                            success_ppl(text_spl);
                        } else {
                            success_ppl(text_spl);
                        }
                    });
                } else {
                    retVal_o = response_opl.text().then(function (text_spl) {
                        if (JSON.parse(text_spl)['alert'] != undefined) {
                            document.querySelector('#alert-box').removeAttribute("hidden");
                            document.querySelector('#alert-text').innerText = JSON.parse(text_spl)['alert'];
                            fail_ppl(text_spl);
                        } else {
                            fail_ppl(text_spl);
                        }
                    });
                }
                return retVal_o;
            })
            .catch(function (error_opl) {
                console.log('[Requester] fetch-Problem: ', error_opl.message);
            });
    }

    put_px(path_spl, data, success_ppl, fail_ppl) {
        let options = {
            method: "PUT",
            chache: "no-cache",
            body: data
        };
        fetch(path_spl, options)
            .then(function (response_opl) {
                let retVal_o = null;
                if (response_opl.ok) { // 200er-Status-Code
                    retVal_o = response_opl.text().then(function (text_spl) {
                        if (JSON.parse(text_spl)['feedback'] != undefined) {
                            document.querySelector('#feedback-box').removeAttribute("hidden");
                            document.querySelector('#feedback-box-text').innerText = JSON.parse(text_spl)['feedback'];
                            success_ppl(text_spl);
                        } else {
                            success_ppl(text_spl);
                        }
                    });
                } else {
                    retVal_o = response_opl.text().then(function (text_spl) {
                        if (JSON.parse(text_spl)['alert'] != undefined) {
                            document.querySelector('#alert-box').removeAttribute("hidden");
                            document.querySelector('#alert-text').innerText = JSON.parse(text_spl)['alert'];
                            fail_ppl(text_spl);
                        } else {
                            fail_ppl(text_spl);
                        }
                    });
                }
                return retVal_o;
            })
            .catch(function (error_opl) {
                console.log('[Requester] fetch-Problem: ', error_opl.message);
            });
    }

    post_px(path_spl, data, success_ppl, fail_ppl) {

        let options = {
            method: "POST",
            chache: "no-cache",
            body: data
        };
        if (data === undefined) {
            options = {
                method: "POST"
            };
        }
        fetch(path_spl, options)
            .then(function (response_opl) {
                let retVal_o = null;
                if (response_opl.ok) { // 200er-Status-Code
                    retVal_o = response_opl.text().then(function (text_spl) {
                        if (JSON.parse(text_spl)['feedback'] != undefined) {
                            document.querySelector('#feedback-box').removeAttribute("hidden");
                            document.querySelector('#feedback-box-text').innerText = JSON.parse(text_spl)['feedback'];
                            success_ppl(text_spl);
                        } else {
                            success_ppl(text_spl);
                        }
                    });
                } else {
                    retVal_o = response_opl.text().then(function (text_spl) {
                        if (JSON.parse(text_spl)['alert'] != undefined) {
                            document.querySelector('#alert-box').removeAttribute("hidden");
                            document.querySelector('#alert-text').innerText = JSON.parse(text_spl)['alert'];
                            fail_ppl(text_spl);
                        } else {
                            fail_ppl(text_spl);
                        }
                    });
                }
                return retVal_o;
            })
            .catch(function (error_opl) {
                console.log('[Requester] fetch-Problem: ', error_opl.message);
            });
    }

    delete_px(path_spl, success_ppl, fail_ppl) {
        var string = "";
        let first = true;

        let options = {
            method: "DELETE",
            chache: "no-cache"
        };
        fetch(path_spl + string, options)
            .then(function (response_opl) {
                let retVal_o = null;
                if (response_opl.ok) { // 200er-Status-Code
                    retVal_o = response_opl.text().then(function (text_spl) {
                        if (JSON.parse(text_spl)['feedback'] != undefined) {
                            document.querySelector('#feedback-box').removeAttribute("hidden");
                            document.querySelector('#feedback-box-text').innerText = JSON.parse(text_spl)['feedback'];
                            success_ppl(text_spl);
                        } else {
                            success_ppl(text_spl);
                        }
                    });
                } else {
                    retVal_o = response_opl.text().then(function (text_spl) {
                        if (JSON.parse(text_spl)['alert'] != undefined) {
                            document.querySelector('#alert-box').removeAttribute("hidden");
                            document.querySelector('#alert-text').innerText = JSON.parse(text_spl)['alert'];
                            fail_ppl(text_spl);
                        } else {
                            fail_ppl(text_spl);
                        }
                    });
                }
                return retVal_o;
            }).catch(function (error_opl) {
            console.log('[Requester] fetch-Problem: ', error_opl.message);
        });
    }
}
// EOF