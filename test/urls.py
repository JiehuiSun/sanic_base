# -*- coding: utf-8 -*-


from .views import TestView


routing_dict = dict()

routing_dict["/test"] = TestView

routing_dict.update(routing_dict)
