#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# Configuration file
Config = {

    # Homeworks are processed from email sent to a specific address in
    # a specific mailbox in an IMAP main server
    #
    'imap server'   : None,
    'imap user'     : None,
    'imap mailbox'  : None,
    #
    # The password may be a string or a function that return a string
    #
    'imap password' : None,

    # Replies are send by mail as well
    #
    'sender'        : None,
    'smtp server'   : None,
    'smtp user'     : None,
    #
    # The password may be a string or a function that return a string
    #
    'smtp password' : None,

    # Data storage
    #
    'storage path'  : None,
    'storage db'    : None   
}


class ReadOnlyDict(dict):
    def __readonly__(self, *args, **kwargs):
        raise RuntimeError("Cannot modify ReadOnlyDict")
    __setitem__ = __readonly__
    __delitem__ = __readonly__
    pop = __readonly__
    popitem = __readonly__
    clear = __readonly__
    update = __readonly__
    setdefault = __readonly__
    del __readonly__


def test_configuration():
    """Check that everything has been configured.

    This just checks for data in the configuration entries. If the
    data does not make sense, you will only discove at runtime.

    """
    for key in Config:
        if Config[key] is None:
            return False
    return True


def set_configuration(aConfig):
    """Load the configuration in input as the default 
    """
    for key in Config:
        if key in aConfig and aConfig[key] is not None:
            Config[key] = aConfig[key]

def get_configuration():
    """Load the configuration in input as the default 
    """
    return ReadOnlyDict(Config)
