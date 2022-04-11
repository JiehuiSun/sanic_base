# -*- coding: utf-8 -*-


import os
import importlib
from sanic import Sanic
from sanic import Blueprint

from main import configs

APP_NAME = "dlwn"


def create_app():
    app = Sanic(APP_NAME)
    app.config.update_config(configs.BaseConfig)
    app.config.update_config(configs.Config)
    config_blueprint(app)

    return app


def config_blueprint(app):
    if app.config.get("RESP_MODE", "json") == "json":
        default_url_prefix = "/api"
    else:
        default_url_prefix = ""

    instance = Blueprint(app.name,
                         url_prefix=app.config.get("URL_PREFIX", default_url_prefix))

    routing_dict = dict()

    for module in app.config.get("MODULES", ()):
        if not os.path.exists(f"{module}/urls.py"):
            continue

        app_router = importlib.import_module(f'{module}.urls')

        model_routing_dict = getattr(app_router, "routing_dict")
        if not model_routing_dict:
            continue

        MODEL_NAME = getattr(app_router, "MODEL_NAME", module)

        for k, v in model_routing_dict.items():
            routing_dict["/{0}/{1}/".format(MODEL_NAME, k.strip("/"))] = v

    methods = ["GET", "POST", "PUT", "DELETE"]
    for path, view in routing_dict.items():
        instance.add_route(view.as_view(), "{0}<key:.*>".format(path),
                           methods=methods)

    app.blueprint(instance)


app = create_app()


if __name__ == "__main__":
    app.run()
