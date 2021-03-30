from typing import Optional

from flask import Flask

from ggci import forwarder
from ggci.config import Config, load_yaml_config


def create_app(config: Optional[Config] = None) -> Flask:

    if config is None:
        config = load_yaml_config()
        assert isinstance(config, Config)

    if not isinstance(config, Config):
        raise TypeError(
            f'config must be of type ggci.Config, got: {type(config)}'
        )

    app = Flask(__name__)
    app.register_blueprint(forwarder.bp)
    app.config.update(dict(config))
    return app
