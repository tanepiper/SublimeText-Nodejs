import os
import re
import shellenv

from .nodejs_debug import debug
from .nodejs_command_thread import run_os_command

class Nvm(object):
    """
    The class for work with NVM if it is installed in system
    """
    nvm_file = '.nvmrc'

    user_env = shellenv.get_env()[1]

    current_node_version = ''
    current_node_path = ''

    @staticmethod
    def is_installed():
        if os.name == 'nt': return None

        if not Nvm.user_env.get('NVM_BIN', False): return False

        return True

    @staticmethod
    def node_version():
        rx = r'v\d+\.\d+\.\d+'

        if not Nvm.is_installed(): return False
        
        if not Nvm.user_env.get('NVM_SYMLINK_CURRENT', False):
            debug('NVM_SYMLINK_CURRENT', False)
            Nvm.current_node_version = re.findall(rx, 
                    Nvm.user_env.get('NVM_BIN', False))[0]
        else:
            debug('NVM_SYMLINK_CURRENT', True)
            home_dir = os.path.expanduser("~/.nvm/current")
            realpath = os.path.realpath(home_dir)
            Nvm.current_node_version = re.findall(rx, realpath)[0]
        return Nvm.current_node_version
            
    @staticmethod
    def get_current_node_path():
        if os.name == 'nt': return None

        Nvm.current_node_path = Nvm.user_env.get('NVM_BIN', False)
        return Nvm.current_node_path