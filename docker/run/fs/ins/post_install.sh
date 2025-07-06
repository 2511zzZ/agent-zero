#!/bin/bash
set -e

# Build Board UI for production
bash /ins/build_board_ui.sh "$@"

# Cleanup package list
rm -rf /var/lib/apt/lists/*
apt-get clean