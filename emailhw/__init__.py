#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
Main package with the `emailhw` functionality
"""



from emailhw.iochannels import mailbox_input_channel,mailbox_output_channel
from emailhw.iochannels import pipe_io_channel,file_output_channel
from emailhw.iochannels import imap_input_channel,smtp_output_channel

from emailhw.messages   import print_message
from emailhw.errors     import print_error


from emailhw.commands   import compile_command,CompilationFailed
