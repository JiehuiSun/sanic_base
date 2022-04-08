# -*- coding: utf-8 -*-


from flask.views import MethodView


class TestView(MethodView):
    def get(self, key):
        return "ok"
