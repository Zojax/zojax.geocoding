##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface

from zope.app.cache.ram import RAMCache
from interfaces import IGeocodingConfiglet


class GeocodingConfiglet(object):
    interface.implements(IGeocodingConfiglet)

    @property
    def cache(self):
        cache = self.data.get('ramcache')
        if cache is None:
            cache = RAMCache()
            self.data['ramcache'] = cache

        return cache

    def query(self, id, key, default=None):
        if not self.enabled:
            return default
        return self.cache.query(id, key, default)

    def set(self, data, id, key):
        if self.enabled:
            self.cache.set(data, id, key)

