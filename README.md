# Gitlab Google Chat Integration

A Python Flask web application that forwards webhook requests
from GitLab to Google Chat.

![GGCI showcase](https://raw.githubusercontent.com/lukany/ggci/cb0886eb6594e36c5e56e54f00dbfdb71d3d8629/showcase.png)

## Installation

`ggci` is available as a Python package
on [PyPI](https://pypi.org/project/ggci).
It can be installed via standard package managers in Python, e.g. pip:

```sh
pip install ggci
```

## Usage

`ggci` provides a standard Flask application factory `create_app()`:

```python
from ggci import create_app

app = create_app()
```

For how to use this application factory refer to the official [Flask
documentation](https://flask.palletsprojects.com/en/1.1.x/).

## Configuration

There are several ways how `ggci` can be configured.

### YAML config (default)

By default `create_app()` looks for a YAML configuration file specified
by `GGCI_CONFIG` environment variable.
Example config:

```YAML
ggci_secret: xxxxxxx

user_mappings:  # OPTIONAL, used for mentions; key: GitLab ID, val: Google Chat ID
  5894317: 120984893489384029908  # Gandalf
  4985120: 109238409842809234892  # Chuck Norris
```

### Config Object

Alternatively, `create_app()` also accepts optional argument `config` of type
`ggci.Config`.

```python
from ggci import Config, create_app

config = Config(
    ggci_secret='xxxxxxx',
    user_mappings={
        5894317: 120984893489384029908,  # Gandalf
        4985120: 109238409842809234892,  # Chuck Norris
    },
)

app = create_app(config=config)
```

## Features

### Merge Request Events Notifications

Notifications for merge requests actions.
All notifications for one MR are posted to the same thread (identified
by merge request ID).
Supported actions:

- *open*: includes link with title, event author, mentions of assignees
  and description
- *approved*: includes link and event author
- *update of assigness*: includes link and mentions of current assignees
- *merged*: includes link and action author
- *closed*: includes link and action author
- *reopened*: includes link and action author
