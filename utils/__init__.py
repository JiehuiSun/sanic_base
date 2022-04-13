# -*- coding: utf-8 -*-


import pytz
import random
import datetime


TZ_UTC = pytz.timezone("UTC")
TZ_LOCAL = pytz.timezone("Asia/Shanghai")


def gen_random(lenth: int = 4) -> str:
    """生成随机数字"""
    start = int("1" + "0" * (lenth - 1))
    end = int("1" + "0" * lenth)
    return random.randrange(start, end)


def utc_now():
    return datetime.datetime.utcnow()


def dt2str(dt: datetime.datetime, str_format: str = "%Y-%m-%d %H:%M:%S"):
    return dt.strftime(str_format)


def dt2utc(dt: datetime.datetime):
    return dt.replace(tzinfo=TZ_UTC).astimezone(tz=TZ_LOCAL)
