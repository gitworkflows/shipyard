IMAGE_NAME ?= khulnasoft/shipyard
IMAGE_TAG ?= $(shell cat shipyard/__init__.py | grep '^__version__ =' | sed "s/__version__ = ['\"]\(.*\)['\"].*/\1/")
VENV_BIN ?= python3 -m venv
VENV_DIR ?= .venv
PIP_CMD ?= pip3
TEST_PATH ?= .
PYTEST_LOGLEVEL ?=
DISABLE_BOTO_RETRIES ?= 1
MAIN_CONTAINER_NAME ?= shipyard-main

MAJOR_VERSION = $(shell echo ${IMAGE_TAG} | cut -d '.' -f1)
MINOR_VERSION = $(shell echo ${IMAGE_TAG} | cut -d '.' -f2)
PATCH_VERSION = $(shell echo ${IMAGE_TAG} | cut -d '.' -f3)

ifeq ($(OS), Windows_NT)
	VENV_ACTIVATE = $(VENV_DIR)/Scripts/activate
else
	VENV_ACTIVATE = $(VENV_DIR)/bin/activate
endif

VENV_RUN = . $(VENV_ACTIVATE)

usage:                    ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/:.*##\s*/##/g' | awk -F'##' '{ printf "%-25s %s\n", $$1, $$2 }'

$(VENV_ACTIVATE): setup.py setup.cfg
	test -d $(VENV_DIR) || $(VENV_BIN) $(VENV_DIR)
	$(VENV_RUN); $(PIP_CMD) install --upgrade pip setuptools wheel plux
	touch $(VENV_ACTIVATE)

venv: $(VENV_ACTIVATE)    ## Create a new (empty) virtual environment

freeze:                   ## Run pip freeze -l in the virtual environment
	@$(VENV_RUN); pip freeze -l

install-basic: venv       ## Install basic dependencies for CLI usage into venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -e ".[cli]"

install-runtime: venv     ## Install dependencies for the shipyard runtime into venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -e ".[cli,runtime]"

install-test: venv        ## Install requirements to run tests into venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -e ".[cli,runtime,test]"

install-test-only: venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -e ".[test]"

install-dev: venv         ## Install developer requirements into venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -e ".[cli,runtime,test,dev]"

install-dev-types: venv   ## Install developer requirements incl. type hints into venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -e ".[cli,runtime,test,dev,typehint]"

install-s3: venv     ## Install dependencies for the shipyard runtime for s3-only into venv
	$(VENV_RUN); $(PIP_CMD) install $(PIP_OPTS) -e ".[cli,base-runtime]"

install: install-dev entrypoints  ## Install full dependencies into venv

entrypoints:              ## Run setup.py develop to build entry points
	$(VENV_RUN); python setup.py plugins egg_info
	@# make sure that the entrypoints were correctly created and are non-empty
	@test -s shipyard_core.egg-info/entry_points.txt || (echo "Entrypoints were not correctly created! Aborting!" && exit 1)

dist: entrypoints        ## Build source and built (wheel) distributions of the current version
	$(VENV_RUN); pip install --upgrade twine; python setup.py sdist bdist_wheel

publish: clean-dist dist  ## Publish the library to the central PyPi repository
	# make sure the dist archive contains a non-empty entry_points.txt file before uploading
	tar --wildcards --to-stdout -xf dist/shipyard-core*.tar.gz "shipyard-core*/shipyard_core.egg-info/entry_points.txt" | grep . > /dev/null 2>&1 || (echo "Refusing upload, shipyard-core dist does not contain entrypoints." && exit 1)
	$(VENV_RUN); twine upload dist/*

coveralls:         		  ## Publish coveralls metrics
	$(VENV_RUN); coveralls

start:             		  ## Manually start the local infrastructure for testing
	($(VENV_RUN); exec bin/shipyard start --host)

TAGS ?= $(IMAGE_NAME)
docker-save-image: 		  ## Export the built Docker image
	docker save -o target/shipyard-docker-image-$(PLATFORM).tar $(TAGS)

# By default we export the community image
TAG ?= $(IMAGE_NAME)
# By default we load the result to the docker daemon
DOCKER_BUILD_FLAGS ?= "--load"
DOCKERFILE ?= "./Dockerfile"
docker-build: 			  ## Build Docker image
	# start build
	# --add-host: Fix for Centos host OS
	# --build-arg BUILDKIT_INLINE_CACHE=1: Instruct buildkit to inline the caching information into the image
	# --cache-from: Use the inlined caching information when building the image
	DOCKER_BUILDKIT=1 docker buildx build --pull --progress=plain \
		--cache-from $(TAG) --build-arg BUILDKIT_INLINE_CACHE=1 \
		--build-arg SHIPYARD_PRE_RELEASE=$(shell cat shipyard/__init__.py | grep '^__version__ =' | grep -v '.dev' >> /dev/null && echo "0" || echo "1") \
		--build-arg SHIPYARD_BUILD_GIT_HASH=$(shell git rev-parse --short HEAD) \
		--build-arg=SHIPYARD_BUILD_DATE=$(shell date -u +"%Y-%m-%d") \
		--build-arg=SHIPYARD_BUILD_VERSION=$(IMAGE_TAG) \
		--add-host="localhost.localdomain:127.0.0.1" \
		-t $(TAG) $(DOCKER_BUILD_FLAGS) . -f $(DOCKERFILE)

docker-build-multiarch:   ## Build the Multi-Arch Full Docker Image
	# Make sure to prepare your environment for cross-platform docker builds! (see doc/developer_guides/README.md)
	# Multi-Platform builds cannot be loaded to the docker daemon from buildx, so we can't add "--load".
	make DOCKER_BUILD_FLAGS="--platform linux/amd64,linux/arm64" docker-build

SOURCE_IMAGE_NAME ?= $(IMAGE_NAME)
TARGET_IMAGE_NAME ?= $(IMAGE_NAME)
docker-push-master: 	  ## Push a single platform-specific Docker image to registry IF we are currently on the master branch
	(CURRENT_BRANCH=`(git rev-parse --abbrev-ref HEAD | grep '^master$$' || ((git branch -a | grep 'HEAD detached at [0-9a-zA-Z]*)') && git branch -a)) | grep '^[* ]*master$$' | sed 's/[* ]//g' || true`; \
		test "$$CURRENT_BRANCH" != 'master' && echo "Not on master branch.") || \
	((test "$$DOCKER_USERNAME" = '' || test "$$DOCKER_PASSWORD" = '' ) && \
		echo "Skipping docker push as no credentials are provided.") || \
	(REMOTE_ORIGIN="`git remote -v | grep '/shipyard' | grep origin | grep push | awk '{print $$2}'`"; \
		test "$$REMOTE_ORIGIN" != 'https://github.com/khulnasoft/shipyard.git' && \
		test "$$REMOTE_ORIGIN" != 'git@github.com:khulnasoft/shipyard.git' && \
		echo "This is a fork and not the main repo.") || \
	( \
		docker info | grep Username || docker login -u $$DOCKER_USERNAME -p $$DOCKER_PASSWORD; \
			docker tag $(SOURCE_IMAGE_NAME):latest $(TARGET_IMAGE_NAME):latest-$(PLATFORM) && \
		((! (git diff HEAD~1 shipyard/__init__.py | grep '^+__version__ =' | grep -v '.dev') && \
			echo "Only pushing tag 'latest' as version has not changed.") || \
			(docker tag $(TARGET_IMAGE_NAME):latest-$(PLATFORM) $(TARGET_IMAGE_NAME):stable-$(PLATFORM) && \
				docker tag $(TARGET_IMAGE_NAME):latest-$(PLATFORM) $(TARGET_IMAGE_NAME):$(IMAGE_TAG)-$(PLATFORM) && \
				docker tag $(TARGET_IMAGE_NAME):latest-$(PLATFORM) $(TARGET_IMAGE_NAME):$(MAJOR_VERSION)-$(PLATFORM) && \
				docker tag $(TARGET_IMAGE_NAME):latest-$(PLATFORM) $(TARGET_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION)-$(PLATFORM) && \
				docker tag $(TARGET_IMAGE_NAME):latest-$(PLATFORM) $(TARGET_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_VERSION)-$(PLATFORM) && \
				docker push $(TARGET_IMAGE_NAME):stable-$(PLATFORM) && \
				docker push $(TARGET_IMAGE_NAME):$(IMAGE_TAG)-$(PLATFORM) && \
				docker push $(TARGET_IMAGE_NAME):$(MAJOR_VERSION)-$(PLATFORM) && \
				docker push $(TARGET_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION)-$(PLATFORM) && \
				docker push $(TARGET_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_VERSION)-$(PLATFORM) \
				)) && \
				  docker push $(TARGET_IMAGE_NAME):latest-$(PLATFORM) \
	)

MANIFEST_IMAGE_NAME ?= $(IMAGE_NAME)
docker-create-push-manifests:	## Create and push manifests for a docker image (default: community)
	(CURRENT_BRANCH=`(git rev-parse --abbrev-ref HEAD | grep '^master$$' || ((git branch -a | grep 'HEAD detached at [0-9a-zA-Z]*)') && git branch -a)) | grep '^[* ]*master$$' | sed 's/[* ]//g' || true`; \
		test "$$CURRENT_BRANCH" != 'master' && echo "Not on master branch.") || \
	((test "$$DOCKER_USERNAME" = '' || test "$$DOCKER_PASSWORD" = '' ) && \
		echo "Skipping docker manifest push as no credentials are provided.") || \
	(REMOTE_ORIGIN="`git remote -v | grep '/shipyard' | grep origin | grep push | awk '{print $$2}'`"; \
		test "$$REMOTE_ORIGIN" != 'https://github.com/khulnasoft/shipyard.git' && \
		test "$$REMOTE_ORIGIN" != 'git@github.com:khulnasoft/shipyard.git' && \
		echo "This is a fork and not the main repo.") || \
	( \
		docker info | grep Username || docker login -u $$DOCKER_USERNAME -p $$DOCKER_PASSWORD; \
			docker manifest create $(MANIFEST_IMAGE_NAME):latest --amend $(MANIFEST_IMAGE_NAME):latest-amd64 --amend $(MANIFEST_IMAGE_NAME):latest-arm64 && \
		((! (git diff HEAD~1 shipyard/__init__.py | grep '^+__version__ =' | grep -v '.dev') && \
				echo "Only pushing tag 'latest' as version has not changed.") || \
			(docker manifest create $(MANIFEST_IMAGE_NAME):$(IMAGE_TAG) \
			--amend $(MANIFEST_IMAGE_NAME):$(IMAGE_TAG)-amd64 \
			--amend $(MANIFEST_IMAGE_NAME):$(IMAGE_TAG)-arm64 && \
			docker manifest create $(MANIFEST_IMAGE_NAME):stable \
			--amend $(MANIFEST_IMAGE_NAME):stable-amd64 \
			--amend $(MANIFEST_IMAGE_NAME):stable-arm64 && \
			docker manifest create $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION) \
			--amend $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION)-amd64 \
			--amend $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION)-arm64 && \
			docker manifest create $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION) \
			--amend $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION)-amd64 \
			--amend $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION)-arm64 && \
			docker manifest create $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_VERSION) \
			--amend $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_VERSION)-amd64 \
			--amend $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_VERSION)-arm64 && \
				docker manifest push $(MANIFEST_IMAGE_NAME):stable && \
				docker manifest push $(MANIFEST_IMAGE_NAME):$(IMAGE_TAG) && \
				docker manifest push $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION) && \
				docker manifest push $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION) && \
				docker manifest push $(MANIFEST_IMAGE_NAME):$(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_VERSION))) && \
		docker manifest push $(MANIFEST_IMAGE_NAME):latest \
	)

docker-run-tests:		  ## Initializes the test environment and runs the tests in a docker container
	# Remove argparse and dataclasses to fix https://github.com/pytest-dev/pytest/issues/5594
	# Note: running "install-test-only" below, to avoid pulling in [runtime] extras from transitive dependencies
	docker run -e SHIPYARD_INTERNAL_TEST_COLLECT_METRIC=1 --entrypoint= -v `pwd`/tests/:/opt/code/shipyard/tests/ -v `pwd`/target/:/opt/code/shipyard/target/ -v /var/run/docker.sock:/var/run/docker.sock -v /tmp/shipyard:/var/lib/shipyard \
		$(IMAGE_NAME) \
	    bash -c "make install-test-only && pip uninstall -y argparse dataclasses && DEBUG=$(DEBUG) PYTEST_LOGLEVEL=debug PYTEST_ARGS='$(PYTEST_ARGS)' COVERAGE_FILE='$(COVERAGE_FILE)' TEST_PATH='$(TEST_PATH)' LAMBDA_IGNORE_ARCHITECTURE=1 LAMBDA_INIT_POST_INVOKE_WAIT_MS=50 TINYBIRD_PYTEST_ARGS='$(TINYBIRD_PYTEST_ARGS)' TINYBIRD_DATASOURCE='$(TINYBIRD_DATASOURCE)' TINYBIRD_TOKEN='$(TINYBIRD_TOKEN)' TINYBIRD_URL='$(TINYBIRD_URL)' CI_COMMIT_BRANCH='$(CI_COMMIT_BRANCH)' CI_COMMIT_SHA='$(CI_COMMIT_SHA)' CI_JOB_URL='$(CI_JOB_URL)' CI_JOB_NAME='$(CI_JOB_NAME)' CI_JOB_ID='$(CI_JOB_ID)' make test-coverage"

docker-run-tests-s3-only:		  ## Initializes the test environment and runs the tests in a docker container for the S3 only image
	# Remove argparse and dataclasses to fix https://github.com/pytest-dev/pytest/issues/5594
	# Note: running "install-test-only" below, to avoid pulling in [runtime] extras from transitive dependencies
	# TODO: We need node as it's a dependency of the InfraProvisioner at import time, remove when we do not need it anymore
	docker run -e SHIPYARD_INTERNAL_TEST_COLLECT_METRIC=1 --entrypoint= -v `pwd`/tests/:/opt/code/shipyard/tests/ -v `pwd`/target/:/opt/code/shipyard/target/ -v /var/run/docker.sock:/var/run/docker.sock -v /tmp/shipyard:/var/lib/shipyard \
		$(IMAGE_NAME) \
	    bash -c "make install-test-only && apt-get install -y --no-install-recommends gnupg && mkdir -p /etc/apt/keyrings && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && echo \"deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main\" > /etc/apt/sources.list.d/nodesource.list && apt-get update && apt-get install -y --no-install-recommends nodejs && pip uninstall -y argparse dataclasses && DEBUG=$(DEBUG) PYTEST_LOGLEVEL=debug PYTEST_ARGS='$(PYTEST_ARGS)' TEST_PATH='$(TEST_PATH)' TINYBIRD_PYTEST_ARGS='$(TINYBIRD_PYTEST_ARGS)' TINYBIRD_DATASOURCE='$(TINYBIRD_DATASOURCE)' TINYBIRD_TOKEN='$(TINYBIRD_TOKEN)' TINYBIRD_URL='$(TINYBIRD_URL)' CI_COMMIT_BRANCH='$(CI_COMMIT_BRANCH)' CI_COMMIT_SHA='$(CI_COMMIT_SHA)' CI_JOB_URL='$(CI_JOB_URL)' CI_JOB_NAME='$(CI_JOB_NAME)' CI_JOB_ID='$(CI_JOB_ID)' make test"


docker-run:        		  ## Run Docker image locally
	($(VENV_RUN); bin/shipyard start)

docker-mount-run:
	MOTO_DIR=$$(echo $$(pwd)/.venv/lib/python*/site-packages/moto | awk '{print $$NF}'); echo MOTO_DIR $$MOTO_DIR; \
		DOCKER_FLAGS="$(DOCKER_FLAGS) -v `pwd`/shipyard/constants.py:/opt/code/khulnasoft/shipyard/constants.py -v `pwd`/shipyard/config.py:/opt/code/khulnasoft/shipyard/config.py -v `pwd`/shipyard/plugins.py:/opt/code/khulnasoft/shipyard/plugins.py -v `pwd`/shipyard/plugin:/opt/code/khulnasoft/shipyard/plugin -v `pwd`/shipyard/runtime:/opt/code/khulnasoft/shipyard/runtime -v `pwd`/shipyard/utils:/opt/code/khulnasoft/shipyard/utils -v `pwd`/shipyard/services:/opt/code/khulnasoft/shipyard/services -v `pwd`/shipyard/http:/opt/code/khulnasoft/shipyard/http -v `pwd`/shipyard/contrib:/opt/code/khulnasoft/shipyard/contrib -v `pwd`/tests:/opt/code/shipyard/tests -v $$MOTO_DIR:/opt/code/shipyard/.venv/lib/python3.11/site-packages/moto/" make docker-run

docker-cp-coverage:
	@echo 'Extracting .coverage file from Docker image'; \
		id=$$(docker create khulnasoft/shipyard); \
		docker cp $$id:/opt/code/shipyard/.coverage .coverage; \
		docker rm -v $$id

test:              		  ## Run automated tests
	($(VENV_RUN); DEBUG=$(DEBUG) DISABLE_BOTO_RETRIES=$(DISABLE_BOTO_RETRIES) pytest --durations=10 --log-cli-level=$(PYTEST_LOGLEVEL) -s $(PYTEST_ARGS) $(TEST_PATH))

test-coverage:     		  ## Run automated tests and create coverage report
	($(VENV_RUN); python -m coverage --version; \
		DEBUG=$(DEBUG) \
		DISABLE_BOTO_RETRIES=$(DISABLE_BOTO_RETRIES) \
		SHIPYARD_INTERNAL_TEST_COLLECT_METRIC=1 \
		python -m coverage run $(COVERAGE_ARGS) -m \
		pytest --durations=10 --log-cli-level=$(PYTEST_LOGLEVEL) -s $(PYTEST_ARGS) $(TEST_PATH))

test-docker:
	DOCKER_FLAGS="--entrypoint= $(DOCKER_FLAGS)" CMD="make test" make docker-run

test-docker-mount:		  ## Run automated tests in Docker (mounting local code)
	# TODO: find a cleaner way to mount/copy the dependencies into the container...
	VENV_DIR=$$(pwd)/.venv/; \
		PKG_DIR=$$(echo $$VENV_DIR/lib/python*/site-packages | awk '{print $$NF}'); \
		PKG_DIR_CON=/opt/code/shipyard/.venv/lib/python3.11/site-packages; \
		echo "#!/usr/bin/env python" > /tmp/pytest.ls.bin; cat $$VENV_DIR/bin/pytest >> /tmp/pytest.ls.bin; chmod +x /tmp/pytest.ls.bin; \
		DOCKER_FLAGS="-v `pwd`/tests:/opt/code/shipyard/tests -v /tmp/pytest.ls.bin:/opt/code/shipyard/.venv/bin/pytest -v $$PKG_DIR/deepdiff:$$PKG_DIR_CON/deepdiff -v $$PKG_DIR/ordered_set:$$PKG_DIR_CON/ordered_set -v $$PKG_DIR/py:$$PKG_DIR_CON/py -v $$PKG_DIR/pluggy:$$PKG_DIR_CON/pluggy -v $$PKG_DIR/iniconfig:$$PKG_DIR_CON/iniconfig -v $$PKG_DIR/jsonpath_ng:$$PKG_DIR_CON/jsonpath_ng -v $$PKG_DIR/packaging:$$PKG_DIR_CON/packaging -v $$PKG_DIR/pytest:$$PKG_DIR_CON/pytest -v $$PKG_DIR/pytest_httpserver:$$PKG_DIR_CON/pytest_httpserver -v $$PKG_DIR/_pytest:$$PKG_DIR_CON/_pytest -v $$PKG_DIR/_pytest:$$PKG_DIR_CON/orjson" make test-docker-mount-code

test-docker-mount-code:
	PACKAGES_DIR=$$(echo $$(pwd)/.venv/lib/python*/site-packages | awk '{print $$NF}'); \
		DOCKER_FLAGS="$(DOCKER_FLAGS) --entrypoint= -v `pwd`/shipyard/config.py:/opt/code/khulnasoft/shipyard/config.py -v `pwd`/shipyard/constants.py:/opt/code/khulnasoft/shipyard/constants.py -v `pwd`/shipyard/utils:/opt/code/khulnasoft/shipyard/utils -v `pwd`/shipyard/services:/opt/code/khulnasoft/shipyard/services -v `pwd`/shipyard/aws:/opt/code/khulnasoft/shipyard/aws -v `pwd`/Makefile:/opt/code/shipyard/Makefile -v $$PACKAGES_DIR/moto:/opt/code/shipyard/.venv/lib/python3.11/site-packages/moto/ -e TEST_PATH=\\'$(TEST_PATH)\\' -e LAMBDA_JAVA_OPTS=$(LAMBDA_JAVA_OPTS) $(ENTRYPOINT)" CMD="make test" make docker-run

lint:              		  ## Run code linter to check code style and check if formatter would make changes
	($(VENV_RUN); python -m ruff check --show-source . && python -m black --check .)

lint-modified:     		  ## Run code linter to check code style and check if formatter would make changes on modified files
	($(VENV_RUN); python -m ruff check --show-source `git diff --diff-filter=d --name-only HEAD | grep '\.py$$' | xargs` && python -m black --check `git diff --diff-filter=d --name-only HEAD | grep '\.py$$' | xargs`)

check-aws-markers:     		  ## Lightweight check to ensure all AWS tests have proper compatibilty markers set
	($(VENV_RUN); python -m pytest --co tests/aws/)

format:            		  ## Run ruff and black to format the whole codebase
	($(VENV_RUN); python -m ruff check --show-source --fix .; python -m black .)

format-modified:          ## Run ruff and black to format only modified code
	($(VENV_RUN); python -m ruff check --show-source --fix `git diff --diff-filter=d --name-only HEAD | grep '\.py$$' | xargs`; python -m black `git diff --diff-filter=d --name-only HEAD | grep '\.py$$' | xargs` )

init-precommit:    		  ## install te pre-commit hook into your local git repository
	($(VENV_RUN); pre-commit install)

clean:             		  ## Clean up (npm dependencies, downloaded infrastructure code, compiled Java classes)
	rm -rf .filesystem
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf $(VENV_DIR)

clean-dist:				  ## Clean up python distribution directories
	rm -rf dist/ build/
	rm -rf *.egg-info

.PHONY: usage freeze install-basic install-runtime install-test install-test-only install-dev install entrypoints dist publish coveralls start docker-save-image docker-build docker-build-multiarch docker-push-master docker-create-push-manifests docker-run-tests docker-run docker-mount-run docker-cp-coverage test test-coverage test-docker test-docker-mount test-docker-mount-code lint lint-modified format format-modified init-precommit clean clean-dist
