# -*- coding: utf-8 -*-


from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

from api import Api
from .models import GiftPool



class TestView(Api):
    async def get(self):
        """
        详情
        /api/test/test/1
        """
        read_concern = ReadConcern(level='majority')
        unfin_pool = await GiftPool.with_options(
            read_concern=read_concern,
            read_preference=ReadPreference.PRIMARY
        ).find_one(
            {
                'poolState': 'i',
                'poolType': "primary"
            },
            sort=[('tOpen', -1)],
            projection={'gifts': 1, 'poolVersion': 1}
        )

        return unfin_pool

    async def list(self):
        """
        列表
        /api/test/test
        """
        return {"method": "list"}
