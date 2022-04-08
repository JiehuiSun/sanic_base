# -*- coding: utf-8 -*-


from flask import Flask
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
    app.url_map.converters['re'] = RegexConverter

    return app
