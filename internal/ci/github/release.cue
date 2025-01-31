package github

workflows: release: {
	name: "release"
	on: {
		push: {
			branches: ["main"]
			tags: ["v[0-9]+.[0-9]+.[0-9]+"]
		}
		pull_request: null
		merge_group:  null
	}
	concurrency: {
		group:                "${{ github.workflow }}-${{ github.head_ref || github.run_id }}"
		"cancel-in-progress": true
	}
	permissions: contents: "read"
	env: {
		MINIMUM_PYTHON_VERSION: "\(_min_py_version)"
		UV_VERSION:             "0.5.15"
	}
	jobs: {
		build: {

			// This action builds distribution files for upload to PyPI
			name:      "ubuntu / \(_min_py_version) / build"
			"runs-on": "ubuntu-latest"
			steps: [{
				//----------------------------------------------
				//       check-out repo and set-up python
				//----------------------------------------------
				name: "Check out repository"
				uses: "actions/checkout@v4"
				with: submodules: true
			}, {

				//----------------------------------------------
				//  -----  setup python   -----
				//----------------------------------------------
				name: "Set up the environment"
				uses: "actions/setup-python@v5"
				id:   "setup-python"
				with: "python-version": "${{ env.MINIMUM_PYTHON_VERSION }}"
			}, {

				//----------------------------------------------
				//  -----  setup uv and load cache   -----
				//----------------------------------------------
				name: "Set up uv"
				uses: "astral-sh/setup-uv@v5"
				with: {
					version:        "${{ env.UV_VERSION }}"
					"enable-cache": true
				}
			}, {

				//----------------------------------------------
				//  -----  build distribution -----
				//----------------------------------------------
				name: "Build distribution"
				run:  "make build"
			}, {

				//----------------------------------------------
				//  -----  upload artifacts  -----
				//----------------------------------------------
				uses: "actions/upload-artifact@v4"
				with: {
					name: "pypi_files"
					path: "dist"
				}
			}]
		}
		"test-build": {

			// This action runs the test suite on the built artifact in the `build` action.
			// The default is to run this in ubuntu, macos and windows
			name: "${{ matrix.os }} / \(_min_py_version) / test built artifact"
			needs: ["build"]
			strategy: {
				"fail-fast": false
				matrix: os: [
					"ubuntu",
					"macos",
					"windows",
				]
			}
			"runs-on": "${{ matrix.os }}-latest"
			steps: [{
				uses: "actions/checkout@v4"
				with: submodules: true
			}, {
				name: "set up python"
				uses: "actions/setup-python@v5"
				with: "python-version": "${{ env.MINIMUM_PYTHON_VERSION }}"
			}, {
				name: "get dist artifacts"
				uses: "actions/download-artifact@v4"
				with: {
					name: "pypi_files"
					path: "dist"
				}
			}, {
				run: "rm -r <INSERT PROJECT SRC>"
			}, {
				run: "pip install typing-extensions"
			}, {
				run: "pip install -r tests/requirements-testing.lock"
			}, {
				run: "pip install <INSERT PROJECT NAME> --no-index --no-deps --find-links dist --force-reinstall"
			}, {
				run: "pytest"
			}]
		}

		// https://github.com/marketplace/actions/alls-green#why used for branch protection checks
		"release-check": {
			if: "always()"
			needs: [
				"build",
				"test-build",
			]
			"runs-on": "ubuntu-latest"
			permissions: {}
			steps: [{
				name: "Decide whether the needed jobs succeeded or failed"
				uses: "re-actors/alls-green@release/v1"
				with: {
					// allowed-failures: coverage
					jobs: "${{ toJSON(needs) }}"
				}
			}]
		}
		publish: {

			// This action publishes the built and tested artifact to PyPI, but only on a tag
			needs: ["test-build"]
			if:          "success() && startsWith(github.ref, 'refs/tags/v')"
			"runs-on":   "ubuntu-latest"
			environment: "release"
			permissions: {
				// IMPORTANT: this permission is mandatory for trusted publishing
				"id-token": "write"
			}
			steps: [{
				uses: "actions/checkout@v4"
				with: "fetch-depth": 0
			}, {
				name: "Set up Python ${{ env.MINIMUM_PYTHON_VERSION }}"
				uses: "actions/setup-python@v5"
				with: "python-version": "${{ env.MINIMUM_PYTHON_VERSION }}"
			}, {
				name: "get dist artifacts"
				uses: "actions/download-artifact@v4"
				with: {
					name: "pypi_files"
					path: "dist"
				}
			}, {
				name: "Publish package to PyPI"
				uses: "pypa/gh-action-pypi-publish@release/v1"
			}]
		}
	}
}
