import os


class Nvm(object):
    """
    The class for work with NVM if it is installed in system
    """
    nvm_file = '.nvmrc'

    home_folder = os.path.expanduser("~")
    nvm_folder = os.path.join(home_folder, '.nvm')

    current_node_version = ''
    current_node_path = ''

    @staticmethod
    def is_installed():
        if os.name == 'nt': return None

        if os.path.exists(Nvm.nvm_folder):
            with open(os.path.join(Nvm.nvm_folder, "alias/", "default")) as f:
                Nvm.current_node_version = f.read()
            return True
        return False
            
    @staticmethod
    def get_current_node_path():
        return os.path.join(Nvm.nvm_folder, 'versions', 'node',
            Nvm.current_node_version, 'bin')