from telethon import TelegramClient, events
import asyncio
import g4f
import json
import requests
api_id = 22703059
api_hash = 'e61d8d8fb6f1aa3c47cefdfdcc59592d'
session_name = 'session1'
client = TelegramClient(session_name, api_id, api_hash)


async def get_message_ai(q:str):
  message = [
                    {'role': 'system', 'content': 'أنت الان في محادثة في التليجرام وقام شخص ما بإرسال الرسالة التالية , أريدك أن تقوم بالرد عليها بإعتبار أنك منصة إسمها "studyco" يجب أن تكون الرسالة قصيرة وتفي بالغرض قدر الإمكان'},
                    {"role": "user", "content": q}
                  ]
  data = {
    "prompt": f"أنت الان في محادثة في التليجرام وقام شخص ما بإرسال الرسالة التالية , أريدك أن تقوم بالرد عليها بإعتبار أنك منصة إسمها 'studyco' يجب أن تكون الرسالة قصيرة وتفي بالغرض قدر الإمكان {q}",
    "api_owner": 'AlharaqApi',
    "model":"mixtral-8x7b",
    "lang": "ar",
    "user_id": "dcb2d2ae-4039-4172-a347-7d324337eca8",
    "conversation_id": "c137a562-dfa9-4d8c-a4d0-acb77a5b3e86",
    "is_web_search": False,
    "is_emojis": False
}

  url = "https://randai09078-randdaj.hf.space/api/chat/text"

  response = requests.post(url, json=data)
    
    # Check if request was successful (status code 200)
  if response.status_code == 200:
      # Get JSON response data
    try:
        # Try to parse JSON response data
        response_data = response.json()
        if 'messageAi' in response_data and 'textTranInfo' in response_data['messageAi']:
            for info in response_data['messageAi']['textTranInfo']:
                if info.get('code_id') == 'ar':
                    return info['text']
    except json.decoder.JSONDecodeError:
        # If parsing fails, print response text
        response_text = response.text.strip()
        response_objects = response_text.split('\n')
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

        response = await get_message_ai(event.message)
        if response:
            sender_id = event.sender_id
            await client.send_message(sender_id, event.message)
            await client.send_message(sender_id, "السلام عليكم.")
            await client.send_message(sender_id, response)


async def main():
    await client.start()
    print("Client started.")
    await client.run_until_disconnected()
asyncio.run(main())