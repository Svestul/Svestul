from .. import loader, utils 


@loader.tds
class MuteMod(loader.Module):
    """Мут."""
    strings = {'name': 'Mute'}

    async def client_ready(self, client, db):
        self.db = db

    async def мcmd(self, message):
        """Включить/выключить мут. Используй: .м <@ или реплай>."""
        if message.chat:
            chat = await message.get_chat()
            if not chat.admin_rights and not chat.creator:
                return await message.edit("<b>Я не админ здесь.</b>")
            else:
                if chat.admin_rights.delete_messages == False:
                    return await message.edit("<b>У меня нет нужных прав.</b>")
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chatid = str(message.chat_id)
        mutes = self.db.get("Mute", "mutes", {})
        if not args and not reply: return await message.edit("<b>Нет аргументов или реплая.</b>")
        try:
            if args: 
                if args.isnumeric(): user = await message.client.get_entity(int(args))
                else: user = await message.client.get_entity(args)
            else: user = await message.client.get_entity(reply.sender_id)
        except ValueError: await message.edit("<b>Не удалось найти этого пользователя.</b>")
        if chatid not in mutes:
            mutes.setdefault(chatid, [])
        if str(user.id) not in mutes[chatid]:
            mutes[chatid].append(str(user.id))
            self.db.set("Mute", "mutes", mutes)
            await message.edit("спать")
        else:
            mutes[chatid].remove(str(user.id))
            if len(mutes[chatid]) == 0:
                mutes.pop(chatid)
            self.db.set("Mute", "mutes", mutes)
            await message.edit("просыпайся")

    async def кроваткаcmd(self, message):
        """Настройки мута. Используй: .кроватка <клеар/клеаралл (по желанию)>."""
        try:
            args = utils.get_args_raw(message)
            mutes = self.db.get("Mute", "mutes", {})
            chatid = str(message.chat_id)
            ls = mutes[chatid]
            users = ""
            if args == "клеар":
                mutes.pop(chatid)
                self.db.set("Mute", "mutes", mutes)
                return await message.edit("окес")
            if args == "клеаралл":
                self.db.set("Mute", "mutes", {})
                return await message.edit("окесс")
            for _ in ls:
                user = await message.client.get_entity(int(_))
                users += f"• <a href=\"tg://user?id={int(_)}\">{user.first_name}</a> <b>| [</b><code>{_}</code><b>]</b>\n"
            await message.edit(f"спят: {len(ls)}</b>\n\n{users}")
        except KeyError: return await message.edit("<b>пусто</b>")

    async def watcher(self, message):
        try:
            mutes = self.db.get("Mute", "mutes", {})
            chatid = str(message.chat_id)
            if chatid not in str(mutes): return
            ls = mutes[chatid]
            for _ in ls:
                if message.sender_id == int(_):
                    await message.client.delete_messages(message.chat_id, message.id)
        except: pass