#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import operator
import sys

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

PY2 = sys.version_info[0] == 2
WIN = sys.platform.startswith('win')

_identity = lambda x: x

if PY2:
    unichr = unichr
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)

    iterkeys = lambda d, *args, **kwargs: d.iterkeys(*args, **kwargs)
    itervalues = lambda d, *args, **kwargs: d.itervalues(*args, **kwargs)
    iteritems = lambda d, *args, **kwargs: d.iteritems(*args, **kwargs)

    iterlists = lambda d, *args, **kwargs: d.iterlists(*args, **kwargs)
    iterlistvalues = lambda d, *args, **kwargs: d.iterlistvalues(*args, **kwargs)

    int_to_byte = chr
    iter_bytes = iter

    exec('def reraise(tp, value, tb=None):\n raise tp, value, tb')


    def fix_tuple_repr(obj):
        def __repr__(self):
            cls = self.__class__
            return '%s(%s)' % (cls.__name__, ', '.join(
                '%s=%r' % (field, self[index])
                for index, field in enumerate(cls._fields)
            ))

        obj.__repr__ = __repr__
        return obj


    def implements_iterator(cls):
        cls.next = cls.__next__
        del cls.__next__
        return cls


    def implements_to_string(cls):
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls


    def native_string_result(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs).encode('utf-8')

        return functools.update_wrapper(wrapper, func)


    def implements_bool(cls):
        cls.__nonzero__ = cls.__bool__
        del cls.__bool__
        return cls


    from itertools import izip

    range_type = xrange

    from StringIO import StringIO
    from cStringIO import StringIO as BytesIO

    NativeStringIO = BytesIO


    def make_literal_wrapper(reference):
        return _identity


    def normalize_string_tuple(tup):
        """Normalizes a string tuple to a common type. Following Python 2
        rules, upgrades to unicode are implicit.
        """
        if any(isinstance(x, text_type) for x in tup):
            return tuple(to_unicode(x) for x in tup)
        return tup


    def try_coerce_native(s):
        """Try to coerce a unicode string to native if possible. Otherwise,
        leave it as unicode.
        """
        try:
            return to_native(s)
        except UnicodeError:
            return s


    wsgi_get_bytes = _identity


    def wsgi_decoding_dance(s, charset='utf-8', errors='replace'):
        return s.decode(charset, errors)


    def wsgi_encoding_dance(s, charset='utf-8', errors='replace'):
        if isinstance(s, bytes):
            return s
        return s.encode(charset, errors)


    def to_bytes(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None:
            return None
        if isinstance(x, (bytes, bytearray, buffer)):
            return bytes(x)
        if isinstance(x, unicode):
            return x.encode(charset, errors)
        raise TypeError('Expected bytes')


    def to_native(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None or isinstance(x, str):
            return x
        return x.encode(charset, errors)

else:
    unichr = chr
    text_type = str
    string_types = (str,)
    integer_types = (int,)

    iterkeys = lambda d, *args, **kwargs: iter(d.keys(*args, **kwargs))
    itervalues = lambda d, *args, **kwargs: iter(d.values(*args, **kwargs))
    iteritems = lambda d, *args, **kwargs: iter(d.items(*args, **kwargs))

    iterlists = lambda d, *args, **kwargs: iter(d.lists(*args, **kwargs))
    iterlistvalues = lambda d, *args, **kwargs: iter(d.listvalues(*args, **kwargs))

    int_to_byte = operator.methodcaller('to_bytes', 1, 'big')
    iter_bytes = functools.partial(map, int_to_byte)


    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value


    fix_tuple_repr = _identity
    implements_iterator = _identity
    implements_to_string = _identity
    implements_bool = _identity
    native_string_result = _identity
    imap = map
    izip = zip
    ifilter = filter
    range_type = range

    from io import StringIO, BytesIO

    NativeStringIO = StringIO

    _latin1_encode = operator.methodcaller('encode', 'latin1')


    def make_literal_wrapper(reference):
        if isinstance(reference, text_type):
            return _identity
        return _latin1_encode


    def normalize_string_tuple(tup):
        """Ensures that all types in the tuple are either strings
        or bytes.
        """
        tupiter = iter(tup)
        is_text = isinstance(next(tupiter, None), text_type)
        for arg in tupiter:
            if isinstance(arg, text_type) != is_text:
                raise TypeError('Cannot mix str and bytes arguments (got %s)'
                                % repr(tup))
        return tup


    try_coerce_native = _identity
    wsgi_get_bytes = _latin1_encode


    def wsgi_decoding_dance(s, charset='utf-8', errors='replace'):
        return s.encode('latin1').decode(charset, errors)


    def wsgi_encoding_dance(s, charset='utf-8', errors='replace'):
        if isinstance(s, text_type):
            s = s.encode(charset)
        return s.decode('latin1', errors)


    def to_bytes(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None:
            return None
        if isinstance(x, (bytes, bytearray, memoryview)):  # noqa
            return bytes(x)
        if isinstance(x, str):
            return x.encode(charset, errors)
        raise TypeError('Expected bytes')


    def to_native(x, charset=sys.getdefaultencoding(), errors='strict'):
        if x is None or isinstance(x, str):
            return x
        return x.decode(charset, errors)


def to_unicode(x, charset=sys.getdefaultencoding(), errors='strict',
               allow_none_charset=False):
    if x is None:
        return None
    if not isinstance(x, bytes):
        return text_type(x)
    if charset is None and allow_none_charset:
        return x
    return x.decode(charset, errors)


import codecs
import hashlib
import hmac
import os
from itertools import starmap
from operator import xor
from random import SystemRandom
from struct import Struct

SALT_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
DEFAULT_PBKDF2_ITERATIONS = 50000

_pack_int = Struct('>I').pack
_builtin_safe_str_cmp = getattr(hmac, 'compare_digest', None)
_sys_rng = SystemRandom()
_os_alt_seps = list(sep for sep in [os.path.sep, os.path.altsep]
                    if sep not in (None, '/'))


def _find_hashlib_algorithms():
    algos = getattr(hashlib, 'algorithms', None)
    if algos is None:
        algos = ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')
    rv = {}
    for algo in algos:
        func = getattr(hashlib, algo, None)
        if func is not None:
            rv[algo] = func
    return rv


_hash_funcs = _find_hashlib_algorithms()


def pbkdf2_hex(data, salt, iterations=DEFAULT_PBKDF2_ITERATIONS,
               keylen=None, hashfunc=None):
    """Like :func:`pbkdf2_bin`, but returns a hex-encoded string.
    .. versionadded:: 0.9
    :param data: the data to derive.
    :param salt: the salt for the derivation.
    :param iterations: the number of iterations.
    :param keylen: the length of the resulting key.  If not provided,
                   the digest size will be used.
    :param hashfunc: the hash function to use.  This can either be the
                     string name of a known hash function, or a function
                     from the hashlib module.  Defaults to sha256.
    """
    rv = pbkdf2_bin(data, salt, iterations, keylen, hashfunc)
    return to_native(codecs.encode(rv, 'hex_codec'))


_has_native_pbkdf2 = hasattr(hashlib, 'pbkdf2_hmac')


def pbkdf2_bin(data, salt, iterations=DEFAULT_PBKDF2_ITERATIONS,
               keylen=None, hashfunc=None):
    """Returns a binary digest for the PBKDF2 hash algorithm of `data`
    with the given `salt`. It iterates `iterations` times and produces a
    key of `keylen` bytes. By default, SHA-256 is used as hash function;
    a different hashlib `hashfunc` can be provided.
    .. versionadded:: 0.9
    :param data: the data to derive.
    :param salt: the salt for the derivation.
    :param iterations: the number of iterations.
    :param keylen: the length of the resulting key.  If not provided
                   the digest size will be used.
    :param hashfunc: the hash function to use.  This can either be the
                     string name of a known hash function or a function
                     from the hashlib module.  Defaults to sha256.
    """
    if isinstance(hashfunc, string_types):
        hashfunc = _hash_funcs[hashfunc]
    elif not hashfunc:
        hashfunc = hashlib.sha256
    data = to_bytes(data)
    salt = to_bytes(salt)

    # If we're on Python with pbkdf2_hmac we can try to use it for
    # compatible digests.
    if _has_native_pbkdf2:
        _test_hash = hashfunc()
        if hasattr(_test_hash, 'name') and \
                        _test_hash.name in _hash_funcs:
            return hashlib.pbkdf2_hmac(_test_hash.name,
                                       data, salt, iterations,
                                       keylen)

    mac = hmac.HMAC(data, None, hashfunc)
    if not keylen:
        keylen = mac.digest_size

    def _pseudorandom(x, mac=mac):
        h = mac.copy()
        h.update(x)
        return bytearray(h.digest())

    buf = bytearray()
    for block in range_type(1, -(-keylen // mac.digest_size) + 1):
        rv = u = _pseudorandom(salt + _pack_int(block))
        for i in range_type(iterations - 1):
            u = _pseudorandom(bytes(u))
            rv = bytearray(starmap(xor, izip(rv, u)))
        buf.extend(rv)
    return bytes(buf[:keylen])


def safe_str_cmp(a, b):
    """This function compares strings in somewhat constant time.  This
    requires that the length of at least one string is known in advance.
    Returns `True` if the two strings are equal, or `False` if they are not.
    .. versionadded:: 0.7
    """
    if isinstance(a, text_type):
        a = a.encode('utf-8')
    if isinstance(b, text_type):
        b = b.encode('utf-8')

    if _builtin_safe_str_cmp is not None:
        return _builtin_safe_str_cmp(a, b)

    if len(a) != len(b):
        return False

    rv = 0
    if PY2:
        for x, y in izip(a, b):
            rv |= ord(x) ^ ord(y)
    else:
        for x, y in izip(a, b):
            rv |= x ^ y

    return rv == 0


def gen_salt(length):
    """Generate a random string of SALT_CHARS with specified ``length``."""
    if length <= 0:
        raise ValueError('Salt length must be positive')
    return ''.join(_sys_rng.choice(SALT_CHARS) for _ in range_type(length))


def _hash_internal(method, salt, password):
    """Internal password hash helper.  Supports plaintext without salt,
    unsalted and salted passwords.  In case salted passwords are used
    hmac is used.
    """
    if method == 'plain':
        return password, method

    if isinstance(password, text_type):
        password = password.encode('utf-8')

    if method.startswith('pbkdf2:'):
        args = method[7:].split(':')
        if len(args) not in (1, 2):
            raise ValueError('Invalid number of arguments for PBKDF2')
        method = args.pop(0)
        iterations = args and int(args[0] or 0) or DEFAULT_PBKDF2_ITERATIONS
        is_pbkdf2 = True
        actual_method = 'pbkdf2:%s:%d' % (method, iterations)
    else:
        is_pbkdf2 = False
        actual_method = method

    hash_func = _hash_funcs.get(method)
    if hash_func is None:
        raise TypeError('invalid method %r' % method)

    if is_pbkdf2:
        if not salt:
            raise ValueError('Salt is required for PBKDF2')
        rv = pbkdf2_hex(password, salt, iterations,
                        hashfunc=hash_func)
    elif salt:
        if isinstance(salt, text_type):
            salt = salt.encode('utf-8')
        rv = hmac.HMAC(salt, password, hash_func).hexdigest()
    else:
        h = hash_func()
        h.update(password)
        rv = h.hexdigest()
    return rv, actual_method


def generate_password_hash(password, method='pbkdf2:sha256', salt_length=8):
    """Hash a password with the given method and salt with a string of
    the given length. The format of the string returned includes the method
    that was used so that :func:`check_password_hash` can check the hash.
    The format for the hashed string looks like this::
        method$salt$hash
    This method can **not** generate unsalted passwords but it is possible
    to set param method='plain' in order to enforce plaintext passwords.
    If a salt is used, hmac is used internally to salt the password.
    If PBKDF2 is wanted it can be enabled by setting the method to
    ``pbkdf2:method:iterations`` where iterations is optional::
        pbkdf2:sha256:80000$salt$hash
        pbkdf2:sha256$salt$hash
    :param password: the password to hash.
    :param method: the hash method to use (one that hashlib supports). Can
                   optionally be in the format ``pbkdf2:<method>[:iterations]``
                   to enable PBKDF2.
    :param salt_length: the length of the salt in letters.
    """
    salt = method != 'plain' and gen_salt(salt_length) or ''
    h, actual_method = _hash_internal(method, salt, password)
    return '%s$%s$%s' % (actual_method, salt, h)


def check_password_hash(pwhash, password):
    """check a password against a given salted and hashed password value.
    In order to support unsalted legacy passwords this method supports
    plain text passwords, md5 and sha1 hashes (both salted and unsalted).
    Returns `True` if the password matched, `False` otherwise.
    :param pwhash: a hashed string like returned by
                   :func:`generate_password_hash`.
    :param password: the plaintext password to compare against the hash.
    """
    if pwhash.count('$') < 2:
        return False
    method, salt, hashval = pwhash.split('$', 2)
    return safe_str_cmp(_hash_internal(method, salt, password)[0], hashval)
