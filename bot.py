from pyrogram import Client, filters
from pymongo import MongoClient
import random, string

API_ID = 15191874
API_HASH = "3037d39233c6fad9b80d83bb8a339a07"
BOT_TOKEN = "6941908449:AAG4rJU2UzaNIR1G6TvMZH2Kk9M8xdsop8k"
BOT_USERNAME = "Joe1Obot"   # without @

MONGO_URI = "mongodb://hp108044:zWy9AuflXmsrAfSY@147.93.103.130:27017/?authSource=admin"

# MongoDB
mongo = MongoClient(MONGO_URI)
db = mongo["link_store_bot"]
links_col = db["links"]

app = Client(
    "link_store_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def generate_slug():
    length = random.randint(25, 30)
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@app.on_message(filters.command("start"))
async def start(client, message):
    if len(message.command) > 1:
        slug = message.command[1]
        data = links_col.find_one({"slug": slug})

        if data:
            await message.reply_text(
                "ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ!\n"
                "ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ᴘʀᴏᴄᴇᴇᴅ",
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            "🔗 Open Link",
                            url=data["link"]
                        )
                    ]]
                ))
            
        else:
            await message.reply_text("❌ Invalid or expired link.")
    else:
        await message.reply_text(
            "👋 Welcome!\n\n"
            "Send me a link and reply to it with /genlink"
        )


@app.on_message(filters.command("genlink"))
async def genlink(client, message):
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a link message.")
        return

    link = message.reply_to_message.text
    slug = generate_slug()

    links_col.insert_one({
        "slug": slug,
        "link": link
    })

    short_link = f"https://t.me/{BOT_USERNAME}?start={slug}"

    await message.reply_text(
        f"✅ Your link generated:\n\n{short_link}",
        reply_to_message_id=message.reply_to_message.id
    )


app.run()