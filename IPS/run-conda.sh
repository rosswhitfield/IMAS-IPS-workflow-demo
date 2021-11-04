#!/bin/bash
conda activate imas

ips.py --config=ips.imas.config --platform=platform.conf
ips.py --config=ips.omas.imas.config --platform=platform.conf
ips.py --config=ips.imaspy.imas.config --platform=platform.conf
