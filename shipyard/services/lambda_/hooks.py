"""Definition of Plux extension points (i.e., hooks) for Lambda."""
from shipyard.runtime.hooks import hook_spec

HOOKS_LAMBDA_START_DOCKER_EXECUTOR = "shipyard.hooks.lambda_start_docker_executor"
HOOKS_LAMBDA_PREPARE_DOCKER_EXECUTOR = "shipyard.hooks.lambda_prepare_docker_executors"
HOOKS_LAMBDA_INJECT_LAYER_FETCHER = "shipyard.hooks.lambda_inject_layer_fetcher"

start_docker_executor = hook_spec(HOOKS_LAMBDA_START_DOCKER_EXECUTOR)
prepare_docker_executor = hook_spec(HOOKS_LAMBDA_PREPARE_DOCKER_EXECUTOR)
inject_layer_fetcher = hook_spec(HOOKS_LAMBDA_INJECT_LAYER_FETCHER)
