import sublime
import sys
import os
from unittest import TestCase


try:
    from .lib.nodejs_nvm import Nvm
except SystemError as e:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
    from nodejs_nvm import Nvm


class TestNodeNvm(TestCase):

    def setUp(self):
        if os.name != 'nt':
            self.user_node = False

            self.home_path = os.path.expanduser('~')
            self.nvm_path = os.path.join(self.home_path, '.nvm')
            self.nvm_bin_path = os.path.join(self.home_path, '.nvm/versions/node/v8.4.0/bin')
            self.alias_path = os.path.join(self.home_path, '.nvm', 'alias')
            self.alias_default_path = os.path.join(self.alias_path, 'default')

            if not os.path.exists(self.nvm_path):
                os.makedirs(self.nvm_path); os.makedirs(self.alias_path)
            else:
                # saving current node version
                self.user_node = True
                with open(self.alias_default_path, 'r') as f:
                    self.user_node_version = f.read()

            with open(self.alias_default_path, 'w') as f:
                f.write('v8.4.0')


    def tearDown(self):
        if os.name != 'nt' and not self.user_node:
            os.removedirs(os.path.join(self.home_path, '.nvm'))
            with open(self.alias_default_path, 'w') as f:
                f.write(self.user_node_version)

    def testIfSystemIsNt(self):
        if os.name == 'nt':
            self.assertEqual(Nvm.is_installed(), None)
        else:
            self.assertEqual(Nvm.is_installed(), True)

    def testCurrentNodePath(self):
        if os.name != 'nt':
            self.assertEqual(Nvm.get_current_node_path(), self.nvm_bin_path)
        else:
            self.assertEqual(Nvm.get_current_node_path(), None)