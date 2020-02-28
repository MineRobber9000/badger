from plugin import DictData
BOT = None

username_nick = DictData("association.json")

def on_privmsg(event):
	if BOT is None: return
	if event.tags.get("account") is None: return
	username_nick[event.tags["account"]]=event.hostmask.nick

def register(bot):
	global BOT
	BOT=bot
	bot.event_manager.on("privmsg",on_privmsg)
