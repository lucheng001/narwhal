#!/usr/bin/env bash

BASEDIR=$(cd "$(dirname "$0")";pwd)
APPDIR=$(dirname "$BASEDIR")
VENV="$APPDIR/venv"

GUNICORN="$VENV/bin/gunicorn"
CONFIGFILE="$APPDIR/webservers/app-gunicorn-cfg.py"

PIDFILE="$APPDIR/run/app.pid"

if [ -e "$PIDFILE" ]; then
    exit 0
fi

source "$VENV/bin/activate"

cd "$APPDIR"

$GUNICORN --config $CONFIGFILE wsgi:app

