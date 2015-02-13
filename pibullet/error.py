#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# @file   error.py
# @author Albert Puig (albert.puig@cern.ch)
# @date   28.01.2015
# =============================================================================
"""Errors and exceptions."""


class ConfigFileError(Exception):
    """Configuration-file related exceptions."""


class PushBulletError(Exception):
    """Class for errors in the calls to PushBullet."""

# EOF
