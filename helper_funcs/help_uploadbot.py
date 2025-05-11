import os
import time
import math
import logging
import requests
import datetime

logger = logging.getLogger(__name__)

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nPercentage: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join([" " for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

async def DownLoadFile(url, file_name, client, ud_type, message, start_time, progress_for_pyrogram):
    try:
        if "placeholder.com" in url:
            logger.warning("Skipping placeholder.com URL")
            return None
        r = requests.get(url, allow_redirects=True, stream=True)
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(file_name, "wb") as fd:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    fd.write(chunk)
                    downloaded += len(chunk)
                    await progress_for_pyrogram(downloaded, total_size, ud_type, message, start_time)
        return file_name
    except requests.exceptions.ConnectionError as e:
        logger.warning(f"Failed to download {url}: {e}")
        return None
