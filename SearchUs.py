# meta developer: @ManulMods

from telethon.tl.types import Message, User
from .. import loader, utils

@loader.tds
class UserIDFinderMod(loader.Module):
    """Получение ID пользователя по юзернейму"""
    strings = {"name": "UserID Finder"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def ид(self, message: Message):
        """[@юзернейм или реплай] - Узнать ID пользователя"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        try:
            if args:
                username = args.lstrip('@')
                user = await self.client.get_entity(username)
            elif reply:
                user = await self.client.get_entity(reply.sender_id)
            else:
                return await utils.answer(message, "❌ Укажите @юзернейм или сделайте реплай!")

            if isinstance(user, User):
                # Формируем информацию о фамилии
                last_name = f"{user.last_name}" if user.last_name else "<emoji document_id=5215273032553078755>❎</emoji>"
                
                result = (
                    f"👤 Информация о пользователе:\n\n"
                    f"🆔 ID: <code>@{user.id}</code>\n"
                    f"📛 Имя: {user.first_name or '<emoji document_id=5215273032553078755>❎</emoji>'}\n"
                    f"📚 Фамилия: {last_name}\n"
                    f"🌐 Юзернейм: @{user.username or 'нет'}\n"
                    f"🤖 Бот: {'✅ Да' if user.bot else '❌ Нет'}"
                )
                await utils.answer(message, result)
            else:
                await utils.answer(message, "❌ Это не пользователь!")

        except ValueError:
            await utils.answer(message, "❌ Пользователь не найден!")
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {str(e)}")
