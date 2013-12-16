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
import time
import urllib
import simplejson as json


class UnknownGeocodeError(Exception):
    """Unknown geocode"""


def geocode(address):

    # address should be a string or unicode
    if not isinstance(address, (str, unicode)):
        raise TypeError("Invalid address type", type(address))

    mapsUrl = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    # This joins the parts of the URL together into one string.
    # https://developers.google.com/maps/documentation/geocoding/
    url = ''.join([mapsUrl, urllib.quote(address.strip()),
                   '&sensor=false&language=en'])
    # This retrieves the URL from Google, parses out the longitude and
    # latitude, and then returns them as a string.
    response = json.loads(urllib.urlopen(url).read())

    # workaround for QUERY_LIMIT
    if response['status'] == "OVER_QUERY_LIMIT":
        time.sleep(2)
        response = json.loads(urllib.urlopen(url).read())

    if response['status'] != 'OK':
        raise UnknownGeocodeError(response)

    coordinates = response['results'][0]['geometry']['location']
    return '%s,%s' % (coordinates['lat'],coordinates['lng'])