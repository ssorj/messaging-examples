#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import print_function

import sys

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

class SendHandler(MessagingHandler):
    def __init__(self, connection_url, address, message_body):
        super(SendHandler, self).__init__()

        self.connection_url = connection_url
        self.address = address
        self.message_body = message_body

        self.sent = False
    
    def on_start(self, event):
        event.container.connect(self.connection_url)

    def on_connection_opened(self, event):
        print("SEND: Connected to '{0}'".format(self.connection_url))
        
        event.container.create_sender(self.address)

    def on_link_opened(self, event):
        print("SEND: Created sender for target address '{0}'".format(self.address))

    def on_sendable(self, event):
        if self.sent:
            return

        message = Message(self.message_body)
        event.sender.send(message)

        print("SEND: Sent message '{0}'".format(self.message_body))
        
        event.connection.close()

        self.sent = True

    # on_accepted

def main():
    try:
        connection_url, address, message_body = sys.argv[1:]
    except:
        sys.exit("Usage: send.py CONNECTION-URL ADDRESS MESSAGE")

    handler = SendHandler(connection_url, address, message_body)
    container = Container(handler)
    container.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
