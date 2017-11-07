# import sublime
# import sys
# import os
# from unittest import TestCase

# try:
#     from .lib.nodejs_command_thread import run_os_command
# except SystemError as e:
#     sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
#     from nodejs_command_thread import run_os_command


# class TestRunOsCommand(TestCase):

#     def testRunOsCommandNode(self):
#         cmd = ['node', '--version']
#         output = run_os_command(cmd)
#         self.assertEqual('v', output[0])

#     def testRunOsCommandLs(self):
#         cmd = ['ls', '-l']
#         output = run_os_command(cmd)
#         self.assertEqual(0, output.find('total'))