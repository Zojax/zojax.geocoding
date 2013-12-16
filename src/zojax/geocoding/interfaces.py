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
""" geocoding interfaces

$Id$
"""

from zope import schema, interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.geocoding')


class IGeocodingConfiglet(interface.Interface):
    """ configlet interface """

    cache = interface.Attribute('Cached coordinates')

    #enabled = schema.Bool(
    #    title = _(u'Enabled'),
    #    description = _(u'Enable geocoding service.'),
    #    default = False,
    #    required = False)

    maxEntries = schema.Int(
        title = u'Maximum cached entries',
        default = 3000,
        required = True)

    maxAge = schema.Int(
        title = u'Maximum age of cached entries (seconds)',
        default = 604800,
        required = True)

    cleanupInterval = schema.Int(
        title = u'Time between cache cleanups (seconds)',
        default = 300,
        required = True)

    def query(id, key, default=None):
        """ return cached value """

    def set(data, id, key):
        """ set cache data """
