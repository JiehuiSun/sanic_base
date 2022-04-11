# -*- coding: utf-8 -*-


from sanic.views import HTTPMethodView
from sanic.response import text, json


class Api(HTTPMethodView):
    async def dispatch_request(self, *args, **kwargs):
        self.request = args[0]
        self.key = kwargs.get("key")
        await self._handle_params()
        await self._dispatch()
        method = getattr(self, self.call_method, None)
        if not method:
            raise MethodError()

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
        pass

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


class BaseError(Exception):
    errno = 10000
    errmsg = '程序员跑路了'

    def __init__(self, errmsg=None):
        if errmsg:
            self.errmsg = errmsg


class MethodError(BaseError):
    errno = 10002
    errmsg = '不支持的请求方式'
