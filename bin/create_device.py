#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# @file   create_device.py
# @author Albert Puig (albert.puig@cern.ch)
# @date   13.02.2015
# =============================================================================
"""Create device configuration to work with the Pushbullet API."""

from __future__ import with_statement

import os
import sys
import argparse
import cPickle


def write_config(device_name, api_key, config_file):
    """Write the configuration information to file.

    :param device_name: Name of the device.
    :type device_name: str
    :param api_key: Pushbullet API key.
    :type api_key: str
    :param config_file: Output file.
    :type config_file: str

    """
    configuration = (device_name, api_key)
    with open(config_file, 'w') as file_:
        cPickle.dump(configuration, file_)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('device_name', action='store', type=str,
                        help="Name of the device to create")
    parser.add_argument('api_key', action='store', type=str,
                        help="Pushbullet API key")
    parser.add_argument('config_file', action='store', type=str,
                        help="File to save the device config to")
    args = parser.parse_args()
    # Check that the config file doesn't exist
    if os.path.exists(args.config_file):
        sys.exit("Config file already exists")
    # Write the configuration
    write_config(args.device_name, args.api_key, args.config_file)

# EOF
