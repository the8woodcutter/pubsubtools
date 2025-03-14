from getpass import getpass
from pubsub_commands import PubSubCommands as ps_commands
import asyncio
import slixmpp
import logging
import os
import random

class PubSubTools(slixmpp.ClientXMPP):

	def __init__(self, jid, password, room, nick):
		slixmpp.ClientXMPP.__init__(self, jid, password)

		self.jid = jid
		self.password = password
		self.room = room
		self.nick = nick
		self.pubsub_server = "pubsub.xmpp.packets.cc"
		self.add_event_handler("session_start", self.start)
		self.add_event_handler("groupchat_message", self.muc_message)

	async def start(self, event):
		await self.get_roster()
		self.send_presence()
		self.plugin['xep_0045'].join_muc(self.room, self.nick)

	def muc_message(self, msg):
	# ### COMMANDS:
		body = msg['body']
		parts = body.split(' ')

		# GET NODES:
		async def nodes(self):
			nodes = await ps_commands.nodes(self)
			msg.reply(nodes).send()

		if body == "!xmpp nodes":
			nodes(self)

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



	# SERVICE DISCOVERY:
	## NOT PUBSUB!
		# GET LOCAL INFO:
		async def get_info(self):
			info = await self['xep_0030'].get_info(node=self.nick, local=True)
			# info_list = info.split('\n')
			# info_str = "\r\n".join(info_list)
			msg.reply("I have yet to be figured out!").send() # !!!!!!!!!!!!!!!!!!!!

		if body == "!xmpp getinfo":
			get_info(self)

		# GET LOCAL NODE ITEMS:
		async def items(self, node):
					try:
						items = await self['xep_0030'].get_items(jid=self.jid, node=node, local=True)
						items_string = "\r\n".join(items)
						msg.reply(items_string).send()
					except:
						mesg = "Invalid Node!"
						msg.reply(mesg).send()

		if body.startswith('!xmpp items '):
			if len(parts) > 2:
				node = parts[2]
				node = str(node)
				items(self, node)

	# INFORMATIONAL:
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



if __name__ == '__main__':
	botjid_to_load_in = input("Bot's JID: ")
	botjid_to_load = str(botjid_to_load_in)

	passwd_to_load_in =  input("Password: ")
	passwd_to_load = str(passwd_to_load_in)

	botnick_to_load_in =  input("Bot's nickname: ")
	botnick_to_load = str(botnick_to_load_in)

	muc_to_load_in =  input("MUC's JID: ")
	muc_to_load = str(muc_to_load_in)

	xmpp = PubSubTools(botjid_to_load, passwd_to_load, muc_to_load, botnick_to_load)
	xmpp.register_plugin('xep_0030')  # Service Discovery
	xmpp.register_plugin('xep_0045')  # Multi-User Chat
	xmpp.register_plugin('xep_0059')  # Result Set Management
	xmpp.register_plugin('xep_0060')  # PubSub
	xmpp.register_plugin('xep_0199')  # XMPP Ping
	xmpp.connect()
	# xmpp.process()
	asyncio.get_event_loop().run_forever()
