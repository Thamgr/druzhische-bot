#!/bin/bash
sudo systemctl status druzhische-bot
sudo journalctl -u druzhische-bot -n 50 --no-pager