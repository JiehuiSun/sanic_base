# -*- coding: utf-8 -*-


from api import Api
from .services import list_user, get_user, create_user


class Page():
    async def handle_page(self, queryset):
        page_no = self.data.get("pageNo", 1)
        page_size = self.data.get("pageSize", 10)
        return {
            "pageNo": page_no,
            "pageSize": page_size,
            "totalPage": len(queryset),
            "data": queryset
        }


class UserView(Api, Page):
    async def get(self):
        user = await get_user(self.key)
        if not user:
            return self.ret(20001, "用户不存在")
        return self.ret(data=user)

    async def list(self):
        user_list = await list_user()

        # TODO 分页器(find返回了list, 需要在find时处理分页)
        data = await self.handle_page(user_list.objects)
        ret_list = []
        for i in data.pop("data"):
            user_dict = {
                "id": str(i["_id"])
            }
            ret_list.append(user_dict)

        data["data_list"] = ret_list

        return data

    async def post(self):
        await create_user(**self.data)
        return self.ret()

    async def put(self):
        pass

    async def delete(self):
        """
        软删除
        """
        pass
