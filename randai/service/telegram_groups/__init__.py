# !pip install telebot telethon
# from telethon import TelegramClient, events
from telethon.tl.types import InputPeerChat
from telethon.tl.functions.channels import JoinChannelRequest  
from ..BaseGenerator import BaseGenerator
from telethon.sync import TelegramClient ,  events
from telethon import errors
import asyncio
from pathlib import Path
import nest_asyncio
import json
import requests
import time
sleep_duration = 60
is_join_groups = False
groups_file_path = Path(__file__).resolve().parent / 'groups_list.json'
config_file_path = Path(__file__).resolve().parent / 'config.json'
keyword_file_path = Path(__file__).resolve().parent / 'keyword_list.json'
# client = TelegramClient("session_name", "api_id", "api_hash")

class TelegramInfo():
    def __init__(self):
        self.groups_file_path = groups_file_path
        self.config_file_path = config_file_path
        self.keyword_file_path = keyword_file_path
        

    def add_group_to_file(self, new_group):
        """Adds a new group to the JSON file."""
        try:
            with open(self.groups_file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                groups = data.get('groups', [])
                groups.append(new_group)
                data['groups'] = groups
                file.seek(0)
                json.dump(data, file, indent=4, ensure_ascii=False)
                file.truncate()
                print("New group added successfully.")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def get_all_groups(self):
        """Reads groups from a JSON file and returns a list of groups."""
        try:
            with open(self.groups_file_path, 'r') as file:
                data = json.load(file)
                groups = data.get('groups', [])
                return groups
        except FileNotFoundError:
            print("File not found.")
            return []


    def delete_group_from_file(self, group_to_delete):
        try:
            with open(self.group_file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                groups = data.get('groups', [])
                
                if group_to_delete in groups:
                    groups.remove(group_to_delete)
                    
                    file.seek(0)
                    json.dump(data, file, indent=4, ensure_ascii=False)
                    file.truncate()
                    
                    return True  
                else:
                    return False  
        except FileNotFoundError:
            raise FileNotFoundError("File not found.")
        except Exception as e:
            raise e

    def update_group_in_file(self, group_to_update, new_group):
        try:
            with open(self.group_file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                groups = data.get('groups', [])
                if group_to_update in groups:
                    index = groups.index(group_to_update)
                    groups[index] = new_group
                    file.seek(0)
                    json.dump(data, file, indent=4, ensure_ascii=False)
                    file.truncate()
                    return True  
                else:
                    return False 
        except FileNotFoundError:
            raise FileNotFoundError("File not found.")
        except Exception as e:
            raise e 
            
    def add_keyword_to_file(self, new_keyword):
        """Adds a new new_keyword to the JSON file."""
        try:
            with open(self.keyword_file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                keywords = data.get('keywords', [])
                keywords.append(new_keyword)
                data['keywords'] = keywords
                file.seek(0)
                json.dump(data, file, indent=4, ensure_ascii=False)
                file.truncate()
                print("New keywords added successfully.")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def get_all_keyword(self):
        """Reads keyword from a JSON file and returns a list of groups."""
        try:
            with open(self.keyword_file_path, 'r') as file:
                data = json.load(file)
                keywords = data.get('keywords', [])
                return keywords
        except FileNotFoundError:
            print("File not found.")
            return []
        
    def delete_keyword_from_file(self, keyword_to_delete):
        try:
            with open(self.keyword_file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                keywords = data.get('keywords', [])
                
                if keyword_to_delete in keywords:
                    keywords.remove(keyword_to_delete)
                    
                    file.seek(0)
                    json.dump(data, file, indent=4, ensure_ascii=False)
                    file.truncate()
                    
                    return True  
                else:
                    return False 
        except FileNotFoundError:
            raise FileNotFoundError("File not found.")
        except Exception as e:
            raise e

    def update_keyword_in_file(self, keyword_to_update, new_keyword):
        try:
            with open(self.keyword_file_path, 'r+', encoding='utf-8') as file:
                data = json.load(file)
                keywords = data.get('keywords', [])
                if keyword_to_update in keywords:
                    index = keywords.index(keyword_to_update)
                    keywords[index] = new_keyword
                    file.seek(0)
                    json.dump(data, file, indent=4, ensure_ascii=False)
                    file.truncate()
                    return True  
                else:
                    return False 
        except FileNotFoundError:
            raise FileNotFoundError("File not found.")
        except Exception as e:
            raise e


class TelegramJoinGroups():
    def __init__(self):
        self.groups_file_path = groups_file_path
        self.config_file_path = config_file_path
        self.keyword_file_path = keyword_file_path
        self.get_config()

    def get_config(self):
        try:
            with open(self.config_file_path, 'r') as file:
                data = json.load(file)
                config = data.get('myself', {})
                print("config ", config )
                return config
        except FileNotFoundError:
            print("File not found.")
            return {}

    async def is_already_joined(self, client, link):
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            entity = dialog.entity
            if entity.username == link or f't.me/{link}' in entity.username:
                return True
        return False



    async def join_groups_from_list(self):
        group_links = read_groups_from_file(groups_file_path)
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
                
                
class TelegramAuto(BaseGenerator):
    def __init__(self, req):
        super().__init__(req)
        self.groups_file_path = groups_file_path
        self.config_file_path = config_file_path
        self.keyword_file_path = keyword_file_path
        self.config = {}
        self.get_config()

    def get_config(self):
        try:
            with open(self.config_file_path, 'r') as file:
                data = json.load(file)
                self.config = data.get('myself', {})
                print("config ", self.config.get("api_id") )
        except FileNotFoundError:
            print("File not found.")
            return {}
        
    async def start_service(self):
        print("start_service(self) start_service(self)")
        try:
            phone = '+967714589027'
            client = TelegramClient(
                "session_name",
                22703059, 
                "e61d8d8fb6f1aa3c47cefdfdcc59592d")
            print(" TelegramClient TelegramClient TelegramClient")
            await  client.connect()
            print(" client.connect() client.connect() client.connect()")
            # await client.start()
            print(" client.start() client.start() client.start()")
            if not await client.is_user_authorized():
                    print("client.is_user_authorized( client.is_user_authorized( client.is_user_authorized(")
                    await client.send_code_request(phone)
                    # signing in the client
                    await client.sign_in(phone, input('Enter the code: '))
            print("Client started.")
            await client.run_until_disconnected()
            print("start")
        except errors.FloodWaitError as e:
            print(f"Flood wait error: {e}")
            # Handle flood wait error here
        except errors.TimeoutError as e:
            print(f"Timeout error: {e}")
            # Handle timeout error here
        except Exception as e:
            print(f"An error occurred: {e}")
            # Handle any other exceptions here
        
    async def get_message_ai(self,q: str):
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

        




    # @client.on(events.NewMessage)
    async def handle_new_group_message(event):
        print(f"New message from group: {event.message}")
        if event.sender_id == await client.get_me():
            return
        if event.is_group:
            print(event.message.text)
            if any(keyword in event.message.text for keyword in keyword_list):
                if is_use_ai:
                    response = await self.create_non_stream_response(event.message.text)
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

    async def join_groups_from_list():
        await client.start()
        print("Client started.")
        await join_groups_from_list(groups_list)


    def create_non_stream_response(self):
        retries = 0
        while retries < self.max_retries:
            try:
                params = self.prepare_params()
                response = self.g4f.ChatCompletion.create(**params)
                if response is not None:
                    if any(error_response in response for error_response in self.errors_response):
                        retries += 1
                    else:
                        break
                    
                else:
                    print("Received None response. Retrying...")
                    retries += 1

            except (RuntimeError, Exception) as e:
                print(f"Error during generate:")
                if retries < self.max_retries - 1:
                    print(f"Retrying... Attempt {retries + 2}/{self.max_retries}")
                    retries += 1
                else:
                    raise
        
        return response

# nest_asyncio.apply()
# asyncio.run(main())
