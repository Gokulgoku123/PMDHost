#!/bin/bash
# Install Java
apt update
apt install -y default-jdk unzip curl

# Download PMD if not already present
if [ ! -d "pmd-bin-7.17.0" ]; then
  curl -L -o pmd-bin.zip https://github.com/pmd/pmd/releases/download/pmd_releases%2F7.17.0/pmd-bin-7.17.0.zip
  unzip pmd-bin.zip
fi

# Run Flask
export FLASK_APP=app.py
export PORT=${PORT:-5000}
flask run --host=0.0.0.0 --port=$PORT
