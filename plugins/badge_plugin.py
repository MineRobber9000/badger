import plugin, badge, random, json, traceback
from bot import IRCLine
from collections import Counter
BOT = None

class BadgePopData(plugin.Data):
	def serialize(self):
		return json.dumps(self.value.to_json())
	def deserialize(self,s):
		self.value = badge.BadgePopulation.from_json(s)

population = BadgePopData(badge.BadgePopulation())
population.load("badges.json")

timeouts = plugin.DictData("timeouts.json")

badge_weights = {'Berrybadge': 0.65, 'Rockbadge': 0.1, 'Waterbadge': 0.05, 'Firebadge': 0.15, 'Tildebadge': 0.001, 'Shadybadge': 0.02, 'Musicbadge': 0.019, 'Sportsbadge': 0.01}

def privmsg(target,message):
	return IRCLine("PRIVMSG",target,":"+message).line

def respond(event,message):
	if BOT is None: return
	BOT.socket.send(privmsg(event.target if event.target.startswith("#") else event.hostmask.nick,(event.hostmask.nick+": " if event.target.startswith("#") else "")+message))

def on_privmsg(event):
	if BOT is None: return
	account = event.tags.get("account",None)
	if account is None: return
	if account in ("BitBot",): return # ignore BitBot
	if not event.target.startswith("#"): return
	if timeouts.get(event.target,0)==0:
		badge_to_give = random.choices(list(badge_weights.keys()),list(badge_weights.values()))[0]
		if account not in population.value.badges:
			BOT.socket.send(privmsg(event.hostmask.nick,f"Hey, you've got a badge! Badges are a nice way to show how active you are in channels like {event.target}. Type 'help' to see what you can do with these badges."))
		population.value.give_badge(account,badge_to_give)
		population.save("badges.json")
		timeouts[event.target]=random.randint(20,50)
	else:
		timeouts[event.target]-=1
	if event.message=="!botlist":
		respond(event,"Hi! I'm the badger! I give out badges randomly. "+("Commands you can use include 'listbadges' and 'transmute'." if account is not None else "To get started, log in to a services account! (/msg NickServ help)"))

def on_cmd_help(event):
	if BOT is None: return
	account = event.tags.get("account",None)
	if len(event.parts)==0:
		respond(event,"Hi! I'm the badger! I give out badges randomly. "+("Commands you can use include 'listbadges' and 'transmute'." if account is not None else "To get started, log in to a services account! (/msg NickServ help)"))
		return None
	if account is None: return
	if event.parts[0]=="listbadges":
		respond(event,"Lists the badges in your possession. Usage: listbadges")
	elif event.parts[0]=="transmute":
		respond(event,"Transmutes 3 or more badges into one, possibly rarer, badge. Usage: transmute <badge one> <badge two> <badge three> [badge four...]")

def on_cmd_listbadges(event):
	if BOT is None: return
	account = event.tags.get("account",None)
	if account is None: return
	counts = Counter([x.name for x in population.value.badges.get(account,"")])
	ret = []
	for item in counts.items():
		ret.append("{} (x{!s})".format(*item))
	if len(counts.items())==0:
		respond(event,"You don't have any badges yet! Just stay active in the channel and you'll get one eventually.")
	else:
		respond(event,"You have: "+", ".join(ret))

def on_cmd_transmute(event):
	if BOT is None: return
	account = event.tags.get("account",None)
	if account is None: return
	if len(event.parts)<3:
		respond(event,"You must insert at least 3 badges for use in transmutation.")
		return
	try:
		badge_result = population.value.transmute(account,*event.parts)
	except:
		traceback.print_exc()
		respond(event,"You must have at least one (1) of each badge you wish to use in the transmutation.")
		return
	respond(event,"You put in the {!s} badges above, and out pops a {}!".format(len(event.parts),badge_result))
	population.value.give_badge(account,badge_result,False)
	population.save("badges.json")

def admin_givebadge(event):
	print(event.name,event.data)
	try:
		account, badge = event.parts[:2]
		normal=True
		if len(event.parts)==3 and event.parts[2].lower() in ("n","no","f","false"): normal=False
		population.value.give_badge(account,badge,normal)
		population.save("badges.json")
	except: pass

def register(bot):
	global BOT
	BOT=bot
	bot.event_manager.on("privmsg",on_privmsg)
	bot.event_manager.on("command_help",on_cmd_help)
	bot.event_manager.on("command_listbadges",on_cmd_listbadges)
	bot.event_manager.on("command_transmute",on_cmd_transmute)
	bot.event_manager.on("admin_givebadge",admin_givebadge)
