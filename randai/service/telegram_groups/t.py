# !pip install telebot telethon
from telethon import TelegramClient, events
from telethon.tl.types import InputPeerChat
from telethon.tl.functions.channels import JoinChannelRequest  
import asyncio
import nest_asyncio
import json
import requests
import time
api_id = 22703059
api_hash = "e61d8d8fb6f1aa3c47cefdfdcc59592d"
session_name = "session"
client = TelegramClient(session_name, api_id, api_hash)
keyword_list = [
    "أريد بحث", 
    "أبغى حد يسوي بحث",
    "حد يساعدني في حل واجب"
  
    ]
company_name = "StudyCo"
is_use_ai = False
default_replay = ["مرحبا يسعدني مساعدتك!"]
url = "https://randai09078-randdaj.hf.space/api/chat/text"
sleep_duration = 60
groups_list = ["https://t.me/un_taif", "https://t.me/UT1_CS"]

is_join_groups = False


async def is_already_joined(client, link):
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        entity = dialog.entity
        if entity.username == link or f't.me/{link}' in entity.username:
            return True
    return False



async def join_groups_from_list(group_links):
    if not client.is_connected:
        print("Client is not connected. Unable to join groups.")
        return

    for link in group_links:
        # if await is_already_joined(link):
        #     continue
        try:
            await client(JoinChannelRequest(link))
            print(f"Joined group: {link}")
            await asyncio.sleep(sleep_duration)
        except Exception as e:
            print(f"Error joining group {link}: {str(e)}")
        
async def get_message_ai(q: str):
    system_prompt = f"""
  أنت الآن في محادثة في تطبيق تليجرام ، أنت تمثل منصة "{company_name}" التي تقدم خدمات لمساعدة الطلاب ، 
تنبية: 
أجعل ردودك قصيرة جداً تتناسب مع محادثة شخصية ، 
لا تقوم بتقديم إي سؤال إلى المستخدم، 
ينبغي أن تتفاعل كمنصة "{company_name}"
قم بالقاء التحية والتعريف بالمنصة
 الآن قم  بالتفاعل مع رسالة الطالب هذه التي يطلب فيها :
{q}
"""
    data = {
        "prompt": system_prompt,
        "api_owner": "AlharaqApi",
        "model": "mixtral-8x7b",#mixtral-8x7b gemini-pro
        "lang": "ar",
        "user_id": "dcb2d2ae-4039-4172-a347-7d324337eca8",
        "conversation_id": "c137a562-dfa9-4d8c-a4d0-acb77a5b3e86",
        "is_web_search": False,
        "is_emojis": False,
        "is_group_telegram": True,
    }

    

    response = requests.post(url, json=data)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Get JSON response data
        try:
            # Try to parse JSON response data
            response_data = response.json()
            if (
                "messageAi" in response_data
                and "textTranInfo" in response_data["messageAi"]
            ):
                for info in response_data["messageAi"]["textTranInfo"]:
                    if info.get("code_id") == "ar":
                        return info["text"]
        except json.decoder.JSONDecodeError:
            # If parsing fails, print response text
            response_text = response.text.strip()
            response_objects = response_text.split("\n")
            for obj in response_objects:
                try:
                    # Try to parse each JSON object separately
                    response_data = json.loads(obj)
                    print(response_data)
                except json.decoder.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
            return None
    else:
        # Handle request error
        print(f"Error: {response.text}")
        return None


@client.on(events.NewMessage)
async def handle_new_group_message(event):
    print(f"New message from group: {event.message}")
    if event.sender_id == await client.get_me():
        return
    if event.is_group:
        print(event.message.text)
        if any(keyword in event.message.text for keyword in keyword_list):
            if is_use_ai:
                response = await get_message_ai(event.message.text)
                if response:
                    sender_id = event.sender_id
                    await client.send_message(sender_id, event.message)
                    await client.send_message(sender_id, "السلام عليكم.")
                    await client.send_message(sender_id, response)
            else:
                sender_id = event.sender_id
                await client.send_message(sender_id, event.message)
                await client.send_message(sender_id, "السلام عليكم.")
                await client.send_message(sender_id, default_replay[0])
        else:
          print("hhhhhh")



async def main():
    await client.start()
    print("Client started.")
    if is_join_groups:
         await join_groups_from_list(groups_list)
    await client.run_until_disconnected()


nest_asyncio.apply()
asyncio.run(main())
