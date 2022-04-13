# -*- coding: utf-8 -*-


import pytz
import datetime

from api import Api, errors
from utils import dt2str, dt2utc

from .models import UserStatus
from .services import (create_user, gen_token, get_user, get_user_from_openid,
                       list_user)


class UserView(Api):
    async def get(self):
        user = await get_user(self.key)
        if user is not None:
            await self.handle_user_info(user)
            return self.ret(user)
        return self.error(20001)

    async def list(self):
        self.params_dict = {
            "pageNo": "optional str",
            "pageSize": "optional str",
        }
        await self.ver_params()
        data = await list_user(**self.data)

        for i in data["dataList"]:
            await self.handle_user_info(i)

        return self.ret(data)

    async def post(self):
        self.params_dict = {
            "openID": "required str|43",
            "loginType": "optional str",
            "sdkType": "optional str",
            "phone": "optional str",
        }
        await self.ver_params()
        await create_user(**self.data)
        return self.ret()

    async def put(self):
        pass

    async def delete(self):
        """
        软删除
        """
        pass

    async def handle_user_info(self, user_dict):
        """处理用户信息"""
        for k, v in user_dict.items():
            if isinstance(v, datetime.datetime):
                v = dt2str(dt2utc(v))
            elif k == "status":
                status = getattr(UserStatus, v, None)
                if not status:
                    raise errors.EnumError("用户状态错误")
                v = {
                    "key": status.name,
                    "value": status.value
                }
            user_dict[k] = v
        return user_dict


class LoginView(UserView):
    """登录/注册"""
    decorators = []

    async def post(self):
        self.params_dict = {
            "openID": "required str|43",
            "loginType": "optional str",
            "sdkType": "optional str",
            "phone": "optional str",
        }
        await self.ver_params()

        user = await get_user_from_openid(self.data["openID"])
        if user is not None:
            uid = user["_id"]
        else:
            uid = await create_user(**self.data)

        token = gen_token(self.request.app, uid)
        return self.ret({"token": token})
