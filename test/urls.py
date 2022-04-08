# -*- coding: utf-8 -*-


from .views import TestView


routing_dict = dict()
v1_routing_dict = dict()

v1_routing_dict["/test"] = TestView

routing_dict.update(v1_routing_dict)
