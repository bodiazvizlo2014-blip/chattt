import asyncio
import os
from pywebio import start_server
from pywebio.input import input, input_group
from pywebio.output import put_markdown, output, put_scrollable
from pywebio.session import run_async

# Список для зберігання всіх повідомлень та активних користувачів
chat_msgs = []  # (ім'я, текст)
online_users = set()


async def main():
    global chat_msgs

    put_markdown("## 💬 Мій онлайн чат")

    # Зона повідомлень
    msg_box = output()
    put_scrollable(msg_box, height=300, keep_bottom=True)

    # Імʼя користувача
    nickname = await input(
        "Вхід у чат",
        placeholder="Ваше ім'я",
        required=True
    )

    online_users.add(nickname)
    chat_msgs.append(("📢", f"'{nickname}' приєднався до чату"))

    # Оновлення повідомлень
    async def refresh_msg():
        last_idx = 0
        while True:
            await asyncio.sleep(0.5)
            for m in chat_msgs[last_idx:]:
                msg_box.append(
                    put_markdown(f"**{m[0]}**: {m[1]}")
                )
            last_idx = len(chat_msgs)

    run_async(refresh_msg())

    # Відправка повідомлень
    while True:
        data = await input_group(
            "Написати повідомлення",
            [
                input(
                    name="msg",
                    placeholder="Текст...",
                    required=True
                )
            ]
        )
        chat_msgs.append((nickname, data["msg"]))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    start_server(
        main,
        port=port,
        host="0.0.0.0",
        debug=False
    )
