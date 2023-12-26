<p align="center">
:zap: We are excited to announce that we released Shipyard 3.0! You can find all information about the release and the new features in our <a href="https://shipyard.khulnasoft.com/blog/2023-11-16-announcing-shipyard-30-general-availability/">blog</a> :zap:
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/khulnasoft/shipyard/master/doc/shipyard-readme-banner.svg" alt="Shipyard - A fully functional local cloud stack">
</p>

<p align="center">
  <a href="https://circleci.com/gh/khulnasoft/shipyard"><img alt="CircleCI" src="https://img.shields.io/circleci/build/gh/khulnasoft/shipyard/master?logo=circleci"></a>
  <a href="https://coveralls.io/github/khulnasoft/shipyard?branch=master"><img alt="Coverage Status" src="https://coveralls.io/repos/github/khulnasoft/shipyard/badge.svg?branch=master"></a>
  <a href="https://pypi.org/project/shipyard/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/shipyard?color=blue"></a>
  <a href="https://hub.docker.com/r/khulnasoft/shipyard"><img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/khulnasoft/shipyard"></a>
  <a href="https://pypi.org/project/shipyard"><img alt="PyPi downloads" src="https://static.pepy.tech/badge/shipyard"></a>
  <a href="#backers"><img alt="Backers on Open Collective" src="https://opencollective.com/shipyard/backers/badge.svg"></a>
  <a href="#sponsors"><img alt="Sponsors on Open Collective" src="https://opencollective.com/shipyard/sponsors/badge.svg"></a>
  <a href="https://img.shields.io/pypi/l/shipyard.svg"><img alt="PyPI License" src="https://img.shields.io/pypi/l/shipyard.svg"></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
  <a href="https://twitter.com/shipyard"><img alt="Twitter" src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social"></a>
</p>

<p align="center">
  Shipyard is a cloud software development framework to develop and test your AWS applications locally.
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#installing">Install</a> •
  <a href="#quickstart">Quickstart</a> •
  <a href="#running">Run</a> •
  <a href="#usage">Usage</a> •
  <a href="#releases">Releases</a> •
  <a href="#contributing">Contributing</a>
  <br/>
  <a href="https://docs.shipyard.khulnasoft.com" target="_blank">📖 Docs</a> •
  <a href="https://app.shipyard.khulnasoft.com" target="_blank">💻 Pro version</a> •
  <a href="https://docs.shipyard.khulnasoft.com/references/coverage/" target="_blank">☑️ Shipyard coverage</a>
</p>

---

# Overview

[Shipyard](https://shipyard.khulnasoft.com) is a cloud service emulator that runs in a single container on your laptop or in your CI environment. With Shipyard, you can run your AWS applications or Lambdas entirely on your local machine without connecting to a remote cloud provider! Whether you are testing complex CDK applications or Terraform configurations, or just beginning to learn about AWS services, Shipyard helps speed up and simplify your testing and development workflow.

Shipyard supports a growing number of AWS services, like AWS Lambda, S3, Dynamodb, Kinesis, SQS, SNS, and many more! The [Pro version of Shipyard](https://shipyard.khulnasoft.com/pricing) supports additional APIs and advanced features. You can find a comprehensive list of supported APIs on our [☑️ Feature Coverage](https://docs.shipyard.khulnasoft.com/user-guide/aws/feature-coverage/) page.

Shipyard also provides additional features to make your life as a cloud developer easier! Check out Shipyard's [User Guides](https://docs.shipyard.khulnasoft.com/user-guide/) for more information.

## Installation

The quickest way get started with Shipyard is by using the Shipyard CLI. It enables you to start and manage the Shipyard Docker container directly through your command line. Ensure that your machine has a functional [`docker` environment](https://docs.docker.com/get-docker/) installed before proceeding.

### Brew (macOS or Linux with Homebrew)

Install the Shipyard CLI through our [official Shipyard Brew Tap](https://github.com/khulnasoft/homebrew-tap):

```bash
brew install shipyard/tap/shipyard-cli
```

### Binary download (MacOS, Linux, Windows)

If Brew is not installed on your machine, you can download the pre-built Shipyard CLI binary directly:

- Visit [khulnasoft/shipyard-cli](https://github.com/khulnasoft/shipyard-cli/releases/latest) and download the latest release for your platform.
- Extract the downloaded archive to a directory included in your `PATH` variable:
    -   For MacOS/Linux, use the command: `sudo tar xvzf ~/Downloads/shipyard-cli-*-darwin-*-onefile.tar.gz -C /usr/local/bin`

### PyPI (MacOS, Linux, Windows)

Shipyard is developed using Python. To install the Shipyard CLI using `pip`, run the following command:

```bash
python3 -m pip install shipyard
```

The `shipyard-cli` installation enables you to run the Docker image containing the Shipyard runtime. To interact with the local AWS services, you need to install the `awslocal` CLI separately. For installation guidelines, refer to the [`awslocal` documentation](https://docs.shipyard.khulnasoft.com/user-guide/integrations/aws-cli/#shipyard-aws-cli-awslocal).

> **Important**: Do not use `sudo` or run as `root` user. Shipyard must be installed and started entirely under a local non-root user. If you have problems with permissions in macOS High Sierra, install with `pip install --user shipyard`

## Quickstart

Start Shipyard inside a Docker container by running:

```bash
 % shipyard start -d

     __                     _______ __             __
    / /   ____  _________ _/ / ___// /_____ ______/ /__
   / /   / __ \/ ___/ __ `/ /\__ \/ __/ __ `/ ___/ //_/
  / /___/ /_/ / /__/ /_/ / /___/ / /_/ /_/ / /__/ ,<
 /_____/\____/\___/\__,_/_//____/\__/\__,_/\___/_/|_|

 💻 Shipyard CLI 3.0.2

[20:22:20] starting Shipyard in Docker mode 🐳
[20:22:21] detaching
```

You can query the status of respective services on Shipyard by running:

```bash
% shipyard status services
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Service                  ┃ Status      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ acm                      │ ✔ available │
│ apigateway               │ ✔ available │
│ cloudformation           │ ✔ available │
│ cloudwatch               │ ✔ available │
│ config                   │ ✔ available │
│ dynamodb                 │ ✔ available │
...
```

To use SQS, a fully managed distributed message queuing service, on Shipyard, run:

```shell
% awslocal sqs create-queue --queue-name sample-queue
{
    "QueueUrl": "http://sqs.us-east-1.localhost.shipyard.khulnasoft.com:4566/000000000000/sample-queue"
}
```

Learn more about [Shipyard AWS services](https://docs.shipyard.khulnasoft.com/references/coverage/) and using them with Shipyard's `awslocal` CLI.

## Running

You can run Shipyard through the following options:

- [Shipyard CLI](https://docs.shipyard.khulnasoft.com/getting-started/installation/#shipyard-cli)
- [Docker](https://docs.shipyard.khulnasoft.com/getting-started/installation/#docker)
- [Docker Compose](https://docs.shipyard.khulnasoft.com/getting-started/installation/#docker-compose)
- [Helm](https://docs.shipyard.khulnasoft.com/getting-started/installation/#helm)

## Usage

To start using Shipyard, check out our [documentation](https://docs.shipyard.khulnasoft.com).

- [Shipyard Configuration](https://docs.shipyard.khulnasoft.com/references/configuration/)
- [Shipyard in CI](https://docs.shipyard.khulnasoft.com/user-guide/ci/)
- [Shipyard Integrations](https://docs.shipyard.khulnasoft.com/user-guide/integrations/)
- [Shipyard Tools](https://docs.shipyard.khulnasoft.com/user-guide/tools/)
- [Understanding Shipyard](https://docs.shipyard.khulnasoft.com/references/)
- [Frequency Asked Questions](https://docs.shipyard.khulnasoft.com/getting-started/faq/)

To use Shipyard with a graphical user interface, you can use the following UI clients:

* [Shipyard Web Application](https://app.shipyard.khulnasoft.com)
* [Shipyard Desktop](https://docs.shipyard.khulnasoft.com/user-guide/tools/shipyard-desktop/) 
* [Shipyard Docker Extension](https://docs.shipyard.khulnasoft.com/user-guide/tools/shipyard-docker-extension/)

## Releases

Please refer to [GitHub releases](https://github.com/khulnasoft/shipyard/releases) to see the complete list of changes for each release. For extended release notes, please refer to the [Shipyard Discuss](https://discuss.shipyard.khulnasoft.com/c/announcement/5).

## Contributing

If you are interested in contributing to Shipyard:

- Start by reading our [contributing guide](CONTRIBUTING.md).
- Check out our [developer guide](https://docs.shipyard.khulnasoft.com/contributing/).
- Navigate our codebase and [open issues](https://github.com/khulnasoft/shipyard/issues).

We are thankful for all the contributions and feedback we receive.

## Get in touch

Get in touch with the Shipyard Team to
report 🐞 [issues](https://github.com/khulnasoft/shipyard/issues/new/choose),
upvote 👍 [feature requests](https://github.com/khulnasoft/shipyard/issues?q=is%3Aissue+is%3Aopen+sort%3Areactions-%2B1-desc+),
🙋🏽 ask [support questions](https://docs.shipyard.khulnasoft.com/getting-started/help-and-support/),
or 🗣️ discuss local cloud development:

- [Shipyard Slack Community](https://shipyard.khulnasoft.com/contact/)
- [Shipyard Discussion Page](https://discuss.shipyard.khulnasoft.com/)
- [Shipyard GitHub Issue tracker](https://github.com/khulnasoft/shipyard/issues)

### Contributors

We are thankful to all the people who have contributed to this project.

<a href="https://github.com/khulnasoft/shipyard/graphs/contributors"><img src="https://opencollective.com/shipyard/contributors.svg?width=890" /></a>

### Backers

We are also grateful to all our backers who have donated to the project. You can become a backer on [Open Collective](https://opencollective.com/shipyard#backer).

<a href="https://opencollective.com/shipyard#backers" target="_blank"><img src="https://opencollective.com/shipyard/backers.svg?width=890"></a>

### Sponsors

You can also support this project by becoming a sponsor on [Open Collective](https://opencollective.com/shipyard#sponsor). Your logo will show up here along with a link to your website.

<a href="https://opencollective.com/shipyard/sponsor/0/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/shipyard/sponsor/1/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/1/avatar.svg"></a>
<a href="https://opencollective.com/shipyard/sponsor/2/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/2/avatar.svg"></a>
<a href="https://opencollective.com/shipyard/sponsor/3/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/3/avatar.svg"></a>
<a href="https://opencollective.com/shipyard/sponsor/4/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/4/avatar.svg"></a>
<a href="https://opencollective.com/shipyard/sponsor/5/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/5/avatar.svg"></a>
<a href="https://opencollective.com/shipyard/sponsor/6/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/6/avatar.svg"></a>
<a href="https://opencollective.com/shipyard/sponsor/7/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/7/avatar.svg"></a>
<a href="https://opencollective.com/shipyard/sponsor/8/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/8/avatar.svg"></a>
<a href="https://opencollective.com/shipyard/sponsor/9/website" target="_blank"><img src="https://opencollective.com/shipyard/sponsor/9/avatar.svg"></a>

## License

Copyright (c) 2017-2023 Shipyard maintainers and contributors.

Copyright (c) 2016 Atlassian and others.

This version of Shipyard is released under the Apache License, Version 2.0 (see [LICENSE](LICENSE.txt)). By downloading and using this software you agree to the [End-User License Agreement (EULA)](doc/end_user_license_agreement). To know about the external software we use, look at our [third party software tools](doc/third-party-software-tools/README.md) page.
