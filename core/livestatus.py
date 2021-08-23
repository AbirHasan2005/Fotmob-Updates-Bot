# (c) @AbirHasan2005

import aiohttp
import asyncio
import datetime
from pyrogram import Client
from pyrogram.types import Message
from core.send_msg import SendMessage, EditMessage

MessagesDB = {}


async def GetData(date: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.fotmob.com/matches?date={date}") as resp:
            data = await resp.json()
            return data


async def GetLiveStatus(bot: Client, updates_channel_id: int):
    running = False
    status = ""
    reason = ""
    while True:
        print("Getting Data ...")
        data = await GetData(str(datetime.datetime.now().date()).replace('-', ''))
        for i in range(len(data["leagues"])):
            print("Loading Data ...")
            for x in range(len(data["leagues"][i]["matches"])):
                leagueName = data["leagues"][i]["name"]
                firstMatchTime = data["leagues"][i]["matches"][x]["time"]
                finished = data["leagues"][i]["matches"][x]["status"].get("finished", True)
                started = data["leagues"][i]["matches"][x]["status"].get("started", False)
                cancelled = data["leagues"][i]["matches"][x]["status"].get("cancelled", False)
                ongoing = data["leagues"][i]["matches"][x]["status"].get("ongoing", False)
                score = data["leagues"][i]["matches"][x]["status"].get("scoreStr", "")
                if score == "":
                    score = f"{data['leagues'][i]['matches'][x]['home']['score']} - {data['leagues'][i]['matches'][x]['away']['score']}"
                if (finished is False) and (started is True) and (cancelled is False) and (ongoing is True):
                    running, status = True, "Started"
                elif finished is True:
                    running, status = False, "Finished"
                elif cancelled is True:
                    running, status, reason = False, "Cancelled", data["leagues"][i]["matches"][x]["status"].get("reason", {}).get("long", "")
                if (running is True) and (finished is False) and (ongoing is True):
                    liveTime = data["leagues"][i]["matches"][x]["status"].get("liveTime", {}).get("long", "")
                    text = f"**League Name:** `{leagueName}`\n\n" \
                           f"**Match Date:** `{firstMatchTime}`\n\n" \
                           f"**Match Status:** `{status}`\n\n" \
                           f"**Time Passed:** `{liveTime}`\n\n" \
                           f"**Teams:** `{data['leagues'][i]['matches'][x]['home']['name']}`  __VS__  `{data['leagues'][i]['matches'][x]['away']['name']}`\n\n" \
                           f"**Score:** `{score}`"
                    if MessagesDB.get(data["leagues"][i]["matches"][x]["id"], None) is None:
                        message = await SendMessage(bot, text, updates_channel_id)
                        MessagesDB[data["leagues"][i]["matches"][x]["id"]] = message
                        print("Sleeping 5s ...")
                        await asyncio.sleep(5)
                    else:
                        editable: Message = MessagesDB[data["leagues"][i]["matches"][x]["id"]]
                        await EditMessage(editable, text)
                elif running is False:
                    if MessagesDB.get(data["leagues"][i]["matches"][x]["id"], None) is not None:
                        status_reason = f"{status}\n\n" \
                                        f"**Reason:** `{reason}`\n\n"
                        text = f"**League Name:** `{leagueName}`\n\n" \
                               f"**Match Date:** `{firstMatchTime}`\n\n" \
                               f"**Match Status:** `{status if (status == 'Finished') else status_reason}`\n\n" \
                               f"**Teams:** `{data['leagues'][i]['matches'][x]['home']['name']}`  __VS__  `{data['leagues'][i]['matches'][x]['away']['name']}`\n\n" \
                               f"**Score:** `{score}`"
                        editable: Message = MessagesDB[data["leagues"][i]["matches"][x]["id"]]
                        await EditMessage(editable, text)
        print("Sleeping 60s ...")
        await asyncio.sleep(60)
