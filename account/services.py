# -*- coding: utf-8 -*-


from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference

from .models import User


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
    user = await User.find(
        kwargs, projects
    )
    return user


async def create_user(**kwargs):
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
