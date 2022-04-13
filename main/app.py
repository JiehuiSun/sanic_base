# -*- coding: utf-8 -*-


from sanic import Sanic


app = Sanic.get_app("dlwn")

__all__ = ["app"]
