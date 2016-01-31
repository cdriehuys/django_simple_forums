#!/usr/bin/env python

import os


# set up django settings before importing django
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'


from django.core import management


if __name__ == "__main__":
    management.execute_from_command_line()
