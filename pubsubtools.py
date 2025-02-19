from getpass import getpass
from pubsub_commands import PubSubCommands as ps_commands
import asyncio
import slixmpp
import logging
import os

class PubSubTools(slixmpp.ClientXMPP):
	def __init__(self, jid, password, room, nick, server, node, data):
		super().__init__(self, jid, password)

		self.jid = jid
		self.password = password
		self.room = room
		self.nick = nick
		self.pubsub_server = server
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

	def muc_message(self, msg):

		# ABOUT:
		if msg['body'] == "!xmpp about":
			mesgs = [
				"xmpp:xmpptools@packets.cc",
				"PubSubToolz aka XMPP Toolz aka xmpptools",
				"*Current State:*",
				"- Development",
				"  - Very Not Working!"
			]
			mesg = "\r\n".join(mesgs)
			msg.reply(mesg).send()

		# HELP:
		if msg['body'] == "!xmpp help":
			mesgs = [
				"`!xmpp nodes` - to get nodes from bot's pubsub server",
				"`!xmpp get <node_name>` - get's node items with valid node name",
			]
			mesg = "\r\n".join(mesgs)
			msg.reply(mesg).send()

		### COMMANDS:
		body = msg['body']
		parts = body.split(' ')

		if body == "!xmpp nodes":
			test = ps_commands.nodes(self)
			if test == True:
				pass # write to muc a message of ____
			elif test == False:
				pass # write to muc (maybe) error of ____
			else:
				pass # handle an obscene error of unknown-ness

		if len(parts) > 2:
			if parts[0] == "!xmpp":
				if len(parts) == 3: # 1 args: node
					node = parts[2]
					node = str(node)
					
					if parts[1] == "get":
						get = ps_commands.get(self, node)
					elif parts[1] == "create":
						create = ps_commands.create(self, node)
					elif parts[1] == "delete":
						delete = ps_commands.delete(self, node)
					elif parts[1] == "purge":
						purge = ps_commands.purge(self, node)
					elif parts[1] == "subscribe":
						subscribe = ps_commands.subscribe(self, node)
					elif parts[1] == "unsubscribe":
						unsubscribe = ps_commands.unsubscribe(self, node)
					else:
						pass # write to muc (maybe) error of ____

				# publish, retract:
				elif len(parts) == 4: # 2 args: node, data
					pass


if __name__ == '__main__':
	jid = input("Bot's JID: ")
	password = getpass("Bot's Password: ")
	room = input("MUC JID to Join: ")
	nick = input("Bot's Nickname: ")
	server = input("PubSub Server JID: ")

	xmpp = PubSubTools(jid, password, room, nick, server, node=None, data='')
	xmpp.connect()
	xmpp.process()