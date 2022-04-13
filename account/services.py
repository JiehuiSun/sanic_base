# -*- coding: utf-8 -*-


import time
import uuid

from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern

from utils import gen_random, utc_now

from .models import User


async def get_user(user_id: str) -> dict:
    read_concern = ReadConcern(level='majority')
    user = await User.with_options(
        read_concern=read_concern,
        read_preference=ReadPreference.PRIMARY
    ).find_one(
        {"_id": user_id}
    )
    return user


async def list_user(projects: dict = None, **kwargs) -> dict:
    """
    Params: projects User Res Field
    Params: kwargs User Fielter Field

    Reture: dict
    """
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


async def create_user(**kwargs) -> None:
    """创建用户"""
    # TODO 直接uuid也可以, 如需分类需确定sdkType值
    kwargs["_id"] = "%s%s-%s" % (kwargs.get("sdkType", "10"),
                                 gen_random(),
                                 uuid.uuid4())
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
    pass


async def get_user_from_openid(openid: str, **kwargs) -> dict:
    """
    根据openid获取用户

    kwargs传sdkType等来源区分
    """
    kwargs["openID"] = openid
    read_concern = ReadConcern(level='majority')
    user = await User.with_options(
        read_concern=read_concern,
        read_preference=ReadPreference.PRIMARY
    ).find_one(kwargs)
    return user


def gen_token(openid: str, **kwargs) -> str:
    """生成Token"""
    sign_str = openid + str(time.time())
    return str(uuid.uuid3(uuid.NAMESPACE_OID, sign_str))
