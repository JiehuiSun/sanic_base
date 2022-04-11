# -*- coding: utf-8 -*-


from sanic import Sanic

app = Sanic.get_app("dlwn")


class GiftPool(app.ctx.BaseModel):
    """奖池"""
    __coll__ = 'gift_pool'
