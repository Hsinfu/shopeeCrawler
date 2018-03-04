# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import uuid
import hashlib
import logging

logger = logging.getLogger(__name__)


def shopee_hash(s):
    # getHashedString: function(e) {
    #    return CryptoJS.SHA256(CryptoJS.MD5(e).toString()).toString()
    # }
    md5_hash = hashlib.md5(s.encode('ascii')).hexdigest()
    sha256_hash = hashlib.sha256(md5_hash.encode('ascii')).hexdigest()
    return sha256_hash


def shopee_uuid(hex_uuid=False):
    o = uuid.uuid4()
    return o.hex if hex_uuid else o.__str__()
