# Copyright 2015, Rob Lyon <nosignsoflifehere@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import xml.dom.minidom
from qhost import Node
from qhost import NodeList
from constants import STATES
from parsers import StringParser
from parsers import IntParser
from parsers import StateParser
from parsers import JobParser
from parsers import StatusParser


class Parser_Pbsnodes:
    def __init__(self, qxml):
        self.qxml = qxml
        self.nodelist = NodeList()

    def parse(self):
        return self.handle_data()

    def handle_data(self):
        dom = xml.dom.minidom.parseString(self.qxml)
        nodes = dom.getElementsByTagName("Node")
        return self.handle_nodes(nodes)

    def handle_nodes(self, nodes):
        for node in nodes:
            self.nodelist.add(self.handle_node(node))

        return self.nodelist

    def handle_node(self, node):
        name = StringParser(node, "name").parse()
        n = Node(name)

        n.procs = IntParser(node, "np", default=0).parse()
        n.gpus = IntParser(node, "gpus", default=0).parse()
        n.properties = StringParser(node, "properties").parse()
        n.ntype = StringParser(node, "ntype").parse()
        n.state = StateParser(node, "state").parse()
        n.jobs, n.slots = JobParser(node, "jobs").parse()
        n.note = StringParser(node, "note", default='').parse()

        status = StatusParser(node, "status").parse()
        n.from_hash(status)

        return n

class Parser_Showq:
    def __init__(self, qxml):
        self.qxml = qxml
        self.joblist = NodeList()

    def parse(self):
        return self.handle_data()

    def handle_data(self):
        dom = xml.dom.minidom.parseString(self.qxml)
        jobs = dom.getElementsByTagName("job")
        return self.handle_jobs(jobs)

    def handle_jobs(self, jobs):
        for job in jobs:
            self.joblist.add(self.handle_job(job))

        return self.joblist

    def handle_job(self, job):
 
        # name = StringParser(job, "JobID").parse()
        # pull from minidom attribute method
        name = job.attributes["JobID"].value
        j = Node(name)

        # j.user = StringParser(job, "\@User", default='').parse()
        # pull from minidom attribute method
        j.userid = job.attributes["User"].value

        return j
