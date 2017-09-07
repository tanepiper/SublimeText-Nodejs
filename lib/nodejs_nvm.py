import os


class Nvm(object):
    """
    The class for work with NVM if it is installed in system
    """
    nvm_file = '.nvmrc'
    project_folder = sublime.active_window().folders()[0]

    home_folder = os.path.expanduser("~")
    nvm_folder = os.path.join(Nvm.home_folder, '.nvm')

    current_node_version = ''
    current_node_path = ''

    @staticmethod
    def is_installed(self):
        if os.name == 'nt': return

        if os.path.exists(Nvm.nvm_folder):
            with open(os.path.join(Nvm.nvm_folder, "alias/", "default")) as f:
                Nvm.current_node_version = f.read()
            return True
        return False
            
    @staticmethod
    def get_current_node_path(self):
        return os.path.join(Nvm.nvm_folder, 'versions', 'node',
            Nvm.current_node_version, 'bin')