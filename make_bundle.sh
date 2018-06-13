#!/bin/bash

pyinstaller -F -n "pinback-$(date +"%Y%m%d")" pinback.py
