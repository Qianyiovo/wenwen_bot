from nonebot import on_command
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import (
    Message,
    GroupMessageEvent,
    Bot,
)
from nonebot_plugin_tortoise_orm import add_model
import json
import config

add_model("models.orm")

add_admin = on_command("添加管理员", permission=SUPERUSER)

remove_admin = on_command("删除管理员", permission=SUPERUSER)


@add_admin.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    if event.group_id in config.groups:
        user_id = args.extract_plain_text()
        if user_id:
            try:
                with open("admins.json", "r") as fp:
                    admins = json.load(fp)
            except FileNotFoundError:
                admins = []

            admins.append(user_id)
            with open("admins.json", "w") as fp:
                json.dump(admins, fp)

            logger.info(f"「{event.user_id} 」添加了管理员「{user_id}」")
            logger.info("管理员列表已更新")
            await add_admin.finish(f"添加成功！")
        else:
            await add_admin.finish(f"无效的语法！\n正确的语法：/添加管理员 <QQ号>")


@remove_admin.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    if event.group_id in config.groups:
        user_id = args.extract_plain_text()
        if user_id:
            try:
                with open("admins.json", "r") as fp:
                    admins = json.load(fp)
            except FileNotFoundError:
                admins = []
                with open("admins.json", "w") as fp:
                    json.dump(admins, fp)
            if user_id in admins:
                admins.remove(user_id)
                with open("admins.json", "w") as fp:
                    json.dump(admins, fp)

                logger.info(f"「{event.user_id} 」删除了管理员「{user_id}」")
                logger.info("管理员列表已更新")
                await remove_admin.finish(f"删除成功！")
            else:
                await remove_admin.finish(f"该用户不是管理员！")
        else:
            await remove_admin.finish(f"无效的语法！\n正确的语法：/删除管理员 <QQ号>")