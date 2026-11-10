"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const samples = [
    {
        path: "scorm/1.2/content/runtime.js",
        api: "API",
        commitError: "101",
        methods: ["LMSInitialize", "LMSSetValue", "LMSCommit", "LMSFinish", "LMSGetLastError"],
        expected: [
            ["cmi.core.lesson_location", "half"],
            ["cmi.core.score.raw", "75"],
            ["cmi.core.lesson_status", "passed"],
            ["cmi.core.session_time", "0000:00:02.00"],
        ],
    },
    {
        path: "scorm/2004.4/course/first/runtime.js",
        api: "API_1484_11",
        commitError: "391",
        methods: ["Initialize", "SetValue", "Commit", "Terminate", "GetLastError"],
        expected: [
            ["cmi.location", "fractions"],
            ["cmi.score.scaled", "0.75"],
            ["cmi.success_status", "passed"],
            ["cmi.completion_status", "completed"],
            ["cmi.session_time", "PT2S"],
        ],
    },
];

function boot(sample, discoverFrom) {
    const [initialize, set, commit, close, lastError] = sample.methods;
    const state = { initialized: false, closed: false, rejectCommit: false };
    const calls = [];
    const recorder = {
        [initialize](argument) {
            assert.equal(argument, "");
            assert.equal(state.initialized, false);
            state.initialized = true;
            calls.push(["initialize"]);
            return "true";
        },
        [set](key, value) {
            assert.ok(state.initialized && !state.closed);
            assert.equal(typeof value, "string");
            calls.push(["set", key, value]);
            return "true";
        },
        [commit](argument) {
            assert.equal(argument, "");
            assert.ok(state.initialized && !state.closed);
            calls.push(["commit"]);
            return state.rejectCommit ? "false" : "true";
        },
        [close](argument) {
            assert.equal(argument, "");
            assert.ok(state.initialized && !state.closed);
            state.closed = true;
            calls.push(["close"]);
            return "true";
        },
        [lastError]() {
            return state.rejectCommit ? sample.commitError : "0";
        },
    };
    const apiWindow = { [sample.api]: recorder };
    apiWindow.parent = apiWindow;
    const window = { opener: null };
    window.parent = window;
    if (discoverFrom === "parent") {
        window.parent = apiWindow;
    }
    if (discoverFrom === "opener") {
        window.parent = new Proxy({}, { get() { throw new Error("cross origin"); } });
        window.opener = apiWindow;
    }
    const status = { textContent: "" };
    const button = { disabled: true, clickHandler: null, addEventListener(type, handler) {
        assert.equal(type, "click");
        this.clickHandler = handler;
    } };
    const document = { getElementById: (id) => id === "finish" ? button : status };
    const source = fs.readFileSync(path.join(__dirname, sample.path), "utf8");
    vm.runInNewContext(source, { window, document }, { timeout: 1000 });
    return { state, calls, button, status };
}

for (const sample of samples) {
    const expected = sample.expected.map(([key, value]) => ["set", key, value]);
    for (const discovery of ["parent", "opener"]) {
        const session = boot(sample, discovery);
        assert.equal(session.button.disabled, false);
        session.button.clickHandler();
        assert.deepEqual(session.calls, [["initialize"], ...expected, ["commit"], ["close"]]);
        assert.equal(session.status.textContent, "Completion saved.");
        assert.equal(session.button.disabled, true);
    }

    const noRuntime = boot(sample, "none");
    assert.equal(noRuntime.button.disabled, true);
    assert.equal(noRuntime.calls.length, 0);
    assert.match(noRuntime.status.textContent, /needs a SCORM/);

    const retry = boot(sample, "parent");
    retry.state.rejectCommit = true;
    retry.button.clickHandler();
    assert.equal(retry.state.closed, false);
    assert.equal(retry.status.textContent, "Save failed. Retry. Code " + sample.commitError);
    retry.state.rejectCommit = false;
    retry.button.clickHandler();
    assert.deepEqual(retry.calls, [["initialize"], ...expected, ["commit"], ...expected, ["commit"], ["close"]]);
    assert.equal(retry.status.textContent, "Completion saved.");
    console.log(sample.api + " fixture passed parent discovery, opener fallback, no-runtime handling and failed-commit retry.");
}
