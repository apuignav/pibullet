#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# @file   device.py
# @author Albert Puig (albert.puig@cern.ch)
# @date   28.01.2015
# =============================================================================
"""Wrapper for the Raspberry Pi device."""

from __future__ import with_statement
import os
import cPickle

from error import ConfigFileError, PushBulletError

from pushbullet import PushBullet, Listener


class Device(object):
    """Wrapper class for the pushbullet device."""

    def __init__(self, config_file):
        """Load device.

        :param config_file: Configuration file.
        :type config_file: str

        :raises: error.ConfigFileError: if the config file
                                        cannot be loaded.
        :raises: error.PushBulletError: if there are errors in
                                        communicating with the API.

        """
        if not os.path.exists(config_file):
            raise ConfigFileError("Cannot find config file!")
        with open(config_file) as file_:
            device_name, api_key = cPickle.load(file_)
        assert api_key
        pb_api = PushBullet(api_key)
        device = None
        for dev in pb_api.devices:
            if dev.nickname == device_name and dev.active:
                device = dev
                break
        if not device:
            # We need to create the device!
            success, device = pb_api.new_device(device_name)
            if not success:
                raise PushBulletError("Failed creation of device!")
        self._device = device
        self._pb_api = pb_api
        self._commands = {}
        self.last_push = 0

    def notify(self, title, message, device=None):
        """Push notification.

        If message is a list, send a list.

        :param title: Title of the notification.
        :type title: str
        :param message: Message to push.
        :type message: object
        :param device: Device to push to.
        :type device: str

        :returns: Output of the push command.
        :rtype: str

        """
        if isinstance(message, (list, tuple)):
            return self._pb_api.push_list(title, message, device=device)
        else:
            return self._pb_api.push_note(title, str(message), device=device)

    def register_command(self, command, callback):
        """Add command to the list of accepted commands for the listen function.

        :param command: Command to add.
        :type command: str
        :param callback: Function to call when command is requested.
        :type callback: function

        :raises: KeyError: If the command is already registered.

        """
        if command in self._commands:
            raise KeyError("Command already registered -> %s" % command)
        self._commands[command] = callback

    def listen(self):
        """Run and wait for commands."""
        listener = Listener(self._pb_api, on_push=self._push_handler)
        self._check_pushes()
        listener.run()

    def _push_handler(self, push):
        """Handler the push notifications.

        Only tickle pushes are picked up and forwarded
        to _check_pushes.

        :param push: Push message.
        :type push: str

        """
        if push["type"] == "tickle":
            # print "TICKLE"
            self._check_pushes()

    def _check_pushes(self):
        """Handler the push notifications.

        First, the destination of the message is checked: it is only
        considered if the current device is its only recipient.
        Afterwards, the message is analyzed.

        For notes, its title and body are used to specified the action
        'command' and the command to be executed. If a suitable command
        is found it is executed and an answer (if any) is returned to the
        pusher in form of a notification.

        If a file is pushed, it is downloaded and the download location
        is returned.

        :raises: PushBulletError: if the API get_pushes fails.

        """
        success, pushes = self._pb_api.get_pushes(self.last_push)
        if not success:
            raise PushBulletError("Cannot get pushes")
        push_list = []
        for push in pushes:
            # Get non-dismissed pushes directed to us
            if push.get("target_device_iden", None) == self._device.device_iden and \
                    not push.get("dismissed", True):
                push_list.append(push)
                self._pb_api.dismiss_push(push.get("iden"))
            self.last_push = max(self.last_push, push.get("created"))
        for push in push_list:
            if push['type'] == 'note':
                if push['title'] == 'command':  # We have a command
                    body = push['body'].split()
                    command = body[0]
                    args = body[1:] if len(body) > 1 else list()
                    if command in self._commands:
                        answer = self._commands[command](*args)
                        if answer:
                            title, body = answer
                            pusher = push.get('source_device_iden', None)
                            print pusher
                            if pusher:
                                for dev in self._pb_api.devices:
                                    if dev.device_iden == pusher:
                                        pusher = dev
                                        break
                            print title, body, pusher
                            self.notify(title, body, pusher)

# EOF
