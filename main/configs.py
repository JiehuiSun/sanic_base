# -*- coding: utf-8 -*-


from .base_config import BaseConfig


class Config(BaseConfig):
    ENV = "development"
    MOTOR_URI = "mongodb://localhost:27017/dlwn?readConcernLevel=majority&directConnection=true&ssl=false"
