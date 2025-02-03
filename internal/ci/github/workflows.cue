package github

import "github.com/cue-tmp/jsonschema-pub/exp1/githubactions"

_min_py:         9
_min_py_version: "3.\(_min_py)"
_py_versions: [9, 10, 11, 12, 13]

// Each member of the workflows struct must be a valid workflow
workflows: [_]: githubactions.#Workflow
