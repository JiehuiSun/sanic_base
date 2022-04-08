# -*- coding: utf-8 -*-


import os
import importlib
from flask import Flask
from flask import Blueprint
from werkzeug.routing import BaseConverter

from main import configs

APP_NAME = "dlwn"


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def create_app():
    app = Flask(APP_NAME)
    app.config.from_object(configs.Config)
    app.url_map.converters["re"] = RegexConverter
    config_blueprint(app)

    return app


def config_blueprint(app):
    instance = Blueprint(app.name,
                         __name__,
                         template_folder=app.config.get("TEMPLATE_DIR", "web"),
                         static_folder=app.config.get("STATIC_DIR", "static"))

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
            routing_dict["/{0}{1}".format(MODEL_NAME, k)] = v

    methods = ["GET", "POST", "PUT", "DELETE"]
    for path, view in routing_dict.items():
        instance.add_url_rule("{0}<re('.*'):key>".format(path),
                              view_func=view.as_view(path),
                              methods=methods)

    if app.config.get("RESP_MODE", "json") == "json":
        default_url_prefix = "/api"
    else:
        default_url_prefix = ""

    app.register_blueprint(instance,
                           url_prefix=app.config.get("URL_PREFIX", default_url_prefix))
