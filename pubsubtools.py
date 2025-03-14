# perhaps put the EVENT LOOP of the muc_message portion of this bot in another ...  event loop
## use the pubsub commands and other commands on the exterior and statically as import
### we needed to sort out these event loops, and asynchronous things!!!

from getpass import getpass
from pubsub_commands import PubSubCommands as ps_commands
import asyncio
import slixmpp
import logging
import os
import random

class PubSubTools(slixmpp.ClientXMPP):

# THIS IS BOOTSTRAPPING ASYNCRONOUS MUC CHAT BOT:
	def __init__(self, jid, password, room, nick):
		slixmpp.ClientXMPP.__init__(self, jid, password)

		self.jid = jid
		self.password = password
		self.room = room
		self.nick = nick
		# FOR TESTING SAKE:
		self.pubsub_server = "pubsub.xmpp.packets.cc"

		self.register_plugin('xep_0030')  # Service Discovery
		self.register_plugin('xep_0045')  # Multi-User Chat
		self.register_plugin('xep_0059')  # Result Set Management
		self.register_plugin('xep_0060')  # PubSub
		self.register_plugin('xep_0199')  # XMPP Ping

		self.add_event_handler("session_start", self.start)
		self.add_event_handler("groupchat_message", self.muc_message)

	async def start(self, event):
		await self.get_roster()
		self.send_presence()
		self.plugin['xep_0045'].join_muc(self.room, self.nick)

	def muc_message(self, msg):
	# PARSE THE INCOMING MESSAGE IN THE EVENT IT TRIGGERS A COMMAND:

		# ABOUT:
		if msg['body'] == "!xmpp about":
			mesgs = [
				"xmpp:xmpptools@packets.cc",
				"xmpp:pubsubtools@packets.cc",
				"PubSubTools - A SliXMPP Bot Project - by chunk",
				"https://github.com/the8woodcutter/pubsubtools"
			]
			mesg = "\r\n".join(mesgs)
			msg.reply(mesg).send()

		# HELP:
		if msg['body'] == "!xmpp help":
			mesgs = [
				"`!xmpp nodes` to get nodes from pubsub server",
				"`!xmpp get <node_name>` to get node items from node",
			]
			mesg = "\r\n".join(mesgs)
			msg.reply(mesg).send()

		# ### COMMANDS:
		body = msg['body']
		parts = body.split(' ')

	# SERVICE DISCOVERY:
	## NOT PUBSUB!
		# GET LOCAL INFO:
		if body == "!xmpp getinfo":
			info = self['xep_0030'].get_info(node=self.nick, local=True)
			info_list = info.split('\n')
			info_str = "\r\n".join(info_list)
			msg.reply(info_str).send()

		# GET LOCAL NODE ITEMS:
		if body.startswith('!xmpp items '):
			if len(parts) > 2:
				node = parts[2]
				node = str(node)
				items = self['xep_0030'].get_items(jid=self.jid, node=node, local=True)
				items_string = "\r\n".join(items)
				msg.reply(items_string).send()

		# if body == "!xmpp nodes":
		# 	test = ps_commands.nodes(self)

		# if len(parts) > 2:
		# 	if parts[0] == "!xmpp":
		# 		if len(parts) == 3: # 1 args: node
		# 			node = parts[2]
		# 			node = str(node)
					
		# 			if parts[1] == "get":
		# 				# variable = method():
		# 				get = ps_commands.get(self, node)
				# 	elif parts[1] == "create":
				# 		# variable = method():
				# 		create = ps_commands.create(self, node)
				# 	elif parts[1] == "delete":
				# 		# variable = method():
				# 		delete = ps_commands.delete(self, node)
				# 	elif parts[1] == "purge":
				# 		# variable = method():
				# 		purge = ps_commands.purge(self, node)
				# 	elif parts[1] == "subscribe":
				# 		# variable = method():
				# 		subscribe = ps_commands.subscribe(self, node)
				# 	elif parts[1] == "unsubscribe":
				# 		# variable = method():
				# 		unsubscribe = ps_commands.unsubscribe(self, node)
				# 	else:
				# 		pass # write to muc (maybe) error of ____

				# # publish, retract:
				# elif len(parts) == 4: # 2 args: node, data
				# 	pass


if __name__ == '__main__':
	jid = input("Bot's JID: ")
	jid = str(jid)
	password = getpass("Bot's Password: ")
	password = str(password)
	if len(password) < 1:
		print('Password is empty!')
	room = input("MUC JID to Join: ")
	room = str(room)
	nick = input("Bot's Nickname: ")
	nick = str(nick)
	# server = input("PubSub Server JID: ")
	# server = str(server)


	xmpp = PubSubTools("b0t@packets.cc", "000000", "memos@muc.xmpp.packets.cc", "b0t")
	xmpp.register_plugin('xep_0030')  # Service Discovery
	xmpp.register_plugin('xep_0045')  # Multi-User Chat
	xmpp.register_plugin('xep_0059')  # Result Set Management
	xmpp.register_plugin('xep_0060')  # PubSub
	xmpp.register_plugin('xep_0199')  # XMPP Ping
	xmpp.connect()
	xmpp.process()

# xmpp = ClientXMPP(f'{jid}/{random.randint(10000,999999)}', str(password))
# # ... Register plugins and event handlers ...
# self.register_plugin('xep_0030')  # Service Discovery
# self.register_plugin('xep_0045')  # Multi-User Chat
# self.register_plugin('xep_0059')  # Result Set Management
# self.register_plugin('xep_0060')  # PubSub
# self.register_plugin('xep_0199')  # XMPP Ping

# self.add_event_handler("session_start", self.start)
# self.add_event_handler("groupchat_message", self.muc_message)
# xmpp.connect()
# asyncio.get_event_loop().run_forever()