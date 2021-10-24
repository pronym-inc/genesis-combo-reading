#!venv/bin/python3.10
import os.path
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "genesis_combo_reading.conf.environments.local")
    path = os.path.dirname(__file__)
    sys.path.append(path)
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
