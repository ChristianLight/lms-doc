"use strict";

function discoverAPI(start, name) {
    let current = start;
    for (let depth = 0; current && depth < 32; depth += 1) {
        try {
            if (current[name]) {
                return current[name];
            }
            if (current === current.parent) {
                return null;
            }
            current = current.parent;
        } catch {
            return null;
        }
    }
    return null;
}

const api = discoverAPI(window, "API") || discoverAPI(window.opener, "API");
const output = document.getElementById("status");
const finish = document.getElementById("finish");

if (api && api.LMSInitialize("") === "true") {
    finish.disabled = false;
    output.textContent = "Ready.";
    finish.addEventListener("click", () => {
        const values = [
            ["cmi.core.lesson_location", "half"],
            ["cmi.core.score.raw", "75"],
            ["cmi.core.lesson_status", "passed"],
            ["cmi.core.session_time", "0000:00:02.00"],
        ];
        for (const [element, value] of values) {
            if (api.LMSSetValue(element, value) !== "true") {
                output.textContent = "Value rejected. Code " + api.LMSGetLastError();
                return;
            }
        }
        if (api.LMSCommit("") !== "true" || api.LMSFinish("") !== "true") {
            output.textContent = "Save failed. Retry. Code " + api.LMSGetLastError();
            return;
        }
        finish.disabled = true;
        output.textContent = "Completion saved.";
    });
} else {
    output.textContent = "This package needs a SCORM 1.2 launch.";
}
