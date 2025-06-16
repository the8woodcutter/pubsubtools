# NOTES FOR THIS FILE:
## Afterwards we will want to make sure that SOMEHOW this script is called from another script (pubsubtools.py)
### that is ALSO handling an XMPP JID login session
### This is slow!!!!

    # WE *COULD* STACK BOTH OF THESE CLASSES ONTOP INTHE SAME FILE!
    ## THEN HOW DO WE EXECUTE IT?
import logging
import slixmpp
from slixmpp.exceptions import XMPPError
from slixmpp.xmlstream import ET, tostring

class PubSubCommands(slixmpp.ClientXMPP):
    # THIS CLASS HOLDS ALL THE COMMAND FUNCTIONS FOR PUBSUBTOOLS:
    ## IT TAKES DATA FROM PUBSUBTOOLS.PY AND RETURNS, AFTER LOGGING ITSELF (THIS SCRIPT) INTO XMPP
    ### SERVER AND GETTING ANY PUBSUB REACTION //  THEN RETURNS BOOLEAN OR DATA TO PUBSUBTOOLS.PY 
    # Initialization:
    def __init__(self, jid, server, node=None, data=''):
        super().__init__(self, jid, server)
        self.jid = jid
        self.pubsub_server = server
        self.node = node
        self.data = data

        # self.commands = {
        #     ## Information:
        #     'nodes': self.nodes, # 0 args
        #     'get': self.get, # 1 args: node

        #     ## Manage Node:
        #     'create': self.create, # 1 args: node
        #     'delete': self.delete, # 1 args: node
        #     'purge': self.purge, # 1 args: node

        #     ## Manage Node Data:
        #     'publish': self.publish, # 2 args: node, data
        #     'retract': self.retract, # 2 args: node, data

        #     ## Subscription:
        #     'subscribe': self.subscribe, # 1 args: node
        #     'unsubscribe': self.unsubscribe, # 1 args: node

        #     ## what about: # 'set_configure': self.set_configure, # ??
        #     # 'get_configure': self.get_configure,
        # }

### QUERY DATA:
    # WHAT NODES AND THEIR NAMES?
    ## THIS IS TOP LEVEL `NODES`
    # nodes()
    async def nodes(self):
        try:
            result = await self['xep_0060'].get_nodes(self.pubsub_server, self.node)
            nodes_list = []
            for item in result['disco_items']['items']:
                nodes_list.append(str(item))
                logging.info('  - %s', str(item))
            if len(nodes_list) > 0:
                nodes_str = "\r\n".join(nodes_list)
                return nodes_str
        except XMPPError as error:
            logging.error(f'Could not retrieve node list: {error}')
            return f"Could not retrieve node list: {error}"

    # WHAT IS THE DATA IN A NODE?
    ## THIS IS `NODES->ITEMS`
    ## get()
    async def get(self, node):
        self.node = node
        try:
            result = await self['xep_0060'].get_item(self.pubsub_server, self.node, self.data)
            for item in result['pubsub']['items']['substanzas']:
                logging.info('Retrieved item %s: %s', item['id'], tostring(item['payload']))
            return True
        except XMPPError as error:
            logging.error('Could not retrieve item %s from node %s: %s', self.data, self.node, error.format())
            return False


# ### MANAGE NODES: ----------------------------------------------------------------
#     # create()
#     async def create(self, node):
#         self.node = node
#         try:
#             await self['xep_0060'].create_node(self.pubsub_server, self.node)
#             logging.info('Created node %s', self.node)
#             return True
#         except XMPPError as error:
#             logging.error('Could not create node %s: %s', self.node, error.format())
#             return False


#     # delete()
#     async def delete(self, node):
#         self.node = node
#         try:
#             await self['xep_0060'].delete_node(self.pubsub_server, self.node)
#             logging.info('Deleted node %s', self.node)
#             return True
#         except XMPPError as error:
#             logging.error('Could not delete node %s: %s', self.node, error.format())
#             return False


#     # purge()
#     async def purge(self, node):
#         self.node = node
#         try:
#             await self['xep_0060'].purge(self.pubsub_server, self.node)
#             logging.info('Purged all items from node %s', self.node)
#             return True
#         except XMPPError as error:
#             logging.error('Could not purge items from node %s: %s', self.node, error.format())
#             return False


# ### MANAGE PUBLICATION: ----------------------------------------------------------
#     # publish()
#     async def publish(self, node, data):
#         self.node = node
#         self.data = data
#         payload = ET.fromstring("<test xmlns='test'>%s</test>" % self.data)
#         try:
#             result = await self['xep_0060'].publish(self.pubsub_server, self.node, payload=payload)
#             logging.info('Published at item id: %s', result['pubsub']['publish']['item']['id'])
#             return True
#         except XMPPError as error:
#             logging.error('Could not publish to %s: %s', self.node, error.format())
#             return False



#     # retract()
#     async def retract(self, node, data):
#         self.node = node
#         self.data = data
#         try:
#             await self['xep_0060'].retract(self.pubsub_server, self.node, self.data)
#             logging.info('Retracted item %s from node %s', self.data, self.node)
#             return True
#         except XMPPError as error:
#             logging.error('Could not retract item %s from node %s: %s', self.data, self.node, error.format())
#             return False


# ### MANAGE SUBSCRIPTION: ---------------------------------------------------------
#     # subscribe()
#     async def subscribe(self, node):
#         self.node = node
#         try:
#             iq = await self['xep_0060'].subscribe(self.pubsub_server, self.node)
#             subscription = iq['pubsub']['subscription']
#             logging.info('Subscribed %s to node %s', subscription['jid'], subscription['node'])
#             return True
#         except XMPPError as error:
#             logging.error('Could not subscribe %s to node %s: %s', self.boundjid.bare, self.node, error.format())
#             return False


#     # unsubscribe()
#     async def unsubscribe(self, node):
#         self.node = node
#         try:
#             await self['xep_0060'].unsubscribe(self.pubsub_server, self.node)
#             logging.info('Unsubscribed %s from node %s', self.boundjid.bare, self.node)
#             return True
#         except XMPPError as error:
#             logging.error('Could not unsubscribe %s from node %s: %s', self.boundjid.bare, self.node, error.format())
#             return False

    # # get_configure()
    # async def get_configure(self):
    #     try:
    #         configuration_form = await self['xep_0060'].get_node_config(self.pubsub_server, self.node)
    #         logging.info('Configure form received from node %s: %s', self.node, configuration_form['pubsub_owner']['configure']['form'])
    #     except XMPPError as error:
    #         logging.error('Could not retrieve configure form from node %s: %s', self.node, error.format())