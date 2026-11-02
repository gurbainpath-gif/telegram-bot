import asyncio
import telethon
import os
import yt_dlp

# Optional Telegram voice-chat support. Install with: pip install -U py-tgcalls
try:
    from pytgcalls import PyTgCalls
    from pytgcalls.types import MediaStream, RecordStream, AudioQuality, VideoQuality
    PYTGCALLS_AVAILABLE = True
except ImportError:
    PyTgCalls = None
    MediaStream = None
    RecordStream = None
    PYTGCALLS_AVAILABLE = False
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

api_id = 35894337
api_hash = "b54bdac807e91707ebf886596c79a053"

SMILEY_MESSAGES = [
  "Teri ma Kali randy 💔🦋",
    "Chal Ma Chuda mere se 🖕",
    "Chal smiley ko Baap Bol",
    "Teri ma mar du randyke 😂🦋",
    "KHAKE BURGUR TERI MA CHODU GHAR GHAR",
    "BAAP BOL MUJHE GAREEB KE BACCHE",
    "Teri ma bhooki randy",
    "Chal na gawar",
    "Hakla kyun rha tu😂",
    "teri maa ke bhosde khol dunga randyke",
    "𝐀ᴘɴɪ 𝐀ᴜᴋᴀᴛ ᴅᴇᴋʜ ᴋᴜᴛᴛᴇ 🐕😂",
    "ѕмιℓєу🩷  𝐃ᴀᴅʏ ᴋᴀ 𝐆ᴜʟᴀᴀᴍ ʜᴀɪ ᴛᴜ 🥀😤",
    "𝐁ʜᴀɢ ʏᴀʜᴀɴ ꜱᴇ ᴋᴜᴛᴛᴇ ᴋᴇ ᴘɪʟʟᴇ 🐕💨",
    "𝐆ᴜʟᴀᴀᴍ ʜᴇɪ ᴛᴜ ᴍᴇʀᴀ ᴀʙ ᴀᴜʀ ʀᴀʜᴇɢᴀ ʙʜɪ 👑😎",
    "𝐀ᴡᴀᴢ 𝐍ɪᴄʜᴇ 𝐆ᴜʟᴀᴀᴍ 🤢👇🏻",
"teri maa ka moan start karwa",
"tmkc mei nature🌲🌳🪾🌴🌵🪴🍀☘️🍃🌱🌿",
"teri maa ko 69 ke pose mei chodunga",
"ey sun tohar maiya ka chodu",
"teri maa ka bhosda on fire",
"teri maa or bhen satrangi randy",
"teri maa ka bhosda h ya india gate sala hmesa khula hi rhta hai",
"teri bhen ki bur faad denge chote",
"garib ke ladke chota likh apni aukat jitna",
"tu mujhe swipe krta rah gya or mene waha teri behen xhod di",
"teri maa ka market mei rape kr dunga"
"teri maa mere lund ki diwani",
"Tʀɪ Mᴀᴄᴏ Esᴀ Cᴏᴅᴜɴɢʜᴀ Pᴀᴅᴏsʜɪ Sᴏᴄʜᴇɴɢᴇ Cᴜᴅᴀɪ Cʜʟʀɪ Yᴀ Sɪʟᴀɪ Mᴀᴄʜɪɴᴇ😂🙏🏿😂🙏🏿😂🙏🏿😂🙏🏿😂🙏🏿",
"☄►♘ / 𝟮 लन्ड अंदर , FIR 𝗞𝗜 𝗠𝗔𝗔 𝗕𝗔𝗡𝗜 सिकंदर 🏳️⚧️💢",
"𝘼𝘼𝙅 𝙃𝙊 𝙃𝙄 𝙅𝘼𝙔𝙀 𝘼𝘼𝙍 𝙔𝘼 𝙋𝘼𝘼𝙍 𝙇𝙂𝘼 𝙏𝙀𝙍𝙄 𝙈𝘼𝙆𝙀 𝘾𝙃𝙐𝙏𝙏𝘼𝘿𝙊 𝙈𝙀 𝘿𝙃𝘼𝘼𝙍 🤣👊🏻🤣👊🏻🤣👊🏻🤣👊🏻",
"𝘙𝘌𝘗𝘌𝘈𝘛 𝘗𝘌 𝘔𝘈 𝘊𝘏𝘜𝘋𝘈𝘕𝘈 𝘉𝘈𝘕𝘋 𝘒𝘈𝘙 टेप रिकॉर्डर🤣😂🙏🤣😂🙏🤣😂🙏🤣😂🙏🤣😂🙏🤣😂🙏🤣😂🙏",
"chup randyce pille",
"𝐌������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������������𝘛𝘌𝘙𝘐 𝘔𝘈𝘈 𝘚𝘐𝘙𝘍 SMILEY  - کین 𝘚𝘌 𝘏𝘐 𝘊𝘏𝘜𝘋 𝘚𝘈𝘒𝘛𝘪 𝘏𝘈𝘪 😈🔥",
"teri maa sirf smiley se hi cudegi",
]
SESSION_NAME = os.environ.get("TELEGRAM_SESSION", "session_1")

active_smiley_loops = {}
original_profile = {}
auto_react_emoji = None
live_forwards = {}
muted_users = {}
active_sp_loops = {}
active_reply_modes = {}
sub_users = set()   # user IDs granted bot access by the owner
owner_id = None     # set at startup
safe_users = {}     # {chat_id: set(user_ids)} — exempt from deletion
voice_call = None
active_recordings = {}   # {chat_id: recording file path}
active_media = {}        # {chat_id: current downloaded media path}
active_media_title = {}  # {chat_id: current media title}


async def main():
    global owner_id
    print(f"🚀 Starting bot with session: {SESSION_NAME}")
    async with TelegramClient(SESSION_NAME, api_id, api_hash) as client:

        me = await client.get_me()
        owner_id = me.id
        print(f"✅ Logged in as {me.first_name} (ID: {owner_id})")

        global voice_call
        if PYTGCALLS_AVAILABLE:
            try:
                voice_call = PyTgCalls(client)
                await voice_call.start()
                print("📞 PyTgCalls voice-chat engine started.")
            except Exception as e:
                voice_call = None
                print(f"⚠️ PyTgCalls could not start: {e}")
        else:
            print("⚠️ PyTgCalls is not installed. Voice-chat commands are disabled.")

        # ── helpers ──────────────────────────────────────────────────────────

        def is_authorized(event):
            return event.out or event.sender_id in sub_users

        async def respond(event, text):
            """Edit if owner sent the command; otherwise delete their msg and reply."""
            if event.out:
                await event.edit(text)
            else:
                try:
                    await event.delete()
                except Exception:
                    pass
                await client.send_message(event.chat_id, text)

        # ── passive / enforcement handlers ───────────────────────────────────

        @client.on(events.NewMessage())
        async def mute_enforcement_handler(event):
            global muted_users
            chat_id = event.chat_id
            user_id = event.sender_id
            if event.out:
                return
            if user_id and chat_id in safe_users and user_id in safe_users[chat_id]:
                return
            is_muted = False
            if chat_id in muted_users:
                if user_id and user_id in muted_users[chat_id]:
                    is_muted = True
                elif chat_id in muted_users[chat_id]:
                    is_muted = True
            if is_muted:
                try:
                    await event.delete()
                except Exception as e:
                    print(f"⚠️ Mute delete error in {chat_id}: {e}")

        @client.on(events.NewMessage())
        async def live_forward_handler(event):
            global live_forwards
            if event.chat_id in live_forwards and not event.out:
                for target_id in live_forwards[event.chat_id]:
                    try:
                        await client.forward_messages(target_id, event.message)
                    except Exception as e:
                        print(f"⚠️ Live forward error from {event.chat_id} to {target_id}: {e}")

        @client.on(events.NewMessage())
        async def auto_react_handler(event):
            global auto_react_emoji
            if auto_react_emoji and event.out:
                try:
                    await client(
                        telethon.functions.messages.SendReactionRequest(
                            peer=event.input_chat,
                            msg_id=event.id,
                            reaction=[
                                telethon.tl.types.ReactionEmoji(emoticon=auto_react_emoji)
                            ]
                        )
                    )
                except telethon.errors.FloodWaitError as e:
                    print(f"⏳ Reaction flood wait: {e.seconds}s — pausing auto-react")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    print(f"Reaction error: {e}")

        @client.on(events.NewMessage())
        async def sp_delete_handler(event):
            chat_id = event.chat_id
            if not active_sp_loops.get(chat_id, False):
                return
            if event.out:
                return
            if event.sender_id and chat_id in safe_users and event.sender_id in safe_users[chat_id]:
                return
            try:
                await event.delete()
            except Exception as e:
                print(f"⚠️ SP delete error: {e}")

        @client.on(events.NewMessage())
        async def auto_reply_handler(event):
            if event.out:
                return
            chat_id = event.chat_id
            user_id = event.sender_id
            if chat_id not in active_reply_modes:
                return
            if user_id not in active_reply_modes[chat_id]:
                return
            reply_text = active_reply_modes[chat_id][user_id]
            try:
                await client.send_message(chat_id, reply_text, reply_to=event.id)
            except telethon.errors.FloodWaitError as e:
                print(f"⏳ Auto-reply flood wait: {e.seconds}s")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"⚠️ Auto-reply error: {e}")

        # ── owner-only: sub-user management ──────────────────────────────────

        @client.on(events.NewMessage(pattern=r"√sub", outgoing=True))
        async def sub_handler(event):
            if "√antisub" in event.message.message:
                return  # let antisub_handler handle it
            if not event.is_reply:
                await event.edit("❌ Reply to someone's message to grant them bot access.")
                return
            reply_msg = await event.get_reply_message()
            target_id = reply_msg.sender_id
            if target_id == owner_id:
                await event.edit("⚠️ That's you — you already own the bot.")
                return
            sub_users.add(target_id)
            name = getattr(reply_msg.sender, 'first_name', None) or str(target_id)
            await event.edit(f"✅ {name} can now use the bot.\nTotal sub-users: {len(sub_users)}")

        @client.on(events.NewMessage(pattern=r"√antisub", outgoing=True))
        async def antisub_handler(event):
            target_id = None
            name = None
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                target_id = reply_msg.sender_id
                name = getattr(reply_msg.sender, 'first_name', None) or str(target_id)
            else:
                args = event.message.message.split()
                if len(args) > 1:
                    username = args[1].replace("@", "")
                    try:
                        user = await client.get_entity(username)
                        target_id = user.id
                        name = getattr(user, 'first_name', None) or username
                    except Exception as e:
                        await event.edit(f"❌ Could not find user: {e}")
                        return
                else:
                    await event.edit("❌ Reply to a message or use: √antisub @username")
                    return
            if target_id in sub_users:
                sub_users.discard(target_id)
                await event.edit(f"🚫 {name}'s bot access has been removed.\nTotal sub-users: {len(sub_users)}")
            else:
                await event.edit(f"⚠️ {name} didn't have bot access.")

        # ── safe mode ────────────────────────────────────────────────────────

        @client.on(events.NewMessage(pattern=r"√safe"))
        async def safe_handler(event):
            if not is_authorized(event):
                return
            if "√unsafe" in event.message.message:
                return
            if not event.is_reply:
                await respond(event, "❌ Reply to someone's message to add them to safe mode.")
                return
            reply_msg = await event.get_reply_message()
            target_id = reply_msg.sender_id
            chat_id = event.chat_id
            if chat_id not in safe_users:
                safe_users[chat_id] = set()
            safe_users[chat_id].add(target_id)
            name = getattr(reply_msg.sender, 'first_name', None) or str(target_id)
            await respond(event, f"🛡 {name} is now in safe mode — their messages won't be deleted.")

        @client.on(events.NewMessage(pattern=r"√unsafe"))
        async def unsafe_handler(event):
            if not is_authorized(event):
                return
            target_id = None
            name = None
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                target_id = reply_msg.sender_id
                name = getattr(reply_msg.sender, 'first_name', None) or str(target_id)
            else:
                args = event.message.message.split()
                if len(args) > 1:
                    username = args[1].replace("@", "")
                    try:
                        user = await client.get_entity(username)
                        target_id = user.id
                        name = getattr(user, 'first_name', None) or username
                    except Exception as e:
                        await respond(event, f"❌ Could not find user: {e}")
                        return
                else:
                    await respond(event, "❌ Reply to a message or use: √unsafe @username")
                    return
            chat_id = event.chat_id
            if chat_id in safe_users and target_id in safe_users[chat_id]:
                safe_users[chat_id].discard(target_id)
                await respond(event, f"⚠️ {name} removed from safe mode — deletions apply again.")
            else:
                await respond(event, f"⚠️ {name} wasn't in safe mode.")

        # ── command handlers (owner + sub-users) ─────────────────────────────

        @client.on(events.NewMessage(pattern="√react"))
        async def react_command_handler(event):
            if not is_authorized(event):
                return
            global auto_react_emoji
            text = event.message.message.replace("√react", "").strip()
            if not text:
                auto_react_emoji = None
                await respond(event, "🛑 Auto-react disabled.")
            else:
                auto_react_emoji = text
                await respond(event, f"✅ Auto-react enabled with {auto_react_emoji}")

        @client.on(events.NewMessage(pattern="√forward"))
        async def forward_handler(event):
            if not is_authorized(event):
                return
            global live_forwards
            args = event.message.message.split()
            if len(args) < 2:
                await respond(event, "❌ Usage: √forward [source_link]")
                return
            source_link = args[1]
            target_chat_id = event.chat_id
            try:
                source_entity = await client.get_entity(source_link)
                source_id = source_entity.id
                if source_id not in live_forwards:
                    live_forwards[source_id] = []
                if target_chat_id not in live_forwards[source_id]:
                    live_forwards[source_id].append(target_chat_id)
                    await respond(event, f"✅ Live sync enabled from {source_link} to this chat.")
                else:
                    await respond(event, f"⚠️ Sync already active for {source_link} here.")
            except Exception as e:
                print(f"⚠️ Live sync setup error: {e}")
                await respond(event, f"❌ Error: {e}")

        @client.on(events.NewMessage(pattern=r"^√song(?:\s+|$)"))
        async def song_handler(event):
            if not is_authorized(event):
                return

            song_name = event.message.message[len("√song"):].strip()
            if not song_name:
                await respond(event, "❌ Use: √song <song name or YouTube URL>")
                return

            await respond(event, f"🎵 Searching and downloading: {song_name}...")
            file_base = f"temp_song_{event.id}"

            ydl_opts = {
                "format": "bestaudio[ext=m4a]/bestaudio/best",
                "outtmpl": f"{file_base}.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "128",
                }],
                "default_search": "ytsearch1",
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
                "nocheckcertificate": True,
                "retries": 3,
                "fragment_retries": 3,
                "extractor_retries": 3,
                "socket_timeout": 20,
                "concurrent_fragment_downloads": 3,
                "no_color": True,
            }

            try:
                # Search first, then download the selected result.
                query = song_name if song_name.startswith(("http://", "https://")) else f"ytsearch1:{song_name}"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(query, download=True)

                if not info:
                    raise RuntimeError("yt-dlp returned no result")

                # ytsearch returns a playlist-like result; direct URLs return a video dict.
                if "entries" in info:
                    entries = [entry for entry in info.get("entries", []) if entry]
                    if not entries:
                        raise RuntimeError("No playable result found")
                    video_info = entries[0]
                else:
                    video_info = info

                file_path = f"{file_base}.mp3"
                if not os.path.exists(file_path):
                    # FFmpeg can keep the original extension in some cases.
                    candidates = [
                        f"{file_base}.m4a",
                        f"{file_base}.webm",
                        f"{file_base}.opus",
                        f"{file_base}.mp4",
                    ]
                    source_file = next((x for x in candidates if os.path.exists(x)), None)
                    if source_file:
                        file_path = source_file
                    else:
                        raise RuntimeError("Download completed but no audio file was created")

                try:
                    await client.send_file(
                        event.chat_id,
                        file_path,
                        voice_note=True,
                        reply_to=event.reply_to_msg_id,
                        attributes=[
                            telethon.tl.types.DocumentAttributeAudio(
                                duration=int(video_info.get("duration") or 0),
                                title=video_info.get("title") or song_name,
                                performer=video_info.get("uploader") or "Unknown",
                            )
                        ],
                    )
                except telethon.errors.rpcerrorlist.ChatSendAudiosForbiddenError:
                    await client.send_file(
                        event.chat_id,
                        file_path,
                        force_document=True,
                        reply_to=event.reply_to_msg_id,
                    )

                try:
                    await event.delete()
                except Exception:
                    pass

            except Exception as e:
                error_text = str(e)
                print(f"⚠️ Song error: {error_text}")

                if "Sign in to confirm" in error_text or "not a bot" in error_text.lower():
                    msg = (
                        "❌ YouTube ne is request ko block kar diya.\n"
                        "Try a different song/URL, ya VPS par valid yt-dlp cookies configure karo."
                    )
                elif "Video unavailable" in error_text or "not available" in error_text.lower():
                    msg = "❌ Ye video available nahi hai ya region/restriction laga hua hai."
                else:
                    msg = f"❌ Song download failed: {error_text[:350]}"

                await respond(event, msg)

            finally:
                # Clean all temporary audio variants.
                for ext in ("mp3", "m4a", "webm", "opus", "mp4", "part", "ytdl"):
                    temp = f"{file_base}.{ext}"
                    try:
                        if os.path.exists(temp):
                            os.remove(temp)
                    except Exception:
                        pass

        @client.on(events.NewMessage(pattern="√clonejutsu", outgoing=True))
        async def clone_handler(event):
            args = event.message.message.split()
            target_user = None
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                target_user = await client.get_entity(reply_msg.sender_id)
            elif len(args) > 1:
                username = args[1].replace("@", "")
                try:
                    target_user = await client.get_entity(username)
                except Exception as e:
                    await event.edit(f"❌ Could not find user: {e}")
                    return
            else:
                await event.edit("❌ Reply to a message or provide a username/ID after √clonejutsu")
                return
            print(f"👤 Cloning account: {getattr(target_user, 'first_name', 'Unknown')}")
            try:
                me = await client.get_me()
                full_me = await client(telethon.functions.users.GetFullUserRequest(me))
                if not original_profile:
                    my_photos = await client.get_profile_photos('me')
                    original_profile['first_name'] = me.first_name or ""
                    original_profile['last_name'] = me.last_name or ""
                    original_profile['about'] = full_me.full_user.about or ""
                    original_profile['photo'] = await client.download_media(my_photos[0]) if my_photos else None
                full_target = await client(telethon.functions.users.GetFullUserRequest(target_user))
                about = full_target.full_user.about or ""
                await client(
                    UpdateProfileRequest(
                        first_name=target_user.first_name or "",
                        last_name=target_user.last_name or "",
                        about=about
                    )
                )
                photos = await client.get_profile_photos(target_user)
                if photos:
                    my_photos = await client.get_profile_photos('me')
                    if my_photos:
                        await client(DeletePhotosRequest(id=my_photos))
                    path = await client.download_media(photos[0])
                    await client(UploadProfilePhotoRequest(file=await client.upload_file(path)))
                    if os.path.exists(path):
                        os.remove(path)
                if event.is_channel:
                    try:
                        permissions = await client.get_permissions(event.chat_id, 'me')
                        if permissions.is_admin:
                            await client(
                                telethon.tl.functions.channels.EditAdminRequest(
                                    channel=event.chat_id,
                                    user_id='me',
                                    admin_rights=telethon.tl.types.ChatAdminRights(
                                        post_messages=True,
                                        anonymous=True
                                    ),
                                    rank='Admin'
                                )
                            )
                    except Exception as e:
                        print(f"⚠️ Anonymous admin error: {e}")
                await event.edit("Summon successfull 🤍🦋")
            except Exception as e:
                print(f"⚠️ Cloning error: {e}")
                await event.edit(f"❌ Error: {e}")

        @client.on(events.NewMessage(pattern="√back", outgoing=True))
        async def back_handler(event):
            if not original_profile:
                await event.edit("❌ No profile backup found.")
                return
            await event.edit("🔄 Reverting profile...")
            try:
                await client(
                    UpdateProfileRequest(
                        first_name=original_profile.get('first_name', ""),
                        last_name=original_profile.get('last_name', ""),
                        about=original_profile.get('about', "")
                    )
                )
                if original_profile.get('photo'):
                    my_photos = await client.get_profile_photos('me')
                    if my_photos:
                        await client(DeletePhotosRequest(id=my_photos))
                    await client(UploadProfilePhotoRequest(
                        file=await client.upload_file(original_profile['photo'])
                    ))
                await event.edit("✅ Profile restored!")
            except Exception as e:
                print(f"⚠️ Revert error: {e}")
                await event.edit(f"❌ Error: {e}")

        # ── voice chat / recording ─────────────────────────────────────────────

        @client.on(events.NewMessage(pattern=r"^√callfight(?:\s+.*)?$"))
        async def callfight_handler(event):
            if not is_authorized(event):
                return
            if not (event.is_group or event.is_channel):
                await respond(event, "❌ √callfight only works in groups/channels.")
                return
            if not PYTGCALLS_AVAILABLE or voice_call is None:
                await respond(event, "❌ Voice-chat support missing. Install: pip install -U py-tgcalls")
                return
            chat_id = event.chat_id
            try:
                # Join an existing Telegram voice chat without playing any media.
                await voice_call.record(chat_id, RecordStream(audio="/dev/null"))
                await respond(event, "📞 Voice chat joined successfully.")
            except Exception as e:
                await respond(event, f"❌ Could not join voice chat: {e}")

        @client.on(events.NewMessage(pattern=r"^√stopcallfight$"))
        async def stopcallfight_handler(event):
            if not is_authorized(event):
                return
            if voice_call is None:
                await respond(event, "❌ Voice-chat engine is not running.")
                return
            try:
                await voice_call.leave_call(event.chat_id)
                active_recordings.pop(event.chat_id, None)
                await respond(event, "📞 Voice chat left.")
            except Exception as e:
                await respond(event, f"❌ Could not leave voice chat: {e}")

        async def _download_vc_media(search_text, event_id, video=False):
            """Download one YouTube result for VC playback."""
            file_base = f"temp_vc_{event_id}"
            if video:
                fmt = "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
                outtmpl = f"{file_base}.%(ext)s"
                post = [{
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }]
            else:
                fmt = "bestaudio[ext=m4a]/bestaudio/best"
                outtmpl = f"{file_base}.%(ext)s"
                post = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "128",
                }]

            opts = {
                "format": fmt,
                "outtmpl": outtmpl,
                "postprocessors": post,
                "default_search": "ytsearch1",
                "noplaylist": True,
                "quiet": True,
                "no_warnings": True,
                "nocheckcertificate": True,
                "retries": 3,
                "fragment_retries": 3,
                "extractor_retries": 3,
                "socket_timeout": 20,
                "no_color": True,
                "merge_output_format": "mp4" if video else None,
            }
            opts = {k: v for k, v in opts.items() if v is not None}
            query = search_text if search_text.startswith(("http://", "https://")) else f"ytsearch1:{search_text}"
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(query, download=True)
            if not info:
                raise RuntimeError("yt-dlp returned no result")
            if "entries" in info:
                entries = [e for e in info.get("entries", []) if e]
                if not entries:
                    raise RuntimeError("No playable result found")
                info = entries[0]
            candidates = []
            if video:
                candidates = [f"{file_base}.mp4", f"{file_base}.mkv", f"{file_base}.webm"]
            else:
                candidates = [f"{file_base}.mp3", f"{file_base}.m4a", f"{file_base}.webm", f"{file_base}.opus"]
            path = next((x for x in candidates if os.path.exists(x)), None)
            if not path:
                raise RuntimeError("Download completed but no media file was created")
            return path, (info.get("title") or search_text)

        async def _cleanup_vc_media(chat_id):
            path = active_media.pop(chat_id, None)
            active_media_title.pop(chat_id, None)
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass

        @client.on(events.NewMessage(pattern=r"^√play(?:\s+|$)"))
        async def vc_play_handler(event):
            if not is_authorized(event):
                return
            if not (event.is_group or event.is_channel):
                await respond(event, "❌ √play only works in groups/channels.")
                return
            if not PYTGCALLS_AVAILABLE or voice_call is None:
                await respond(event, "❌ Voice-chat support missing. Install: pip install -U py-tgcalls")
                return
            query = event.message.message[len("√play"):].strip()
            if not query:
                await respond(event, "❌ Use: √play <song name or YouTube URL>")
                return
            await respond(event, f"🎵 VC search: {query}...")
            chat_id = event.chat_id
            try:
                await _cleanup_vc_media(chat_id)
                path, title = await _download_vc_media(query, event.id, video=False)
                await voice_call.play(chat_id, MediaStream(path, AudioQuality.HIGH))
                active_media[chat_id] = path
                active_media_title[chat_id] = title
                await respond(event, f"🎵 Now playing in VC:\n{title}")
            except Exception as e:
                await respond(event, f"❌ VC audio playback failed: {e}")

        @client.on(events.NewMessage(pattern=r"^√vplay(?:\s+|$)"))
        async def vc_vplay_handler(event):
            if not is_authorized(event):
                return
            if not (event.is_group or event.is_channel):
                await respond(event, "❌ √vplay only works in groups/channels.")
                return
            if not PYTGCALLS_AVAILABLE or voice_call is None:
                await respond(event, "❌ Voice-chat support missing. Install: pip install -U py-tgcalls")
                return
            query = event.message.message[len("√vplay"):].strip()
            if not query:
                await respond(event, "❌ Use: √vplay <video name or YouTube URL>")
                return
            await respond(event, f"🎬 VC video search: {query}...")
            chat_id = event.chat_id
            try:
                await _cleanup_vc_media(chat_id)
                path, title = await _download_vc_media(query, event.id, video=True)
                await voice_call.play(chat_id, MediaStream(path, AudioQuality.HIGH, VideoQuality.HD_720p))
                active_media[chat_id] = path
                active_media_title[chat_id] = title
                await respond(event, f"🎬 Now playing video in VC:\n{title}")
            except Exception as e:
                await respond(event, f"❌ VC video playback failed: {e}")

        @client.on(events.NewMessage(pattern=r"^√skip$"))
        async def vc_skip_handler(event):
            if not is_authorized(event):
                return
            if voice_call is None:
                await respond(event, "❌ Voice-chat engine is not running.")
                return
            if event.chat_id not in active_media:
                await respond(event, "❌ Nothing is playing in VC.")
                return
            try:
                await voice_call.leave_call(event.chat_id)
                await _cleanup_vc_media(event.chat_id)
                await respond(event, "⏭️ Current VC media skipped.")
            except Exception as e:
                await respond(event, f"❌ Could not skip media: {e}")

        @client.on(events.NewMessage(pattern=r"^√recording(?:\s+|$)"))
        async def recording_handler(event):
            if not is_authorized(event):
                return
            if not (event.is_group or event.is_channel):
                await respond(event, "❌ √recording only works in groups/channels.")
                return
            if not PYTGCALLS_AVAILABLE or voice_call is None:
                await respond(event, "❌ Voice-chat support missing. Install: pip install -U py-tgcalls")
                return
            recording_name = event.message.message[len("√recording"):].strip()
            if not recording_name:
                await respond(event, "❌ Use: √recording <audio-file-path-or-URL>")
                return
            chat_id = event.chat_id
            try:
                await voice_call.play(chat_id, MediaStream(recording_name))
                await respond(event, f"🎵 Recording playback started: {recording_name}")
            except Exception as e:
                await respond(event, f"❌ Recording playback failed: {e}")

        @client.on(events.NewMessage(pattern=r"^√stoprecording$"))
        async def stoprecording_handler(event):
            if not is_authorized(event):
                return
            if voice_call is None:
                await respond(event, "❌ Voice-chat engine is not running.")
                return
            try:
                await voice_call.leave_call(event.chat_id)
                active_recordings.pop(event.chat_id, None)
                await respond(event, "⏹️ Recording playback stopped.")
            except Exception as e:
                await respond(event, f"❌ Could not stop recording playback: {e}")

        @client.on(events.NewMessage(pattern=r"^√record(?:\s+|$)"))
        async def record_handler(event):
            if not is_authorized(event):
                return
            if not (event.is_group or event.is_channel):
                await respond(event, "❌ √record only works in groups/channels.")
                return
            if not PYTGCALLS_AVAILABLE or voice_call is None:
                await respond(event, "❌ Voice-chat support missing. Install: pip install -U py-tgcalls")
                return
            name = event.message.message[len("√record"):].strip() or f"voice_record_{event.chat_id}.mp3"
            if not name.endswith((".mp3", ".wav", ".raw", ".ogg")):
                name += ".mp3"
            path = os.path.abspath(name)
            try:
                await voice_call.record(event.chat_id, RecordStream(audio=path))
                active_recordings[event.chat_id] = path
                await respond(event, f"🔴 Voice recording started.\nFile: {path}\nUse √stoprecord to finish.")
            except Exception as e:
                await respond(event, f"❌ Recording could not start: {e}")

        @client.on(events.NewMessage(pattern=r"^√stoprecord$"))
        async def stoprecord_handler(event):
            if not is_authorized(event):
                return
            if voice_call is None:
                await respond(event, "❌ Voice-chat engine is not running.")
                return
            path = active_recordings.pop(event.chat_id, None)
            try:
                await voice_call.leave_call(event.chat_id)
                if path and os.path.exists(path):
                    await respond(event, f"⏹️ Recording stopped.\nSaved: {path}")
                else:
                    await respond(event, "⏹️ Recording stopped.")
            except Exception as e:
                await respond(event, f"❌ Could not stop recording: {e}")

        MENU_TEXT = """
𝐕͟ɪ꯭ʀ꯭ᴀ꯭ᴛ꯭ 🤍

🌷 𝐒͟ᴘ꯭ᴀ꯭ᴍ꯭
 · √smiley 🦋  𝐒͟ᴘ꯭ᴀ꯭ᴍ꯭ ꯭𝐒͟ᴏ꯭ᴍ꯭ᴇ꯭ᴏ꯭ɴ꯭ᴇ꯭
 · √reply 🌸  𝐀͟ᴜ꯭ᴛ꯭ᴏ꯭ 𝐑͟ᴇ꯭ᴘ꯭ʟ꯭ʏ꯭
 · √stop 🍂   𝐒͟ᴛ꯭ᴏ꯭ᴘ꯭ 𝐄͟ᴠ꯭ᴇ꯭ʀ꯭ʏ꯭ᴛ꯭ʜ꯭ɪ꯭ɴ꯭ɢ꯭

🌷 𝐌͟ᴇ꯭ᴅ꯭ɪ꯭ᴀ꯭
 · √song 🎵   𝐒͟ᴇ꯭ɴ꯭ᴅ꯭ 𝐀͟ 𝐒͟ᴏ꯭ɴ꯭ɢ꯭
 · √play 🎧   𝐏͟ʟ꯭ᴀ꯭ʏ꯭ 𝐒͟ᴏ꯭ɴ꯭ɢ꯭ 𝐈͟ɴ꯭ 𝐕͟ᴄ꯭
 · √vplay 🎬   𝐏͟ʟ꯭ᴀ꯭ʏ꯭ 𝐕͟ɪ꯭ᴅ꯭ᴇ꯭ᴏ꯭ 𝐈͟ɴ꯭ 𝐕͟ᴄ꯭
 · √skip ⏭️   𝐒͟ᴋ꯭ɪ꯭ᴘ꯭ 𝐂͟ᴜ꯭ʀ꯭ʀ꯭ᴇ꯭ɴ꯭ᴛ꯭ 𝐕͟ᴄ꯭ 𝐌͟ᴇ꯭ᴅ꯭ɪ꯭ᴀ꯭

🌷 𝐕͟ᴏ꯭ɪ꯭ᴄ꯭ᴇ꯭ 𝐂͟ʜ꯭ᴀ꯭ᴛ꯭
 · √callfight 📞   𝐉͟ᴏ꯭ɪ꯭ɴ꯭ 𝐕͟ᴏ꯭ɪ꯭ᴄ꯭ᴇ꯭ 𝐂͟ʜ꯭ᴀ꯭ᴛ꯭
 · √stopcallfight 📵   𝐋͟ᴇ꯭ᴀ꯭ᴠ꯭ᴇ꯭ 𝐕͟ᴏ꯭ɪ꯭ᴄ꯭ᴇ꯭ 𝐂͟ʜ꯭ᴀ꯭ᴛ꯭
 · √recording 🎵   𝐏͟ʟ꯭ᴀ꯭ʏ꯭ 𝐑͟ᴇ꯭ᴄ꯭ᴏ꯭ʀ꯭ᴅ꯭ɪ꯭ɴ꯭ɢ꯭
 · √stoprecording ⏹️   𝐒͟ᴛ꯭ᴏ꯭ᴘ꯭ 𝐏͟ʟ꯭ᴀ꯭ʏ꯭ʙ꯭ᴀ꯭ᴄ꯭ᴋ꯭
 · √record 🔴   𝐑͟ᴇ꯭ᴄ꯭ᴏ꯭ʀ꯭ᴅ꯭ 𝐕͟ᴏ꯭ɪ꯭ᴄ꯭ᴇ꯭ 𝐂͟ʜ꯭ᴀ꯭ᴛ꯭
 · √stoprecord ⏹️   𝐒͟ᴛ꯭ᴏ꯭ᴘ꯭ 𝐑͟ᴇ꯭ᴄ꯭ᴏ꯭ʀ꯭ᴅ꯭ɪ꯭ɴ꯭ɢ꯭

🌷 𝐂͟ʜ꯭ᴀ꯭ᴛ꯭
 · √mute 🤫   𝐌͟ᴜ꯭ᴛ꯭ᴇ꯭ 𝐀͟ 𝐔͟s꯭ᴇ꯭ʀ꯭
 · √sp 🗑     𝐃͟ᴇ꯭ʟ꯭ᴇ꯭ᴛ꯭ᴇ꯭ 𝐈͟ɴ꯭ᴄ꯭ᴏ꯭ᴍ꯭ɪ꯭ɴ꯭ɢ꯭
 · √react 💫  𝐀͟ᴜ꯭ᴛ꯭ᴏ꯭ 𝐑͟ᴇ꯭ᴀ꯭ᴄ꯭ᴛ꯭
 · √forward 🔗  𝐋͟ɪ꯭ᴠ꯭ᴇ꯭ 𝐅͟ᴏ꯭ʀ꯭ᴡ꯭ᴀ꯭ʀ꯭ᴅ꯭

🌷 𝐀͟ᴅ꯭ᴍ꯭ɪ꯭ɴ꯭
 · √admin 👑  𝐆͟ɪ꯭ᴠ꯭ᴇ꯭ 𝐀͟ᴅ꯭ᴍ꯭ɪ꯭ɴ꯭
 · √take 🚫   𝐑͟ᴇ꯭ᴍ꯭ᴏ꯭ᴠ꯭ᴇ꯭ 𝐀͟ᴅ꯭ᴍ꯭ɪ꯭ɴ꯭
 · √kick 👢   𝐊͟ɪ꯭ᴄ꯭ᴋ꯭ 𝐔͟s꯭ᴇ꯭ʀ꯭
 · √add 🤖    𝐀͟ᴅ꯭ᴅ꯭ 𝐁͟ᴏ꯭ᴛ꯭s꯭

🌷 𝐏͟ʀ꯭ᴏ꯭ғ꯭ɪ꯭ʟ꯭ᴇ꯭
 · √clonejutsu 🌙  𝐂͟ʟ꯭ᴏ꯭ɴ꯭ᴇ꯭ 𝐏͟ʀ꯭ᴏ꯭ғ꯭ɪ꯭ʟ꯭ᴇ꯭
 · √back 🌿   𝐑͟ᴇ꯭s꯭ᴛ꯭ᴏ꯭ʀ꯭ᴇ꯭ 𝐏͟ʀ꯭ᴏ꯭ғ꯭ɪ꯭ʟ꯭ᴇ꯭

🌷 𝐀͟ᴄ꯭ᴄ꯭ᴇ꯭ss꯭
 · √sub 🤍    𝐆͟ɪ꯭ᴠ꯭ᴇ꯭ 𝐀͟ᴄ꯭ᴄ꯭ᴇ꯭ss꯭
 · √antisub 🖤  𝐑͟ᴇ꯭ᴠ꯭ᴏ꯭ᴋ꯭ᴇ꯭ 𝐀͟ᴄ꯭ᴄ꯭ᴇ꯭ss꯭

🌷 𝐒͟ᴀ꯭ғ꯭ᴇ꯭
 · √safe 🛡   𝐏͟ʀ꯭ᴏ꯭ᴛ꯭ᴇ꯭ᴄ꯭ᴛ꯭ 𝐀͟ 𝐔͟s꯭ᴇ꯭ʀ꯭'꯭s꯭ 𝐌͟s꯭ɢ꯭s꯭
 · √unsafe 🌸  𝐑͟ᴇ꯭ᴍ꯭ᴏ꯭ᴠ꯭ᴇ꯭ 𝐏͟ʀ꯭ᴏ꯭ᴛ꯭ᴇ꯭ᴄ꯭ᴛ꯭ɪ꯭ᴏ꯭ɴ꯭

""".strip()

        @client.on(events.NewMessage(pattern="√menu"))
        async def menu_handler(event):
            if not is_authorized(event):
                return
            await respond(event, MENU_TEXT)

        @client.on(events.NewMessage(pattern="√stop"))
        async def stop_handler(event):
            if not is_authorized(event):
                return
            global auto_react_emoji, live_forwards, muted_users
            chat_id = event.chat_id
            stopped_anything = False
            if chat_id in active_smiley_loops and active_smiley_loops[chat_id]:
                active_smiley_loops[chat_id] = False
                stopped_anything = True
            if chat_id in active_sp_loops and active_sp_loops[chat_id]:
                active_sp_loops[chat_id] = False
                stopped_anything = True
            if auto_react_emoji:
                auto_react_emoji = None
                stopped_anything = True
            for source_id in list(live_forwards.keys()):
                if chat_id in live_forwards[source_id]:
                    live_forwards[source_id].remove(chat_id)
                    if not live_forwards[source_id]:
                        del live_forwards[source_id]
                    stopped_anything = True
            if chat_id in muted_users:
                del muted_users[chat_id]
                stopped_anything = True
            if chat_id in active_reply_modes:
                del active_reply_modes[chat_id]
                stopped_anything = True
            if voice_call is not None and (chat_id in active_media or chat_id in active_recordings):
                try:
                    await voice_call.leave_call(chat_id)
                except Exception:
                    pass
                await _cleanup_vc_media(chat_id)
                active_recordings.pop(chat_id, None)
                stopped_anything = True
            if stopped_anything:
                await respond(event, "🛑 All active tasks stopped.")
            else:
                await respond(event, "❌ No active tasks to stop.")

        @client.on(events.NewMessage(pattern="√mute"))
        async def mute_handler(event):
            if not is_authorized(event):
                return
            global muted_users
            chat_id = event.chat_id
            args = event.message.message.split()
            user_id = None
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                user_id = reply_msg.sender_id
            elif len(args) > 1:
                username = args[1].replace("@", "")
                try:
                    target_user = await client.get_entity(username)
                    user_id = target_user.id
                except Exception as e:
                    await respond(event, f"❌ Could not find user: {e}")
                    return
            elif event.is_private:
                user_id = (await event.get_input_chat()).user_id
            else:
                await respond(event, "❌ Reply to a message or use: √mute @username")
                return
            if chat_id not in muted_users:
                muted_users[chat_id] = set()
            if user_id not in muted_users[chat_id]:
                muted_users[chat_id].add(user_id)
                await respond(event, "🤫 Muted — purging old messages...")
                deleted_count = 0
                try:
                    batch = []
                    async for msg in client.iter_messages(chat_id, from_user=user_id, limit=None):
                        batch.append(msg.id)
                        if len(batch) >= 100:
                            try:
                                await client.delete_messages(chat_id, batch)
                                deleted_count += len(batch)
                            except Exception:
                                pass
                            batch = []
                            await asyncio.sleep(0.5)
                    if batch:
                        try:
                            await client.delete_messages(chat_id, batch)
                            deleted_count += len(batch)
                        except Exception:
                            pass
                except Exception as e:
                    print(f"⚠️ Old message purge error: {e}")
                try:
                    await client.send_message(chat_id, f"🤫 Muted + deleted {deleted_count} old messages.")
                except Exception:
                    pass
            else:
                await respond(event, "⚠️ Already muted here.")

        @client.on(events.NewMessage(pattern="√sp"))
        async def sp_handler(event):
            if not is_authorized(event):
                return
            chat_id = event.chat_id
            if active_sp_loops.get(chat_id, False):
                await respond(event, "⚠️ SP mode is already active. Use √stop to cancel.")
                return
            if not (event.is_group or event.is_channel):
                await respond(event, "❌ √sp only works in groups or channels.")
                return
            active_sp_loops[chat_id] = True
            await respond(event, "🗑️ SP mode activated — deleting all incoming messages...")

        @client.on(events.NewMessage(pattern=r"√reply"))
        async def reply_mode_handler(event):
            if not is_authorized(event):
                return
            text = event.message.message.replace("√reply", "", 1).strip()
            if not event.is_reply:
                await respond(event, "❌ Reply to someone's message first, then use: √reply <text>")
                return
            if not text:
                await respond(event, "❌ Provide the reply text: √reply <text>")
                return
            reply_msg = await event.get_reply_message()
            target_id = reply_msg.sender_id
            chat_id = event.chat_id
            if chat_id not in active_reply_modes:
                active_reply_modes[chat_id] = {}
            active_reply_modes[chat_id][target_id] = text
            await respond(event, f"💬 Auto-reply active — replying to that user with:\n{text}")

        @client.on(events.NewMessage(pattern="√admin"))
        async def admin_handler(event):
            if not is_authorized(event):
                return
            args = event.message.message.split()
            target_user = None
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                try:
                    target_user = await client.get_entity(reply_msg.sender_id)
                except Exception as e:
                    await respond(event, f"❌ Could not get user: {e}")
                    return
            elif len(args) > 1:
                username = args[1].replace("@", "")
                try:
                    target_user = await client.get_entity(username)
                except Exception as e:
                    await respond(event, f"❌ Could not find user: {e}")
                    return
            else:
                await respond(event, "❌ Reply to a message or provide @username after √admin")
                return
            name = getattr(target_user, 'first_name', None) or getattr(target_user, 'username', str(target_user.id))
            try:
                chat = await event.get_chat()
                is_supergroup_or_channel = getattr(chat, 'megagroup', False) or getattr(chat, 'broadcast', False)
                if is_supergroup_or_channel:
                    from telethon.tl.types import ChatAdminRights
                    await client(
                        telethon.functions.channels.EditAdminRequest(
                            channel=event.chat_id,
                            user_id=target_user,
                            admin_rights=ChatAdminRights(
                                change_info=True, post_messages=True,
                                edit_messages=True, delete_messages=True,
                                ban_users=True, invite_users=True,
                                pin_messages=True, add_admins=True,
                                anonymous=False, manage_call=True, other=True,
                            ),
                            rank="Admin"
                        )
                    )
                else:
                    await client(
                        telethon.functions.messages.EditChatAdminRequest(
                            chat_id=event.chat_id,
                            user_id=target_user,
                            is_admin=True
                        )
                    )
                await respond(event, f"✅ {name} is now admin with full rights.")
            except Exception as e:
                err = str(e)
                print(f"⚠️ Admin grant error: {e}")
                if "recently" in err.lower() or "TIME_WAIT" in err:
                    await respond(event, "❌ Account is too new/recently logged in to manage admins.")
                elif "CHAT_ADMIN_REQUIRED" in err or "not an admin" in err.lower():
                    await respond(event, "❌ You need admin + 'Add Admins' permission.")
                else:
                    await respond(event, f"❌ Error: {err}")

        @client.on(events.NewMessage(pattern="√take"))
        async def take_handler(event):
            if not is_authorized(event):
                return
            args = event.message.message.split()
            target_user = None
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                try:
                    target_user = await client.get_entity(reply_msg.sender_id)
                except Exception as e:
                    await respond(event, f"❌ Could not get user: {e}")
                    return
            elif len(args) > 1:
                username = args[1].replace("@", "")
                try:
                    target_user = await client.get_entity(username)
                except Exception as e:
                    await respond(event, f"❌ Could not find user: {e}")
                    return
            else:
                await respond(event, "❌ Reply to a message or provide @username after √take")
                return
            name = getattr(target_user, 'first_name', None) or getattr(target_user, 'username', str(target_user.id))
            try:
                chat = await event.get_chat()
                is_supergroup_or_channel = getattr(chat, 'megagroup', False) or getattr(chat, 'broadcast', False)
                if is_supergroup_or_channel:
                    from telethon.tl.types import ChatAdminRights
                    await client(
                        telethon.functions.channels.EditAdminRequest(
                            channel=event.chat_id,
                            user_id=target_user,
                            admin_rights=ChatAdminRights(),
                            rank=""
                        )
                    )
                else:
                    await client(
                        telethon.functions.messages.EditChatAdminRequest(
                            chat_id=event.chat_id,
                            user_id=target_user,
                            is_admin=False
                        )
                    )
                await respond(event, f"✅ Removed all admin rights from {name}.")
            except Exception as e:
                err = str(e)
                print(f"⚠️ Take admin error: {e}")
                if "recently" in err.lower() or "TIME_WAIT" in err:
                    await respond(event, "❌ Account is too new/recently logged in to manage admins.")
                elif "CHAT_ADMIN_REQUIRED" in err or "not an admin" in err.lower():
                    await respond(event, "❌ You need admin + 'Add Admins' permission.")
                else:
                    await respond(event, f"❌ Error: {err}")

        @client.on(events.NewMessage(pattern="√kick"))
        async def kick_handler(event):
            if not is_authorized(event):
                return
            args = event.message.message.split()
            target_user = None
            if event.is_reply:
                reply_msg = await event.get_reply_message()
                try:
                    target_user = await client.get_entity(reply_msg.sender_id)
                except Exception as e:
                    await respond(event, f"❌ Could not get user: {e}")
                    return
            elif len(args) > 1:
                username = args[1].replace("@", "")
                try:
                    target_user = await client.get_entity(username)
                except Exception as e:
                    await respond(event, f"❌ Could not find user: {e}")
                    return
            else:
                await respond(event, "❌ Reply to a message or provide @username after √kick")
                return
            try:
                name = getattr(target_user, 'first_name', None) or getattr(target_user, 'username', str(target_user.id))
                await client.kick_participant(event.chat_id, target_user)
                await respond(event, f"👢 {name} has been kicked.")
            except Exception as e:
                print(f"⚠️ Kick error: {e}")
                await respond(event, f"❌ Error: {e}")

        @client.on(events.NewMessage(pattern="√add", outgoing=True))
        async def add_bots_handler(event):
            bots_to_add = [
                "FORALLNC12BOT",
                "FORALLNC13BOT",
                "FORALLNC14BOT",
            ]
            await event.edit(f"🤖 Adding {len(bots_to_add)} bots and promoting to admin...")
            added_count = 0
            promoted_count = 0
            for bot_username in bots_to_add:
                try:
                    try:
                        bot_entity = await client.get_entity(bot_username)
                    except Exception as entity_error:
                        print(f"⚠️ Could not resolve {bot_username}: {entity_error}")
                        continue
                    try:
                        await client(
                            telethon.functions.channels.InviteToChannelRequest(
                                channel=event.chat_id,
                                users=[bot_entity]
                            )
                        )
                        added_count += 1
                    except Exception as invite_error:
                        if "USER_ALREADY_PARTICIPANT" in str(invite_error):
                            added_count += 1
                        else:
                            print(f"⚠️ Failed to invite {bot_username}: {invite_error}")
                    try:
                        from telethon.tl.types import ChatAdminRights
                        await client(
                            telethon.functions.channels.EditAdminRequest(
                                channel=event.chat_id,
                                user_id=bot_entity,
                                admin_rights=ChatAdminRights(
                                    change_info=True, delete_messages=True,
                                    ban_users=True, invite_users=True,
                                    pin_messages=True, add_admins=False,
                                    anonymous=False, manage_call=True, other=True
                                ),
                                rank="Bot Admin"
                            )
                        )
                        promoted_count += 1
                    except Exception as promote_error:
                        print(f"⚠️ Failed to promote {bot_username}: {promote_error}")
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"⚠️ General error processing {bot_username}: {e}")
            await event.edit(f"✅ Finished! Added/Checked: {added_count}, Promoted: {promoted_count}")

        @client.on(events.NewMessage(pattern=r"√smiley\b"))
        async def smiley_handler(event):
            if not is_authorized(event):
                return
            if not event.is_reply:
                await respond(event, "❌ Please reply to a message with √smiley")
                return
            chat_id = event.chat_id
            if chat_id in active_smiley_loops and active_smiley_loops[chat_id]:
                await respond(event, "⚠️ A Smiley loop is already active here.")
                return
            reply_msg = await event.get_reply_message()
            chat = await event.get_input_chat()
            try:
                await event.delete()
            except Exception:
                pass
            print(f"🔥 Smiley mode activated in chat {chat_id}")
            active_smiley_loops[chat_id] = True
            msg_count = 0
            while active_smiley_loops.get(chat_id, False):
                for msg_text in SMILEY_MESSAGES:
                    if not active_smiley_loops.get(chat_id, False):
                        break
                    try:
                        await client.send_message(chat, msg_text, reply_to=reply_msg.id)
                        msg_count += 1
                        if msg_count % 3 == 0:
                            for _ in range(10):
                                if not active_smiley_loops.get(chat_id, False):
                                    break
                                await asyncio.sleep(1)
                        else:
                            await asyncio.sleep(1)
                    except telethon.errors.rpcerrorlist.FloodWaitError as e:
                        print(f"🛑 FloodWait: waiting {e.seconds} seconds...")
                        await asyncio.sleep(e.seconds)
                    except Exception as e:
                        print(f"⚠️ Smiley error: {e}")
                        await asyncio.sleep(5)
            print(f"🏁 Smiley loop ended in chat {chat_id}")

        print("🤖 Bot running. Owner commands: √sub, √antisub | All commands: √smiley, √stop, -vn, √song, √callfight, √play, √vplay, √skip, √recording, √record, √react, √forward, √mute, √clonejutsu, √back, √add, √sp, √admin, √take, √kick, √reply")
        await client.run_until_disconnected()


async def run_with_reconnect():
    retry_delay = 5
    while True:
        try:
            print(f"🔌 Connecting...")
            await main()
        except (ConnectionError, OSError) as e:
            print(f"🔴 Connection lost: {e} — reconnecting in {retry_delay}s...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
        except telethon.errors.AuthKeyDuplicatedError:
            print("❌ Session conflict (logged in elsewhere). Stopping.")
            break
        except KeyboardInterrupt:
            print("👋 Stopped by user.")
            break
        except Exception as e:
            print(f"⚠️ Unexpected crash: {e} — reconnecting in {retry_delay}s...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)
        else:
            retry_delay = 5


if __name__ == "__main__":
    asyncio.run(run_with_reconnect())
