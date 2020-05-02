#!/usr/bin/env bash
nohup python3 waitress_server.py > app.log 2>&1 &
