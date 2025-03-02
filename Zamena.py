# meta developer: @Berki_Modul, @ManulMods

# License for Module Use

# This module was developed by @Skater2033 and is provided to you under the following license. Please read the terms of use carefully:

# 1. Usage:
#    - You may use this module in your projects, modify, and adapt it at your discretion.

# 2. Distribution:
#    - You are allowed to distribute modified or unmodified versions of the module, provided that you mention @Skater2033 as the author of the original module.

# 3. Prohibition of Commercial Use:
#    - This module is not intended for commercial use without the prior consent of the author.

# 4. Disclaimer:
#    - The author of the module is not responsible for any damages, losses, or consequences arising from the use of this module.

# 5. Feedback:
#    - If you have suggestions or questions, you can contact @Skater2033.

# By using this module, you agree to the terms of this license.

from .. import loader, utils

from contextlib import suppress
from telethon.tl.types import Message, MessageMediaPhoto


@loader.tds
class LeetConverter(loader.Module):
    strings = {
        "name": "LeetConverter"
    }
    
    translate_map = {
        ord("е"): "3",
        ord("а"): "4",
        ord("о"): "0",
        ord("s"): "5",
        ord("t"): "7",
        ord("b"): "8",
        ord("g"): "9"
    }
    
    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        self.enabled = self.db.get("Leet_Converter", "enabled", False)
    
    async def leerercmd(self, message: Message):
        """Включить или отключить режим еблана"""
        
        self.enabled = not self.enabled
        self.db.set("leet", "enabled", self.enabled)
        
        if self.enabled:
            return await utils.answer(
                message=message,
                response="<b> 🟢 Leet-замена активирована! </b>"
            )
        
        else:
            return await utils.answer(
                message=message,
                response="🔴  <b>Leet-замена деактивирована!</b>"
            )
    
    async def leetcmd(self, message: Message):
        """Leet-замена по <reply>"""
        
        reply = await message.get_reply_message()
        
        translated_text = reply.text.translate(self.translate_map)

        await utils.answer(
            message=message,
            response=f" <b>Leet-заменённое сообщение</b>:\n\n{translated_text}"
        )

    
    async def watcher(self, message: Message):
        if self.enabled:
            if message.out:
                translated_text = message.text.translate(self.translate_map)
                
                if message.text != translated_text:
                    await self._client.edit_message(message.peer_id, message.id, translated_text)
