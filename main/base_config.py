# -*- coding: utf-8 -*-
import os


class BaseConfig(object):
    DEBUG = True
    ENV = "production"  # development/production
    TESTING = True
    SECRET_KEY = "08dd9f956653fb091a358b1b4183bc08"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_DIR = "template"
    STATIC_DIR = "static"
    RESP_MODE = "json"
    MODULES = (
        "test",
        "account",
    )
    MOTOR_URI = "mongodb://localhost:27017/mt_prod"
