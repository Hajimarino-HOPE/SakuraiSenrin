"""
    帮助文档V1.0.0
    似乎可以用到正则
    处理被at的信息
"""

from nonebot import on_command, on_message
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.adapters.cqhttp.event import PrivateMessageEvent
from nonebot.rule import to_me
from Utils.CustomRule import check_white_list
import os
import json
import random

HelpPath = os.path.join(os.getcwd(), 'Resources', 'HelpTXT')
StudyPath = os.path.join(os.getcwd(), 'Resources', 'Json', 'wordbank.json')

with open(os.path.join(HelpPath,'HelpList.txt'), 'r', encoding='utf-8-sig') as hp:
    HelpList = hp.read()
with open(StudyPath, 'r', encoding="utf-8") as fr:
    studylib = json.load(fr)
at_msg_reply = studylib['public']['preinstall_words']['at_msg_reply']

help = on_command("help", priority=5, rule=check_white_list())
at_msg = on_message(rule=to_me() & check_white_list(), priority=5)


@help.handle()
async def handle_help(bot: Bot, event: MessageEvent, state: dict):
    args = str(event.get_message()).strip()
    if args:
        state["functionID"] = args
        await bot.send(event, "get it!")
    else:
        msg = (
            MessageSegment.text('[help正常：Succeed]\n嘿嘿！Senrin会的有这些！快输入功能代码获取帮助吧！\n')
            +MessageSegment.at(event.user_id)+MessageSegment.text('Senrin目前支持的功能如下：\n')
            +MessageSegment.text(HelpList)
        )
        await help.send(msg)


@help.got("functionID")
async def got_funtionID(bot: Bot, event: MessageEvent, state: dict):
    functionID = state["functionID"]
    if functionID == "exit":
        await help.finish(f"润！！！")
    else:
        try:
            with open(os.path.join(HelpPath, functionID+'.txt'), mode='r', encoding='utf-8-sig') as files:
                msg = files.read()
            await help.send(msg)
        except:
            await help.reject("[参数错误：functionID]\n"
                            f"可恶，Senrin把脑子都掏空了都没找到“{functionID}”！！！\n"
                            "请重新输入功能代码，或输入 “exit”  来退出帮助文档")
        else:
            await help.finish()

@at_msg.handle()
async def _at_msg(bot: Bot, event: MessageEvent):
    if isinstance(event, PrivateMessageEvent):
        return
    else:
        msg = random.choice(at_msg_reply)
        await at_msg.finish(msg)