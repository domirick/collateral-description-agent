#!/bin/bash

python -m phoenix.server.main serve
python app/app.py loadenv