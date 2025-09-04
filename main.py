#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import signal
import argparse
from termcolor import colored
from forward_shell import ForwardShell


def get_arguments():
    """
    Parse command-line arguments.
    Requires: -u / --url (the target webshell URL).
    """

    parser = argparse.ArgumentParser(description="Forward-Shell tool")
    parser.add_argument("-u", "--url", dest="url", required=True,
            help="Web-Shell url (Ex: -u 'example/shell.php')")
    return parser.parse_args()

def handler(sig, frame):
    """
    Handle Ctrl+C (SIGINT).
    Cleans up remote pipes and exits.
    """

    print(colored(f"\n\n[!] Stopping...\n", 'red'))
    forward_shell.remove_data()
    sys.exit(1)

signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':
    # Parse arguments and start ForwardShell

    args = get_arguments()
    forward_shell = ForwardShell(args.url)
    forward_shell.run()

