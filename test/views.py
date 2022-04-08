# -*- coding: utf-8 -*-


from quart.views import MethodView


class TestView(MethodView):
    async def get(self, key):
        return "ok"
