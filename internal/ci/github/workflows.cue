package github

import "github.com/cue-tmp/jsonschema-pub/exp1/githubactions"

// Each member of the workflows struct must be a valid workflow
workflows: [_]: githubactions.#Workflow
