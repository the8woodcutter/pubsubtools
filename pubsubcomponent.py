#!/usr/bin/env python3

# Slixmpp: The Slick XMPP Library
# Copyright (C) 2010  Nathanael C. Fritz
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

import logging
from getpass import getpass
from argparse import ArgumentParser

import asyncio
import slixmpp
import re
from slixmpp.componentxmpp import ComponentXMPP


class PubSubComponent(ComponentXMPP):

    """
    A simple Slixmpp component that echoes messages.
    """

    def __init__(self, jid, secret, server, port):
        ComponentXMPP.__init__(self, jid, secret, server, port)

        # You don't need a session_start handler, but that is
        # where you would broadcast initial presence.

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Since a component may send messages from any number of JIDs,
        it is best to always include a from JID.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        # The reply method will use the messages 'to' JID as the
        # outgoing reply's 'from' JID.
        msg.reply("Thanks for sending\n%(body)s" % msg).send()

        if msg['type'] == normal:
            frm = msg['from']
            body = msg['body']
            parts = body.split(' ')
            if len(parts) > 1:
                if parts[0] == "create":
                    node = " ".join(parts[1:])
                    create(self.pubsub_server, node)
                elif parts[0] == "delete":
                    node = " ".join(parts[1:])
                    delete(self.pubsub_server, node)
                elif parts[0] == "publish":
                    node = parts[1]
                    data = " ".join(parts[2:])
                    publish(self.pubsub_server, node, data)
                elif parts[0] == "get":
                    node = parts[1]
                    data = " ".join(parts[2:])
                    get(self.pubsub_server, node, data)
                else:
                    pass
            elif len(parts) == 1:
                if parts[0] == "nodes":
                    nodes(self.pubsub_server)

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
    # Setup the command line arguments.
    parser = ArgumentParser(description=EchoComponent.__doc__)

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-s", "--server", dest="server",
                        help="server to connect to")
    parser.add_argument("-P", "--port", dest="port",
                        help="port to connect to")

    args = parser.parse_args()

    if args.jid is None:
        args.jid = input("Component JID: ")
    if args.password is None:
        args.password = getpass("Password: ")
    if args.server is None:
        args.server = input("Server: ")
    if args.port is None:
        args.port = int(input("Port: "))

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    # Setup the EchoComponent and register plugins. Note that while plugins
    # may have interdependencies, the order in which you register them does
    # not matter.
    xmpp = EchoComponent(args.jid, args.password, args.server, args.port)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    asyncio.get_event_loop().run_forever()