# -*- coding: utf-8 -*-

#    Copyright 2015 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from fuelclient.tests.unit.v1 import base


class TestParser(base.UnitTestCase):

    def test_choose_only_one_format(self):
        with mock.patch('sys.stderr') as mstderr:
            self.assertRaises(SystemExit,
                              self.execute,
                              ['fuel', '--json', '--yaml'])
        args, _ = mstderr.write.call_args
        self.assertRegexpMatches(
            args[0],
            r"argument (--json|--yaml): not allowed with"
            r" argument (--yaml|--json)")
