#!/usr/bin/env python3

from waitress import serve
import app

serve(app.app, host='0.0.0.0', port=8080)
