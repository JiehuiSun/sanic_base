# -*- coding: utf-8 -*-


import datetime
import types
from functools import wraps

import jwt
from sanic.request import Request
from sanic.response import json, text
from sanic.views import HTTPMethodView

from . import errors


def check_token(request: Request):
    """
    检测Token
    如果不是用JWT重写此函数
    """
    if not request.token:
        return False

    try:
        jwt.decode(
            request.token,
            request.app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidTokenError:
        return False
    except jwt.exceptions.ExpiredSignatureError:
        raise False
    except KeyError:
        raise errors.BaseError("System Error.")
    else:
        return True


def authorized():
    """认证"""
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json(Api().error(10201), 401)
        return decorated_function
    return decorator


class VerParams:
    """
    参数校验
    """
    def _ver_params(self, params_dict, data):
        data_keys = set(data.keys())
        max_keys = set(params_dict.keys())
        min_keys = set()
        for k in max_keys:
            check_method = params_dict[k]
            if isinstance(check_method, types.FunctionType):
                continue
            params_dict_list = params_dict[k].split(' ')
            if 'optional' not in params_dict_list:
                min_keys.add(k)
        overflow_keys = data_keys - max_keys
        lack_keys = min_keys - data_keys

        # 验证后端需要的key 传递情况
        flag_keys_not_match = False
        errmsg_keys_not_match = ''
        if overflow_keys:
            flag_keys_not_match = True
            errmsg_keys_not_match += 'Unexpected Params: '
            errmsg_keys_not_match += ', '.join([str(k) for k in overflow_keys])
        if lack_keys:
            flag_keys_not_match = True
            errmsg_keys_not_match += 'Missing {} Required Positional Params: '\
                .format(len(lack_keys))
            errmsg_keys_not_match += ', '.join([str(k) for k in lack_keys])
        if flag_keys_not_match:
            return errmsg_keys_not_match

        # 根据params_dict 逐条验证参数.
        errmsg_keys_valid = []
        for k, v in data.items():
            flag = False
            msg = ''
            check_method = params_dict[k]
            # 执行用户自定义验证方法
            if isinstance(check_method, types.FunctionType):
                flag, msg = check_method(v, k)
            elif isinstance(check_method, str):
                check_method_list = check_method.split(' ')
                for item_method in check_method_list:
                    if "|" in item_method:
                        item_method, tag = item_method.split("|")
                        flag, msg = getattr(self, '_valid_'+item_method)(v,
                                                                         k,
                                                                         tag)
                    else:
                        flag, msg = getattr(self, '_valid_'+item_method)(v, k)
                    if not flag:
                        break
                # 执行默认方法
            if not flag:
                errmsg_keys_valid.append(msg)
                continue
        if errmsg_keys_valid:
            errmsg = ' '.join(errmsg_keys_valid)
            return "Params Error: {0}".format(errmsg)
        return True

    def _valid_str(self, i, key_name=None, lenth=None):
        if isinstance(i, str):
            if not lenth:
                return True, 'OK'
            else:
                try:
                    lenth = int(lenth)
                except ValueError:
                    raise errors.InvalidArgsError("参数定义错误")
                if len(i) <= lenth:
                    return True, 'OK'

        return False, key_name

    def _valid_required(self, i, key_name=None):
        '''
        该参数必须有值, 并且判断不能为 False
        '''
        if i or i == 0 or i == []:
            return True, key_name
        return False, key_name

    def _valid_optional(self, i, key_name=None):
        '''
        该参数可以不存在
        '''
        return True, 'OK'

    def _valid_pass(self, i, key_name=None):
        '''
        该参数必须存在, 但不需要验证
        '''
        return True, 'OK'

    def _valid_list(self, i, key_name=None):
        '''
        参数必须为list类型
        '''
        if isinstance(i, list):
            return True, 'OK'
        return False, '{0} 必须为list(array)类型, 谢谢配合!'.format(key_name)

    def _valid_int(self, i, key_name=None):
        '''
        参数必须为int类型
        '''
        if isinstance(i, int):
            return True, 'OK'
        else:
            try:
                int(i)
                return True, 'OK'
            except ValueError:
                pass
        return False, '{0} 必须为int(整型)类型, 谢谢配合!'.format(key_name)

    def _valid_date(self, i, key_name=None, dt_format='%Y-%m-%d %H:%M:%S'):
        '''
        参数必须为日期xxxx-xx-xx xx:xx:xx (以自定义为准)
        '''
        try:
            datetime.datetime.strptime(i, dt_format)
            return True, 'OK'
        except ValueError:
            return False, '{key_name} 日期格式错误, 如: "{dt_format}", 谢谢配合!'


class Api(HTTPMethodView, VerParams):
    decorators = [authorized()]

    def __init__(self, *args, **kwargs):
        self.params_dict: dict = {}
        self.request: Request = None
        self.key: str = None
        self.data: dict = None
        self.call_method: str = None

    async def dispatch_request(self, *args, **kwargs):
        self.request = args[0]
        self.key = kwargs.get("key")
        await self._handle_params()
        await self._dispatch()
        method = getattr(self, self.call_method, None)
        if not method:
            raise errors.MethodError()

        _pre_h = await self._pre_handle()
        if _pre_h:
            return _pre_h
        result = await method()

        await self._after_handle()

        if isinstance(result, dict):
            return json(result)
        elif isinstance(result, str):
            return text(result)
        else:
            return result

    async def _handle_params(self, *args, **kwargs):
        """
        处理参数
        """
        if self.request.method.lower() != 'get':
            self.data = self.request.json
        else:
            self.data = dict(self.request.query_args)

    async def ver_params(self, *args, **kwargs):
        """校验参数"""
        ret = self._ver_params(self.params_dict, self.data)
        if ret is not True:
            # 401?
            raise errors.InvalidArgsError(ret)

    async def _dispatch(self, *args, **kwargs):
        self.call_method = self.request.method.lower()
        if self.call_method == 'get' and not self.key:
            self.call_method = 'list'

    async def _pre_handle(self, *args, **kwargs):
        """
        调用试图之前处理(可以改为Sanic自带的生命周期中间件)
        """
        pass

    async def _after_handle(self, *args, **kwargs):
        """
        调用试图之后处理(可以改为Sanic自带的生命周期中间件)
        """
        pass

    def ret(self, data: dict = None) -> dict:
        """业务正常返回"""
        return {
            "errCode": 0,
            "errMsg": "OK",
            "data": data
        }

    def error(self, errcode: int, errmsg: str = None) -> dict:
        """业务错误"""
        if not errmsg and errcode:
            errmsg = errors.API_ERROR.get(errcode)
            if not errmsg:
                errmsg = errors.API_ERROR[10101]
        return {
            "errCode": errcode,
            "errMsg": errmsg
        }
