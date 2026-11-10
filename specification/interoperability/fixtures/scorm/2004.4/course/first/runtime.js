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

const api = discoverAPI(window, "API_1484_11") || discoverAPI(window.opener, "API_1484_11");
const output = document.getElementById("status");
const finish = document.getElementById("finish");

if (api && api.Initialize("") === "true") {
    finish.disabled = false;
    output.textContent = "Ready.";
    finish.addEventListener("click", () => {
        const values = [
            ["cmi.location", "fractions"],
            ["cmi.score.scaled", "0.75"],
            ["cmi.success_status", "passed"],
            ["cmi.completion_status", "completed"],
            ["cmi.session_time", "PT2S"],
        ];
        for (const [element, value] of values) {
            if (api.SetValue(element, value) !== "true") {
                output.textContent = "Value rejected. Code " + api.GetLastError();
                return;
            }
        }
        if (api.Commit("") !== "true" || api.Terminate("") !== "true") {
            output.textContent = "Save failed. Retry. Code " + api.GetLastError();
            return;
        }
        finish.disabled = true;
        output.textContent = "Completion saved.";
    });
} else {
    output.textContent = "This package needs a SCORM 2004 launch.";
}
