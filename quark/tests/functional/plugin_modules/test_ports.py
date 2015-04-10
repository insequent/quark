# Copyright 2013 Openstack Foundation
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for# the specific language governing permissions and limitations
#  under the License.

import mock
import netaddr
from neutron.common import exceptions
from oslo.config import cfg

import contextlib

from quark.db import api as db_api
import quark.ipam
# import below necessary if file run by itself
from quark import plugin  # noqa
import quark.plugin_modules.ports as port_api
from quark.tests.functional.base import BaseFunctionalTest

CONF = cfg.CONF


class QuarkGetSubnets(BaseFunctionalTest):
    @contextlib.contextmanager
    def _stubs(self, network, subnet):
        self.ipam = quark.ipam.QuarkIpamANY()
        with self.context.session.begin():
            net_mod = db_api.network_create(self.context, **network)
            subnet["network"] = net_mod
            sub1 = db_api.subnet_create(self.context, **subnet)
            subnet["id"] = 2
            sub2 = db_api.subnet_create(self.context, do_not_use=True,
                                        **subnet)
        yield net_mod, sub1, sub2

    def test_get_subnet_do_not_use_not_returned(self):
        network = dict(name="public", tenant_id="fake", network_plugin="BASE")
        subnet = dict(id=1, ip_version=4, next_auto_assign_ip=2,
                      cidr="0.0.0.0/24", first_ip=0, last_ip=255,
                      ip_policy=None, tenant_id="fake")
        with self._stubs(network, subnet) as (net, sub1, sub2):
            subnets = db_api.subnet_find_ordered_by_most_full(self.context,
                                                              net["id"]).all()
            self.assertEqual(len(subnets), 1)
            self.assertEqual(subnets[0][0]["id"], "1")


class QuarkGetPorts(BaseFunctionalTest):
    @contextlib.contextmanager
    def _stubs(self):
        self.ipam = quark.ipam.QuarkIpamANY()
        with self.context.session.begin():
            network = dict(name="public", tenant_id="fake", network_plugin="BASE")
            subnet1 = dict(id=1, ip_version=4, next_auto_assign_ip=2,
                           cidr="10.1.0.0/24", first_ip=0, last_ip=255,
                           ip_policy=None, tenant_id="fake")
            subnet2 = dict(id=2, ip_version=4, next_auto_assign_ip=2,
                           cidr="10.2.0.0/24", first_ip=0, last_ip=255,
                           ip_policy=None, tenant_id="fake")
            new_net = db_api.network_create(self.context, **network)
            subnet1["network"] = new_net
            subnet2["network"] = new_net
            sub1 = db_api.subnet_create(self.context, **subnet1)
            sub2 = db_api.subnet_create(self.context, **subnet2)
            
        yield net_mod, sub1, sub2

    def test_get_port(self):
        fields = dict()
        with self._stubs(
            ports = ports_api.get_port(context, fields)

    def test_get_ports(self):
        fields = dict()
        with self._stubs(
            ports = ports_api.get_ports(context, fields)

    def test_get_ports_by_ip_address(self):
        fields = dict()
        with self.stubs(
            ports = ports_api.get_ports(self.context, fields)

