"""
Credits : @Unknownkz
"""
from contextlib import suppress
from requests import get as get_tiktok
from validators.url import url as valid_url

from telethon.errors import ChatSendMediaForbiddenError

from FallenRobot import *
from FallenRobot.events import register
from FallenRobot import telethn as universe


@register(pattern=r"^/tiktok(?: |$)(.*)")
async def _(event):
    url = (
        await event.get_reply_message()
        if event.is_reply
        else event.pattern_match.group(1)
    )
    tt = ["tiktok", "vt.", "vm."]
    if url not in tt and not (valid_url(url) is True):
        await event.reply(
            'Mohon berikan link yang valid.'
        )
        return

    kz = await event.reply('`Processing...`')

    response = get_tiktok(f'https://api.douyin.wtf/api?url={url}').json()
    if not response:
        await kz.edit('Mohon coba lagi!')
        return
    if not response['status'] == 'success':
        await kz.edit('Video tidak ditemukan.')
        return

    video = response["video_data"]["nwm_video_url"]
    audio = response["music"]["play_url"]["uri"]
    deskripsi = response["desc"]
    author = response["author"]["nickname"]
    time = response["total_time"]

    music_title, music_author = response["music"]["title"], response["music"]["author"]

    caption = f"""
<b>INFORMATION:<b>

<b>› Author:</b> {author}
<b>› Description:</b> {deskripsi}

<b>Total Parsing Time:</b> <pre>{time}s</pre>'
"""
    audio_caption = f"""
<b>Title:</b> {music_title}
<b>Author:</b> <u>{music_author}</u>
"""
    rz = await kz.edit('`Uploading...`')
    with suppress(BaseException):
        if bool(video):
            try:
                await universe.send_file(
                    event.chat_id,
                    file=video,
                    caption=caption,
                    reply_to=event.reply_to_msg_id,
                    parse_mode='html',
                    force_document=True,
                    silent=True,
                )
            except ChatSendMediaForbiddenError:
                await rz.edit('Mohon maaf, tidak diizinkan untuk mengirim file.')
                return

            if bool(audio):
                await universe.send_file(
                    event.chat_id,
                    file=audio,
                    caption=audio_caption,
                    reply_to=event.reply_to_msg_id,
                    force_document=True,
                    parse_mode='html',
                    silent=True,
                )

    await rz.delete()

__mod_name__ = "ᴛɪᴋᴛᴏᴋ"

__help__ = """
❂ /tiktok <URL/Link/Reply Link> *:* Untuk Mendapatkan Video dan Audio dari Tiktok.
"""
