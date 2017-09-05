#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
Main package with the `emailhw` functionality
"""


from emailhw.errors import print_error
from emailhw.defaults import set_configuration,test_configuration,get_configuration

from emailhw.iochannels import mailbox_input_channel,mailbox_output_channel
from emailhw.iochannels import file_output_channel
from emailhw.iochannels import imap_input_channel,smtp_output_channel
from emailhw.messages   import print_message

from emailhw.commands   import compile_command
