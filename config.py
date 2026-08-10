import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID", "0"))
API_HASH = getenv("API_HASH")

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_ID = getenv("BOT_ID")

OWNER_USERNAME = getenv("OWNER_USERNAME", "Xbroze")
BOT_USERNAME = getenv("BOT_USERNAME", "@Clonemusichubot")
BOT_NAME = getenv("BOT_NAME", "CLONE MUSIC")
ASSUSERNAME = getenv("ASSUSERNAME", "")
BOT_LINK = getenv("BOT_LINK", "https://t.me/Clonemusichubot?start=_tgr_QHn2CMQ5Njc1")

MONGO_DB_URI = getenv("")

# ==========================================
# 🔄 MULTI-API FALLBACK SYSTEM SETTINGS
# ==========================================

# PRIMARY API (Pehli API jo gaana search karegi)
API_1_URL = getenv("API_1_URL", "https://music.xbitcode.com")
API_1_KEY = getenv("API_1_KEY", "xbit_283KQ7UaOqAMuVZeX6lePo-LGI4RRVYh")

# SECONDARY API (Agar pehli fail ho gayi, toh ye chalegi)
API_2_URL = getenv("API_2_URL", "https://api.onegrab.fun")
API_2_KEY = getenv("API_2_KEY", "b3f5d5_v1VHZtQsCDFtLOGO0OuD7iqHqVDCSOwa")

# ==========================================

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))

LOGGER_ID = int(getenv("LOGGER_ID", "0"))
CLONE_LOGGER = -1003541175831

OWNER_ID = int(getenv("OWNER_ID", "7524032836"))

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "t.me/zolvid",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", "")

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/narzoxbot")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/xbroze")
GITHUB = getenv("GITHUB", "https://t.me/xbroze")

AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "False")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "9000"))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
PLAYLIST_ID = -1001980154960

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv("START_IMG_URL", "https://graph.org/file/ec892470f3dd08277612b-59e7d2bd194c2c2ee3.jpg").split()
HELP_IMG_URL = getenv("HELP_IMG_URL", "https://graph.org/file/ec892470f3dd08277612b-59e7d2bd194c2c2ee3.jpg").split()
PING_IMG_URL = getenv("PING_IMG_URL", "https://graph.org/file/c733732aa48f1f437cff8-46db3ecea9f26bc132.jpg").split()

PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://i.ibb.co/gL3ykkyh/play-music.jpg").split()
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://i.ibb.co/pBqPtFYn/statistics.jpg").split()
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://i.ibb.co/gL3ykkyh/play-music.jpg").split()
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://i.ibb.co/gL3ykkyh/play-music.jpg").split()
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://i.ibb.co/0VKCS20y/stream.jpg").split()
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://i.ibb.co/S4sPf3q8/soundcloud.jpg").split()
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://i.ibb.co/xShkBVBK/youtube.jpg").split()
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://i.ibb.co/XZfMS8Db/spotify.jpg").split()
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://i.ibb.co/XZfMS8Db/spotify.jpg").split()
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://i.ibb.co/XZfMS8Db/spotify.jpg").split()

def time_to_seconds(time):
    return sum(int(x) * 60**i for i, x in enumerate(reversed(str(time).split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL and not re.match("(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - SUPPORT_CHANNEL url must start with https://")

if SUPPORT_CHAT and not re.match("(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - SUPPORT_CHAT url must start with https://")

CMBOT = [
    "💞", "🥂", "🔍", "🧪", "⚡️", "🔥", "🦋", "🎩", "🌈", "🍷",
    "🥃", "🥤", "🕊️", "💌", "🧨", "✨", "💥", "💯", "🌟", "⚡️",
    "❤️", "😍", "🥰", "😘", "😂", "🤣", "😱", "😡", "👏", "🙏",
    "🎉", "🎊", "🎶", "🎵", "🎧", "🎸", "🎹", "🥁", "🎺", "🎷",
    "🔥", "⚡️", "💫", "🌙", "☀️", "🌈", "❄️", "🌸", "🌺", "🌹",
    "🦋", "🕊️", "🐍", "🐯", "🦁", "🐺", "🐉", "🦅", "🦄", "🐎"
]

EFFECT_ID = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]
