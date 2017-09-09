import os


class Nvm(object):
    """
    The class for work with NVM if it is installed in system
    """
    nvm_file = '.nvmrc'

    home_folder = os.path.expanduser("~")
    nvm_folder = os.path.join(home_folder, '.nvm')
    default_alias_path = os.path.join(nvm_folder, "alias/", "default")

    current_node_version = ''
    current_node_path = ''

    @staticmethod
    def is_installed():
        if os.name == 'nt': return None

        if not os.path.exists(Nvm.default_alias_path): return False

        return True
            
    @staticmethod
    def get_current_node_path():
        if os.name == 'nt': return None

        with open(Nvm.default_alias_path) as f:
            Nvm.current_node_version = f.read()

        return os.path.join(Nvm.nvm_folder, 'versions', 'node',
            Nvm.current_node_version, 'bin')