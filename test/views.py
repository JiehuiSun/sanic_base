# -*- coding: utf-8 -*-


from sanic.views import HTTPMethodView
from sanic.response import text


class TestView(HTTPMethodView):
    async def get(self, req, key):
        return text("ok")
