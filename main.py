import asyncio
from pyrogram import Client, filters
import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]

target_chats = [int(x.strip()) for x in os.environ["TARGET_CHATS"].split(",")]
INTERVAL = 300  # 5 minutes

app = Client("userbot", api_id=api_id, api_hash=api_hash)
queue = []


@app.on_message(filters.chat("me"))
async def save_message(client, message):
    queue.append(message)
    print(f"[+] Queued message {message.id}")


async def post_loop():
    print("[READY] Waiting for Saved Messages...")

    while True:
        if queue:
            msg = queue.pop(0)
            print(f"[>] Sending queued message {msg.id}")

            for chat in target_chats:
                try:
                    await msg.copy(chat)
                    print(f"[✔] Sent → {chat}")
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"[⚠] Failed → {chat}: {e}")
                    await asyncio.sleep(1)

        await asyncio.sleep(INTERVAL)


async def main():
    await app.start()
    print("[LOGIN OK]")
    await post_loop()


app.run(main())
