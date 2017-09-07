import os
import codecs
import sublime
import functools
import threading
import subprocess

from .nodejs_debug import debug


def main_thread(callback, *args, **kwargs):
    # sublime.set_timeout gets used to send things onto the main thread
    # most sublime.[something] calls need to be on the main thread
    sublime.set_timeout(functools.partial(callback, *args, **kwargs), 0)


def _make_text_safeish(text, fallback_encoding):
    # DEPRECATED
    #
    # The unicode decode here is because sublime converts to unicode inside
    # insert in such a way that unknown characters will cause errors, which is
    # distinctly non-ideal... and there's no way to tell what's coming out of
    # git in output. So...
    return text


class CommandThread(threading.Thread):

    def __init__(self, command, on_done, working_dir="", fallback_encoding="", env={}):
        threading.Thread.__init__(self)
        self.command = command
        self.on_done = on_done
        self.working_dir = working_dir
        self.fallback_encoding = fallback_encoding
        self.env = os.environ.copy()
        self.env.update(env)

    def run(self):
        try:
            # Per http://bugs.python.org/issue8557 shell=True is required to
            # get $PATH on Windows. Yay portable code.
            shell = os.name == 'nt'
            if self.working_dir != "":
                os.chdir(self.working_dir)
            proc = subprocess.Popen(self.command,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    shell=shell, universal_newlines=False, env=self.env)
            output = codecs.decode(proc.communicate()[0])
            # if sublime's python gets bumped to 2.7 we can just do:
            # output = subprocess.check_output(self.command)
            main_thread(self.on_done, output)
        except subprocess.CalledProcessError as e:
            main_thread(self.on_done, e.returncode)
        except OSError as e:
            if e.errno == 2:
                main_thread(
                    sublime.error_message, """Node binary could not be found in PATH

                    Consider using the node_command setting for the Node plugin

                    PATH is: %s""" % os.environ['PATH'])
            else:
                raise e


class OsThread(CommandThread):

    def __init__(self, command, on_done, shell=False, working_dir="", fallback_encoding="", env={}):
        super().__init__(command, on_done, working_dir, fallback_encoding, env)
        self.shell = shell

    def run(self):
        try:
            if not self.shell:
                self.shell = os.name == 'nt'

            if self.working_dir != "":
                os.chdir(self.working_dir)

            proc = subprocess.Popen(self.command, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, shell=self.shell, env=self.env)
            output = codecs.decode(proc.communicate()[0])
            self.on_done(output)
        except subprocess.CalledProcessError as e:
            self.on_done(e.returncode, error=True)
        except OSError as e:
            self.on_done(e.message, error=True)
