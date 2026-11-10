# Synthetic interoperability fixtures

These files are original curriculum and protocol examples. They contain no institutional student data or upstream implementation. From this directory run Python 3.11 or newer.

```sh
python3 verify-fixtures.py
python3 verify-fixtures.py --output /tmp/lms-interop-fixtures
node verify-runtime-fixtures.js
```

The first command checks file structure, packages and reopens archive bytes in memory, verifies deterministic assembly and prints expected outcomes. The second also writes the five checked archives. The Node verifier runs the two SCO scripts with isolated fake adapters and verifies the exact ordered calls, parent and opener discovery, missing adapter behavior, and commit failure retry. This is a reference fixture verifier for known inputs. Production ingestion still requires the validation and isolation defined in the parent chapters.

| Archive | Intended proof |
| --- | --- |
| `fraction-course.tar.gz` | Ordered pointer-based OLX tree, shared media, one unresolved link, published and private draft separation, numeric tolerance |
| `fraction-legacy-library.tar.gz` | Scoped library reference and reusable editable question |
| `fraction-versioned-library.zip` | Version 1 envelope, draft and published versions, collection/container references, different bytes under the same version-local asset path |
| `fraction-scorm-12.zip` | One SCO, inherited path, runtime initialization, bookmark, score, completion, duration, commit and finish |
| `fraction-scorm-2004-4.zip` | Shared resource under two activity occurrences, XML base and resource dependency, separate completion and success, typed score and duration |

The SCORM examples have learner-facing HTML and JavaScript that call the correct browser APIs. Use a player adapter to test those calls. The package verifier checks paths, manifest tree and referenced files. It does not ship the official edition XSDs, run browser integration, or establish ADL conformance. The runtime chapter also includes minimal independent JavaScript probe snippets for its respective editions.
