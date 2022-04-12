# -*- coding: utf-8 -*-

"""
    100xx: 公共系统错误码
    101xx: 公共业务错误码
    20xxx: 账号系统
    30xxx: 邮件系统
    40xxx: 兑换码系统
    50xxx: 时间服务
    60xxx: 云存档系统
"""


class BaseError(Exception):
    errno = 10000
    errmsg = '程序员跑路了'

    def __init__(self, errmsg=None):
        if errmsg:
            self.errmsg = errmsg


class MethodError(BaseError):
    errno = 10002
    errmsg = '不支持的请求方式'


class InvalidArgsError(BaseError):
    errno = 10003
    errmsg = '无效的参数'


class EnumError(BaseError):
    errno = 10004
    errmsg = '枚举类型错误'


# 业务错误码
API_ERROR = {
    0: "OK",
    10101: "服务其他异常",
    10201: "Token无效",

    20001: "用户不存在",

    40001: "兑换码无效",
    40002: "兑换码过期",
    40003: "兑换码已使用",
    40004: "兑换码已被领取完",
}
