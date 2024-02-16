import asyncio
from mailer import checkMail, mail_send
from translater import translator_foo
from determine_topic import determine_latter
from config import template_answers


async def main():
    final_answer = {}
    mail = await checkMail()
    if mail:
        mail[0] = await translator_foo(mail[0])
        determain_topic = await determine_latter(mail[0])
        final_answer[0] = template_answers[determain_topic]
        final_answer[1] = mail[1]
        mail_send(final_answer)


if __name__ == '__main__':
    while True:
        asyncio.run(main())
