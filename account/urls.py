# -*- coding: utf-8 -*-

from .views import UserView

routing_dict = dict()

routing_dict["/v1/user/"] = UserView

routing_dict.update(routing_dict)
