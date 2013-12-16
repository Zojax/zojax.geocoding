##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
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
from zope.proxy import removeAllProxies

from zojax.batching.batch import Batch
from zojax.layoutform import Fields
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.wizard.interfaces import ISaveable
from zojax.wizard import WizardStepForm

from ..interfaces import _, IGeocodingConfiglet


class GeocodingEdit(WizardStepForm):
    interface.implements(ISaveable)

    name = 'configlet'
    title = _('Configlet')
    label = _('Configure configlet')

    fields = Fields(IGeocodingConfiglet)

    def render(self):
        return super(GeocodingEdit, self).render()

    def getContent(self):
        cache = removeAllProxies(self.context.cache)
        return {'maxEntries': cache.maxEntries,
                'maxAge': cache.maxAge,
                'cleanupInterval': cache.cleanupInterval}

    def applyChanges(self, data):
        self.context.cache.update(**data)
        return True


class GeocodingStatsView(WizardStepForm):

    name = 'stats'
    title = _(u'Statistics')
    label = _(u' ')

    def update(self):
        super(GeocodingStatsView, self).update()

        request, context = self.request, self.context
        cache = removeAllProxies(context.cache)

        if 'markers.invalidate' in request:
            changed = False
            for oid in request.get('code', ()):
                cache.invalidate('items', {'code': oid})
                changed = True

            if changed:
                IStatusMessage(request).add(
                    u'Cache data has been invalidated.')

        if 'markers.invalidateall' in request:
            cache.invalidateAll()
            IStatusMessage(request).add(
                    u'Cache data has been invalidated.')

        self.stats = cache.getStatistics()

        size = 0
        for rec in self.stats:
            size += rec['size']

        if size < 262144:
            self.size = '%0.2fKb'%(size/1024.0)
        else:
            self.size = '%0.2fMb'%(size/1048576.0)

        try:
            # NOTE: get items from cache
            items = cache._getStorage()._data['items'].items()
        except KeyError:
            items = []

        self.batch = Batch(items, size=20, context=context, request=request)
