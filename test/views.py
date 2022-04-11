# -*- coding: utf-8 -*-


from api import Api


class TestView(Api):
    async def get(self):
        """
        详情
        /api/test/test/1
        """
        return "get"

    async def list(self):
        """
        列表
        /api/test/test/1
        """
        return {"method": "list"}
