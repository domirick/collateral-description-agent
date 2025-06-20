#!/bin/bash

python -m phoenix.server.main serve
python app-v2/app.py loadenv