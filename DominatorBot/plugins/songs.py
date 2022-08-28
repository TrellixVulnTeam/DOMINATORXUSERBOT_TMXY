import asyncio
import time

from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import *


@dominator_cmd(pattern="song(?:\s|$)([\s\S]*)")
async def _(event):
    xyz = await client_id(event)
    ForGo10God, dominator_mention = xyz[0], xyz[2]
    query = event.text[6:]
    max_results = 1
    if query == "":
        return await eod(event, "__Please give a song name to search.__")
    dominator = await eor(event, f"__Searching for__ `{query}`")
    hel_ = await song_search(event, query, max_results, details=True)
    x, title, views, duration, thumb = hel_[0], hel_[1], hel_[2], hel_[3], hel_[4]
    thumb_name = f'thumb{ForGo10God}.jpg'
    thumbnail = requests.get(thumb, allow_redirects=True)
    open(thumb_name, 'wb').write(thumbnail.content)
    url = x.replace("\n", "")
    try:
        await dominator.edit("**Fetching Song**")
        with YoutubeDL(song_opts) as somg:
            dominator_data = somg.extract_info(url)
    except DownloadError as DE:
        return await eod(dominator, f"`{str(DE)}`")
    except ContentTooShortError:
        return await eod(dominator, "`The download content was too short.`")
    except GeoRestrictedError:
        return await eod(dominator, "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`")
    except MaxDownloadsReached:
        return await eod(dominator, "`Max-downloads limit has been reached.`")
    except PostProcessingError:
        return await eod(dominator, "`There was an error during post processing.`")
    except UnavailableVideoError:
        return await eod(dominator, "`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        return await eod(dominator, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await eod(dominator, "`There was an error during info extraction.`")
    except Exception as e:
        return await eod(dominator, f"{str(type(e)): {str(e)}}")
    c_time = time.time()
    await dominator.edit(f"**🎶 Preparing to upload song 🎶 :** \n\n{dominator_data['title']} \n**By :** {dominator_data['uploader']}")
    await event.client.send_file(
        event.chat_id,
        f"{dominator_data['id']}.mp3",
        supports_streaming=True,
        caption=f"**✘ Song -** `{title}` \n**✘ Views -** `{views}` \n**✘ Duration -** `{duration}` \n\n**✘ By :** {dominator_mention}",
        thumb=thumb_name,
        attributes=[
            DocumentAttributeAudio(
                duration=int(dominator_data["duration"]),
                title=str(dominator_data["title"]),
                performer=perf,
            )
        ],
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "Uploading..", f"{dominator_data['title']}.mp3")
        ),
    )
    await dominator.delete()
    os.remove(f"{dominator_data['id']}.mp3")


@dominator_cmd(pattern="vsong(?:\s|$)([\s\S]*)")
async def _(event):
    xyz = await client_id(event)
    ForGo10God, dominator_mention = xyz[0], xyz[2]
    query = event.text[7:]
    max_results = 1
    if query == "":
        return await eod(event, "__Please give a song name to search.__")
    dominator = await eor(event, f"__Searching for__ `{query}`")
    hel_ = await song_search(event, query, max_results, details=True)
    x, title, views, duration, thumb = hel_[0], hel_[1], hel_[2], hel_[3], hel_[4]
    thumb_name = f'thumb{ForGo10God}.jpg'
    thumbnail = requests.get(thumb, allow_redirects=True)
    open(thumb_name, 'wb').write(thumbnail.content)
    url = x.replace("\n", "")
    try:
        await dominator.edit("**Fetching Video**")
        with YoutubeDL(video_opts) as somg:
            dominator_data = somg.extract_info(url)
    except DownloadError as DE:
        return await eod(dominator, f"`{str(DE)}`")
    except ContentTooShortError:
        return await eod(dominator, "`The download content was too short.`")
    except GeoRestrictedError:
        return await eod(dominator, "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`")
    except MaxDownloadsReached:
        return await eod(dominator, "`Max-downloads limit has been reached.`")
    except PostProcessingError:
        return await eod(dominator, "`There was an error during post processing.`")
    except UnavailableVideoError:
        return await eod(dominator, "`Media is not available in the requested format.`")
    except XAttrMetadataError as XAME:
        return await eod(dominator, f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        return await eod(dominator, "`There was an error during info extraction.`")
    except Exception as e:
        return await eod(dominator, f"{str(type(e)): {str(e)}}")
    c_time = time.time()
    await dominator.edit(f"**📺 Preparing to upload video 📺 :** \n\n{dominator_data['title']}\n**By :** {dominator_data['uploader']}")
    await event.client.send_file(
        event.chat_id,
        f"{dominator_data['id']}.mp4",
        supports_streaming=True,
        caption=f"**✘ Video :** `{title}` \n\n**✘ By :** {dominator_mention}",
        thumb=thumb_name,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "Uploading..", f"{dominator_data['title']}.mp4")
        ),
    )
    await dominator.delete()
    os.remove(f"{dominator_data['id']}.mp4")


@dominator_cmd(pattern="lyrics(?: |$)(.*)")
async def nope(kraken):
    dominator = kraken.text[8:]
    uwu = await eor(kraken, f"Searching lyrics for  `{dominator}` ...")
    if not dominator:
        if kraken.is_reply:
            (await kraken.get_reply_message()).message
        else:
            await eod(uwu, "Give song name to get lyrics...")
            return
    try:
        troll = await event.client.inline_query("iLyricsBot", f"{(deEmojify(dominator))}")
        owo = await troll[0].click(Config.LOGGER_ID)
        await asyncio.sleep(3)
        owo_id = owo.id
        lyri = await event.client.get_messages(entity=Config.LOGGER_ID, ids=owo_id)
        await event.client.send_message(kraken.chat_id, lyri)
        await uwu.delete()
        await owo.delete()
    except Exception as e:
        await uwu.edir(f"**ERROR !!** \n\n`{str(e)}`")


@dominator_cmd(pattern="lsong(?:\s|$)([\s\S]*)")
async def _(event):
    dominator_ = event.text[6:]
    xyz = await client_id(event)
    ForGo10God, dominator_mention = xyz[0], xyz[2]
    if dominator_ == "":
        return await eor(event, "Give a song name to search")
    dominator = await eor(event, f"Searching song `{dominator_}`")
    somg = await event.client.inline_query("Lybot", f"{(deEmojify(dominator_))}")
    if somg:
        fak = await somg[0].click(Config.LOGGER_ID)
        if fak:
            await event.client.send_file(
                event.chat_id,
                file=fak,
                caption=f"**Song by :** {dominator_mention}",
            )
        await dominator.delete()
        await fak.delete()
    else:
        await dominator.edit("**ERROR 404 :** __NOT FOUND__")


@dominator_cmd(pattern="wsong(?:\s|$)([\s\S]*)")
async def _(event):
    if not event.reply_to_msg_id:
        return await eor(event, "Reply to a mp3 file.")
    rply = await event.get_reply_message()
    chat = "@auddbot"
    dominator = await eor(event, "Trying to identify song...")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message("/start")
            second = await conv.get_response()
            third = await conv.send_message(rply)
            fourth = await conv.get_response()
            if not fourth.text.startswith("Audio received"):
                await dominator.edit(
                    "Error identifying audio."
                )
                await event.client.delete_messages(conv.chat_id, [first.id, second.id, third.id, fourth.id])
                return
            await dominator.edit("Processed...")
            fifth = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await dominator.edit("Please unblock @auddbot and try again")
    audio = f"**Song Name : **{fifth.text.splitlines()[0]}\n\n**Details : **__{fifth.text.splitlines()[2]}__"
    await dominator.edit(audio)
    await event.client.delete_messages(conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id])


@dominator_cmd(pattern="spotify(?:\s|$)([\s\S]*)")
async def _(event):
    text = event.text[9:]
    chat = "@spotifysavebot"
    if text == "":
        return await eod(event, "Give something to download from Spotify.")
    dominator = await eor(event, f"**Trying to download** `{text}` **from Spotify...**")
    async with event.client.conversation(chat) as conv:
        try:
            first = await conv.send_message("/start")
            second = await conv.get_response()
            somg = await event.client.inline_query("spotifysavebot", f"str: {(deEmojify(text))}")
            if somg:
                third = await somg[0].click(chat)
            else:
                return await eod(dominator, "**ERROR !!** __404 : NOT FOUND__")
            fourth = await conv.get_response()
            fifth = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            return await eod(dominator, f"Please unblock {chat} to use Spotify module.")
        except Exception as e:
            return await eod(dominator, f"**ERROR !!** \n\n{e}")
        await event.client.send_file(event.chat_id, file=fourth, caption="")
        await dominator.delete()
        await event.client.delete_messages(conv.chat_id, [first.id, second.id, third.id, fourth.id, fifth.id])


CmdHelp("songs").add_command(
  "song", "<song name>", "Downloads the song from YouTube."
).add_command(
  "vsong", "<song name>", "Downloads the Video Song from YouTube."
).add_command(
  "lsong", "<song name>", "Sends the searched song in current chat.", "lsong Alone"
).add_command(
  "wsong", "<reply to a song file>", "Searches for the details of replied mp3 song file and uploads it's details."
).add_command(
  "lyrics", "<song name>", "Gives the lyrics of that song.."
).add_command(
  "spotify", "<song name>", "Downloads the song from Spotify."
).add_info(
  "Songs & Lyrics."
).add_warning(
  "✅ Harmless Module."
).add()
