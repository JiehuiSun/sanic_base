# -*- coding: utf-8 -*-


from sanic import Sanic

app = Sanic.get_app("dlwn")


class User(app.ctx.BaseModel):
    """用户表"""
    __coll__ = 'user'


class WhiteUser(app.ctx.BaseModel):
    """用户白名单表"""
    __coll__ = 'white_user'
