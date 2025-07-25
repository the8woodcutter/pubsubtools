import logging
from getpass import getpass
from argparse import ArgumentParser
import os
import slixmpp
import asyncio
from slixmpp.exceptions import XMPPError
from slixmpp.xmlstream import ET, tostring


class PubSubTools(slixmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick, server):
        super().__init__(jid, password)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0059')
        self.register_plugin('xep_0060')
        self.register_plugin('xep_0045')

        self.room = room
        self.nick = nick
        self.node = None
        self.data = ''
        self.pubsub_server = server

        self.add_event_handler('session_start', self.start)
        self.add_event_handler('groupchat_message', self.muc_message)

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].join_muc(self.room, self.nick)

    async def muc_message(self, msg):
        # do the stuff where messages make commands:              
        ## 
        if msg['body'] == "^pubsub nodes":
            await self.nodes()

    async def nodes(self):
        try:
            result = await self['xep_0060'].get_nodes(self.pubsub_server)
            results = []
            for item in result['disco_items']['items']:
                logging.info('  - %s', str(item))
                results.append(f'  - {item}')
            results = "\r\n".join(results)
            return results
        except XMPPError as error:
            logging.error('Could not retrieve node list: %s', error.format())
            return f'Could not retrieve node list: {error}'

    # async def create(self):
    #     try:
    #         await self['xep_0060'].create_node(self.pubsub_server, self.node)
    #         logging.info('Created node %s', self.node)
    #     except XMPPError as error:
    #         logging.error('Could not create node %s: %s', self.node, error.format())

    # async def delete(self):
    #     try:
    #         await self['xep_0060'].delete_node(self.pubsub_server, self.node)
    #         logging.info('Deleted node %s', self.node)
    #     except XMPPError as error:
    #         logging.error('Could not delete node %s: %s', self.node, error.format())

    # async def get_configure(self):
    #     try:
    #         configuration_form = await self['xep_0060'].get_node_config(self.pubsub_server, self.node)
    #         logging.info('Configure form received from node %s: %s', self.node, configuration_form['pubsub_owner']['configure']['form'])
    #     except XMPPError as error:
    #         logging.error('Could not retrieve configure form from node %s: %s', self.node, error.format())

    # async def publish(self):
    #     payload = ET.fromstring("<test xmlns='test'>%s</test>" % self.data)
    #     try:
    #         result = await self['xep_0060'].publish(self.pubsub_server, self.node, payload=payload)
    #         logging.info('Published at item id: %s', result['pubsub']['publish']['item']['id'])
    #     except XMPPError as error:
    #         logging.error('Could not publish to %s: %s', self.node, error.format())

    # async def get(self):
    #     try:
    #         result = await self['xep_0060'].get_item(self.pubsub_server, self.node, self.data)
    #         for item in result['pubsub']['items']['substanzas']:
    #             logging.info('Retrieved item %s: %s', item['id'], tostring(item['payload']))
    #     except XMPPError as error:
    #         logging.error('Could not retrieve item %s from node %s: %s', self.data, self.node, error.format())

    # async def retract(self):
    #     try:
    #         await self['xep_0060'].retract(self.pubsub_server, self.node, self.data)
    #         logging.info('Retracted item %s from node %s', self.data, self.node)
    #     except XMPPError as error:
    #         logging.error('Could not retract item %s from node %s: %s', self.data, self.node, error.format())

    # async def purge(self):
    #     try:
    #         await self['xep_0060'].purge(self.pubsub_server, self.node)
    #         logging.info('Purged all items from node %s', self.node)
    #     except XMPPError as error:
    #         logging.error('Could not purge items from node %s: %s', self.node, error.format())

    # async def subscribe(self):
    #     try:
    #         iq = await self['xep_0060'].subscribe(self.pubsub_server, self.node)
    #         subscription = iq['pubsub']['subscription']
    #         logging.info('Subscribed %s to node %s', subscription['jid'], subscription['node'])
    #     except XMPPError as error:
    #         logging.error('Could not subscribe %s to node %s: %s', self.boundjid.bare, self.node, error.format())

    # async def unsubscribe(self):
    #     try:
    #         await self['xep_0060'].unsubscribe(self.pubsub_server, self.node)
    #         logging.info('Unsubscribed %s from node %s', self.boundjid.bare, self.node)
    #     except XMPPError as error:
    #         logging.error('Could not unsubscribe %s from node %s: %s', self.boundjid.bare, self.node, error.format())

if __name__ == '__main__':
    botjid_to_load_in = input("Bot's JID: ")
    botjid_to_load = str(botjid_to_load_in)

    passwd_to_load_in =  input("Password: ")
    passwd_to_load = str(passwd_to_load_in)

    botnick_to_load_in =  input("Bot's nickname: ")
    botnick_to_load = str(botnick_to_load_in)

    muc_to_load_in =  input("MUC's JID: ")
    muc_to_load = str(muc_to_load_in)

    pubsub_server_to_load_in = input("PubSub Server JID: ")
    pubsub_server_to_load = str(pubsub_server_to_load_in)

    xmpp = PubSubTools(botjid_to_load, passwd_to_load, muc_to_load, botnick_to_load, pubsub_server_to_load)
    # xmpp.register_plugin('xep_0030')  # Service Discovery
    # xmpp.register_plugin('xep_0045')  # Multi-User Chat
    # # xmpp.register_plugin('xep_0059')  # Result Set Management
    # xmpp.register_plugin('xep_0060')  # PubSub
    # xmpp.register_plugin('xep_0199')  # XMPP Ping
    xmpp.connect()
    xmpp.process()
    # asyncio.get_event_loop().run_forever()



# if __name__ == '__main__':
#     # Setup the command line arguments.
#     parser = ArgumentParser()
#     parser.version = '%%prog 0.1'
#     parser.usage = "Usage: %%prog [options] <jid> " + \
#                              'nodes|create|delete|get_configure|purge|subscribe|unsubscribe|publish|retract|get' + \
#                              ' [<node> <data>]'

#     parser.add_argument("-q","--quiet", help="set logging to ERROR",
#                         action="store_const",
#                         dest="loglevel",
#                         const=logging.ERROR,
#                         default=logging.INFO)
#     parser.add_argument("-d","--debug", help="set logging to DEBUG",
#                         action="store_const",
#                         dest="loglevel",
#                         const=logging.DEBUG,
#                         default=logging.INFO)

#     # JID and password options.
#     parser.add_argument("-j", "--jid", dest="jid",
#                         help="JID to use")
#     parser.add_argument("-p", "--password", dest="password",
#                         help="password to use")

#     parser.add_argument("server")
#     parser.add_argument("action", choices=["nodes", "create", "delete", "get_configure", "purge", "subscribe", "unsubscribe", "publish", "retract", "get"])
#     parser.add_argument("node", nargs='?')
#     parser.add_argument("data", nargs='?')

#     args = parser.parse_args()

#     # Setup logging.
#     logging.basicConfig(level=args.loglevel,
#                         format='%(levelname)-8s %(message)s')

#     if args.jid is None:
#         args.jid = input("Username: ")
#     if args.password is None:
#         args.password = getpass("Password: ")

#     # Setup the Pubsub client
#     xmpp = PubsubClient(args.jid, args.password,
#                         server=args.server,
#                         node=args.node,
#                         action=args.action,
#                         data=args.data)

#     # Connect to the XMPP server and start processing XMPP stanzas.
#     xmpp.connect()
#     xmpp.process(forever=False)