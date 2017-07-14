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

from proton import *
from proton.handlers import *
from proton.reactor import *

class Receiver(MessagingHandler):
    def __init__(self, address, max_count):
        super(Receiver, self).__init__()

        self.address = address
        self.max_count = max_count

        self.count = 0
    
    def on_start(self, event):
        event.container.create_receiver(self.address)

        print("RECEIVER: Created receiver for source address '{0}'".format(self.address))

    def on_message(self, event):
        print("RECEIVER: Received message '{0}'".format(event.message.body))

        self.count += 1

        if self.count == self.max_count:
            event.connection.close()

try:
    address = sys.argv[1]
except:
    sys.exit("Usage: receiver.py ADDRESS [MAX-COUNT]")
    
try:
    max_count = int(sys.argv[2])
except:
    max_count = 0
    
handler = Receiver(address, max_count)
container = Container(handler)

try:
    container.run()
except KeyboardInterrupt:
    pass
