# perhaps put the EVENT LOOP of the muc_message portion of this bot in another ...  event loop
## use the pubsub commands and other commands on the exterior and statically as import
### we needed to sort out these event loops, and asynchronous things!!!

from getpass import getpass
from pubsub_commands import PubSubCommands as ps_commands
import asyncio
import slixmpp
import logging
import os

class PubSubTools(slixmpp.ClientXMPP):

# THIS IS BOOTSTRAPPING ASYNCRONOUS MUC CHAT BOT:
	def __init__(self, jid, password, room, nick, server, node=None, data=''):
		super().__init__(self, jid, password)

		self.jid = jid
		self.password = password
		self.room = room
		self.nick = nick
		self.server = server
		self.node = node
		self.data = data

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

# THIS IS ALSO PART OF THE MUC CHAT BOT EVENT LOOP:
## THE ONLY THING WE SHOULD DO HERE IS ROUTE IN DATA TO THE COMMAND LIBRARY
### AND GET RETURN DATA FROM THE COMMAND LIBRARY.  That command library also has to login
### to the XMPP server and we can't have two logins in a loop!!
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
		# body = msg['body']
		# parts = body.split(' ')

		# # this is len(parts) == 2:
		# ## i think the only command of this such:
		# if body == "!xmpp nodes":
		# 	test = ps_commands.nodes(self)
		# 	if test == True:
		# 		pass
		# 	elif test == False:
		# 		pass
		# 	else:
		# 		pass

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
	password = getpass("Bot's Password: ")
	room = input("MUC JID to Join: ")
	nick = input("Bot's Nickname: ")
	server = input("PubSub Server JID: ")

	xmpp = PubSubTools(jid, password, room, nick, server, node=None, data='')
	xmpp.connect()
	xmpp.process()