# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import json
import logging

logger = logging.getLogger(__name__)


class JsonFile(object):
    def __init__(self, json_file):
        self.json_file = json_file

    def load(self):
        try:
            with open(self.json_file, 'r') as json_fptr:
                return json.load(json_fptr)
        except Exception:
            logger.error('load json from file failed', exc_info=True)
        return {}

    def save(self, obj):
        try:
            with open(self.json_file, 'w') as json_fptr:
                json.dump(obj, json_fptr)
            return True
        except Exception:
            logger.error('dump obj: %s to json file failed', obj, exc_info=True)
        return False
