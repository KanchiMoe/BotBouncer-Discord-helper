from .shadowban_check import shadowban_check as _shadowban_check

from functools import wraps
@wraps(_shadowban_check)
def shadowban_check(*args, **kwargs):
    return _shadowban_check(*args, **kwargs)