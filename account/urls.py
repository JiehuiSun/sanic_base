# -*- coding: utf-8 -*-

from .views import UserView, LoginView

routing_dict = dict()

routing_dict["/v1/user/"] = UserView
routing_dict["/v1/login/"] = LoginView

routing_dict.update(routing_dict)
