import asyncio
from hugchat import hugchat
from hugchat.login import Login
from config import hug_login, hug_password, topics


async def determine_latter(latter_text):
    sign = Login(hug_login, hug_password)
    cookies = sign.login()

    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)

    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    request = f"Here are email topics: {topics}.Determine what topic and return only the topic number. This letter relates to - “{latter_text}”. "
    query_result = chatbot.query(request)
    try:
        topic_number = int([i for i in str(query_result) if i.isdigit()][0])
        return topic_number
    except:
        return 0
