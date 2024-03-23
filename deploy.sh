#!/bin/bash
rsync -avz --delete requirements.txt src wsgi.py marcos@10.77.0.10:backend
ssh marcos@10.77.0.10 'source ~/backend/venv/bin/activate && pip install -r ~/backend/requirements.txt'
ssh marcos@10.77.0.10 'sudo supervisorctl reload'