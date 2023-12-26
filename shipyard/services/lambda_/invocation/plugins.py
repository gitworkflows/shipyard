from plugin import Plugin


class RuntimeExecutorPlugin(Plugin):
    namespace = "shipyard.lambda.runtime_executor"


class DockerRuntimeExecutorPlugin(RuntimeExecutorPlugin):
    name = "docker"

    def load(self, *args, **kwargs):
        from shipyard.services.lambda_.invocation.docker_runtime_executor import (
            DockerRuntimeExecutor,
        )

        return DockerRuntimeExecutor
