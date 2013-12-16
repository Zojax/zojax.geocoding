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

import logging

from z3c.jsonrpc import publisher

from zope.component import getUtility

from ..interfaces import IGeocodingConfiglet
from ..utils import geocode


logger = logging.getLogger("zojax.geocoding")


class Geocoding(publisher.MethodPublisher):

    def convertAddress(self, code='', address='', country=''):

        if not code or not address:
            return "ERROR: code and address can not be empty"

        markers = getUtility(IGeocodingConfiglet).cache
        # NOTE: check if code already in cache
        coords = markers.query('items', {'code': code})
        if coords:
            return coords

        try:
            gcoords = geocode(address)
        except:
            gcoords = '0,0'

        # NOTE: get coords of the country instead coords of the address
        if gcoords == '0,0' and country:
            gcoords = geocode(country)

        # NOTE: add code and coords to the cache's array
        markers.set(gcoords, 'items', {'code': code})

        return gcoords
