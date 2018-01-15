#!/usr/bin/env python
import os
import sys
from basic import config

if __name__ == "__main__":
    if sys.argv[1] == 'test':
        config.UNITTEST = 1
        
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "basic.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
