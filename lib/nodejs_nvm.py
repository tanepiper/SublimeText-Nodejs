import os
import re
import shellenv


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
        if not is_installed(): return False
        Nvm.current_node_version = re.findall(r'v\d+\.\d+\.\d+')[0]
        return Nvm.current_node_version
            
    @staticmethod
    def get_current_node_path():
        if os.name == 'nt': return None

        Nvm.current_node_path = Nvm.user_env.get('NVM_BIN', False)
        return Nvm.current_node_path