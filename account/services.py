# -*- coding: utf-8 -*-


import uuid

from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference

from .models import User
from utils import gen_random, utc_now


async def get_user(user_id):
    read_concern = ReadConcern(level='majority')
    user = await User.with_options(
        read_concern=read_concern,
        read_preference=ReadPreference.PRIMARY
    ).find_one(
        {"_id": user_id}
    )
    return user


async def list_user(projects=None, **kwargs):
    page = int(kwargs.pop("pageNo", 1))
    limit = int(kwargs.pop("pageSize", 100))
    count = await User.count_documents(kwargs)
    user = await User.find(
        kwargs,
        projects,
        as_raw=True,
        skip=(page - 1) * limit,
        limit=page * limit
    )

    ret = {
        "pageNo": page,
        "pageSize": limit,
        "totalPage": count,
        "data": user.objects
    }
    return ret


async def create_user(**kwargs):
    # TODO 直接uuid也可以, 如需分类需确定sdkType值
    kwargs["_id"] = "%s%s-%s" % (kwargs.get("sdkType", "10"), gen_random(), uuid.uuid4())
    now = utc_now()
    kwargs["tInsert"] = now
    kwargs["tUpdate"] = now
    kwargs["tSignUp"] = now
    kwargs["active"] = True
    kwargs["status"] = "zc"
    write_concern = WriteConcern(w='majority', wtimeout=6000, j=True)
    await User.with_options(
        write_concern=write_concern
    ).insert_one(kwargs)
    return


async def update_user(projects=None, **kwargs):
    read_concern = ReadConcern(level='majority')
    user = await User.with_options(
        read_concern=read_concern,
        read_preference=ReadPreference.PRIMARY
    ).find(
        kwargs, projects
    )
    return user
