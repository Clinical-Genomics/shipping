"""
shipping.__main__

The main entry point for the command line interface.

Invoke as ``ship`` (if installed)
or ``python -m shio`` (no install required).
"""
import sys

from shipping.cli.base import cli

def main():
    sys.exit(cli())

if __name__ == '__main__':
    main()


