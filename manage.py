#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    # Only touch MySQL for commands that need the database
    if len(sys.argv) > 1 and sys.argv[1] in {"makemigrations", "migrate", "runserver", "test", "createsuperuser"}:
        # runserver's auto-reloader re-runs this file; only create the DB once
        if os.environ.get("RUN_MAIN") != "true":
            from config.dbsetup import ensure_database
            ensure_database()
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
