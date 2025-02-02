# Contributing

We welcome feedback, bug reports, and pull requests!

For pull requests (PRs), please stick to the following guidelines:

* Before submitting a PR, verify that [an issue](https://github.com/khulnasoft/shipyard/issues) exists that describes the bug fix or feature you want to contribute. If there's no issue yet, please [create one](https://github.com/khulnasoft/shipyard/issues/new/choose).
* Fork shipyard on your GitHub user account, make code changes there, and then create a PR against main shipyard repository.
* Add tests for any new features or bug fixes. Ideally, each PR increases the test coverage. Please read our [integration testing](https://docs.shipyard.khulnasoft.com/contributing/integration-tests/) and [parity testing](https://docs.shipyard.khulnasoft.com/contributing/parity-testing/) guides on how to write tests for AWS services.
* Follow the existing code style. Run `make format` and `make lint` before checking in your code.
  * Refer to [Development Environment Setup](https://docs.shipyard.khulnasoft.com/contributing/development-environment-setup/) if your local testing environment is not yet properly set up.
* Document newly introduced methods and classes with pydoc, and add inline comments to code that is not self-documenting.
* Separate unrelated changes into multiple PRs.
* When creating a PR, classify the size of your change with setting a semver label:
  * `semver: patch`: Small, non-breaking changes.
  * `semver: minor`: Bigger, non-breaking changes (like features or bigger refactorings).
  * `semver: major`: Breaking changes (no matter how big).

Please note that by contributing any code or documentation to this repository (by raising PRs, or otherwise) you explicitly agree to the [**Contributor License Agreement**](.github/CLA.md).
