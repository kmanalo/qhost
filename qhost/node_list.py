# Copyright 2014, Rob Lyon <nosignsoflifehere@gmail.com>
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


class NodeList:
    def __init__(self):
        self.nodes = []
        self.filters = {}
        self.jobid_to_user = {}
        self.user_to_jobid = {}

    def __iter__(self):
        for node in self.nodes:
            if self.matches(node):
                yield node

    def __getitem__(self, index):
        return self.nodes[index]

    def add(self, node):
        self.nodes.append(node)

    def add_filter(self, filter, value):
        if value:
            self.filters[filter] = value

    def add_joblist(self, joblist):
        if joblist:
            # form a dictionary between jobid and 'osuXXXX'
            for job in joblist:
                self.jobid_to_user[str(job)] = job.userid

            # inverse map
            for k, v in self.jobid_to_user.iteritems():
                self.user_to_jobid[v] = self.user_to_jobid.get(v, [])
                self.user_to_jobid[v].append(k)

    def matches(self, node):
        for key, value in self.filters.iteritems():
            if not getattr(self, "filter_by_%s" % key)(node, value):
                return False
        return True

    def filter_by_jobid(self, node, jobid):
        return node.has_job(jobid)

    def filter_by_userid(self, node, userid):
        jobids = self.user_to_jobid.setdefault(userid, "None")
        return node.has_user(jobids)

    def filter_by_node_regex(self, node, regex):
        return node.matches(regex)

    def filter_by_any_state(self, node, state):
        return node.state_any_matches(state)

    def filter_by_exclusive_state(self, node, state):
        return node.state_exclusive_matches(state)
