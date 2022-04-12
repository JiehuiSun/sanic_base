# -*- coding: utf-8 -*-


from enum import Enum
from sanic import Sanic

app = Sanic.get_app("dlwn")


class UserStatus(Enum):
    """用户状态"""
    zc = "正常"
    wg = "外挂/修改权被封"
    sd = "管理员手动禁封"


class User(app.ctx.BaseModel):
    """用户表"""
    __coll__ = 'user'
    __unique_fields__ = ["openID"]
    """
    uid = str() # 用户ID
    openID = str()  # 用户三方ID
    loginType = //
    sdkType = //
    tInsert = datetime()    # 创建/注册时间
    tUpdate = datetime()    # 更新时间
    # active = bool() # 活动/在线
    username = str() # 用户名/手机号
    tSignUp = datetime()    # 最后的登录时间
    status = str(UserStatus.name)  # 用户状态
    """


class WhiteUser(app.ctx.BaseModel):
    """用户白名单表"""
    __coll__ = 'white_user'
    """
    id = int()  # 自增ID
    uid = str() # 用户ID
    tInsert = datetime()    # 创建时间
    tUpdate = datetime()    # 更新时间
    status = bool()  # 状态
    remarks = str() # 备注
    """
