import logging
import slixmpp
from slixmpp.exceptions import XMPPError
from slixmpp.xmlstream import ET, tostring

class PubSubCommands(PubSubTools):
    # Initialization:
    def __init__(self, jid, server, node=None, data=''):
        super().__init__(self, jid, server)
        self.jid = jid
        self.server = server
        self.node = node
        self.data = data

        # This should be inherited:
        # self.register_plugin('xep_0030')
        # self.register_plugin('xep_0059')
        # self.register_plugin('xep_0060')

        self.commands = {
            ## Information:
            'nodes': self.nodes, # 0 args
            'get': self.get, # 1 args: node

            ## Manage Node:
            'create': self.create, # 1 args: node
            'delete': self.delete, # 1 args: node
            'purge': self.purge, # 1 args: node

            ## Manage Node Data:
            'publish': self.publish, # 2 args: node, data
            'retract': self.retract, # 2 args: node, data

            ## Subscription:
            'subscribe': self.subscribe, # 1 args: node
            'unsubscribe': self.unsubscribe, # 1 args: node

            ## what about: # 'set_configure': self.set_configure, # ??
            # 'get_configure': self.get_configure,
        }

### INFORMATION:
    # nodes()
    async def nodes(self):
        try:
            result = await self['xep_0060'].get_nodes(self.server, self.node)
            for item in result['disco_items']['items']:
                logging.info('  - %s', str(item))
            return True
        except XMPPError as error:
            logging.error('Could not retrieve node list: %s', error.format())
            return False


    ## get()
    async def get(self, node):
        self.node = node
        try:
            result = await self['xep_0060'].get_item(self.server, self.node, self.data)
            for item in result['pubsub']['items']['substanzas']:
                logging.info('Retrieved item %s: %s', item['id'], tostring(item['payload']))
            return True
        except XMPPError as error:
            logging.error('Could not retrieve item %s from node %s: %s', self.data, self.node, error.format())
            return False


### MANAGE NODE:
    # create()
    async def create(self, node):
        self.node = node
        try:
            await self['xep_0060'].create_node(self.server, self.node)
            logging.info('Created node %s', self.node)
            return True
        except XMPPError as error:
            logging.error('Could not create node %s: %s', self.node, error.format())
            return False


    # delete()
    async def delete(self, node):
        self.node = node
        try:
            await self['xep_0060'].delete_node(self.server, self.node)
            logging.info('Deleted node %s', self.node)
            return True
        except XMPPError as error:
            logging.error('Could not delete node %s: %s', self.node, error.format())
            return False


    # purge()
    async def purge(self, node):
        self.node = node
        try:
            await self['xep_0060'].purge(self.server, self.node)
            logging.info('Purged all items from node %s', self.node)
            return True
        except XMPPError as error:
            logging.error('Could not purge items from node %s: %s', self.node, error.format())
            return False


### MANAGE DATA:
    # publish()
    async def publish(self, node, data):
        self.node = node
        self.data = data
        payload = ET.fromstring("<test xmlns='test'>%s</test>" % self.data)
        try:
            result = await self['xep_0060'].publish(self.server, self.node, payload=payload)
            logging.info('Published at item id: %s', result['pubsub']['publish']['item']['id'])
            return True
        except XMPPError as error:
            logging.error('Could not publish to %s: %s', self.node, error.format())
            return False



    # retract()
    async def retract(self, node, data):
        self.node = node
        self.data = data
        try:
            await self['xep_0060'].retract(self.server, self.node, self.data)
            logging.info('Retracted item %s from node %s', self.data, self.node)
            return True
        except XMPPError as error:
            logging.error('Could not retract item %s from node %s: %s', self.data, self.node, error.format())
            return False


### SUBSCRIPTION:
    # subscribe()
    async def subscribe(self, node):
        self.node = node
        try:
            iq = await self['xep_0060'].subscribe(self.server, self.node)
            subscription = iq['pubsub']['subscription']
            logging.info('Subscribed %s to node %s', subscription['jid'], subscription['node'])
            return True
        except XMPPError as error:
            logging.error('Could not subscribe %s to node %s: %s', self.boundjid.bare, self.node, error.format())
            return False


    # unsubscribe()
    async def unsubscribe(self, node):
        self.node = node
        try:
            await self['xep_0060'].unsubscribe(self.server, self.node)
            logging.info('Unsubscribed %s from node %s', self.boundjid.bare, self.node)
            return True
        except XMPPError as error:
            logging.error('Could not unsubscribe %s from node %s: %s', self.boundjid.bare, self.node, error.format())
            return False

    # # get_configure()
    # async def get_configure(self):
    #     try:
    #         configuration_form = await self['xep_0060'].get_node_config(self.server, self.node)
    #         logging.info('Configure form received from node %s: %s', self.node, configuration_form['pubsub_owner']['configure']['form'])
    #     except XMPPError as error:
    #         logging.error('Could not retrieve configure form from node %s: %s', self.node, error.format())