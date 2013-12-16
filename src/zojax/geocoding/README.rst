=============
Browser tests
=============

    >>> from z3c.jsonrpc.testing import JSONRPCTestProxy
    >>> from zope.component import getUtility
    >>> from zope.testbrowser.testing import Browser
    >>> from zope.app.component.hooks import setSite

    >>> from zojax.geocoding.interfaces import IGeocodingConfiglet


declare default variables
-------------------------

    >>> siteURL = 'http://localhost'
    >>> geocodingConfiglet = getUtility(IGeocodingConfiglet)
    >>> markers = getUtility(IGeocodingConfiglet).cache

    >>> root = getRootFolder()
    >>> setSite(root)


JSONRPC
-------

check if cache is empty

    >>> markers.getStatistics()
    ()


set default settings for the request

    >>> siteURL = 'http://localhost/++skin++JSONRPC.geocoding'
    >>> b = Browser()
    >>> b.handleErrors = False

get coordinates for real address

    >>> code = 'TEST01'
    >>> geo = "4600 A GOODFELLOW BLVD, ST LOUIS, MO, UNITED STATES"
    >>> b.post(
    ...     siteURL,
    ...     "{'method':'convertAddress', 'params': {'code': '"+code+"', 'address': '"+geo+"'}}",
    ...     content_type='application/json')
    >>> b.contents
    '{"jsonrpc":"2.0","result":"38.6950519,-90.264156","id":"jsonrpc"}'

check if cache is not empty (it should contain one object)

    >>> markers.getStatistics()[0]['entries']
    1

if the address is not correct, get "0,0"

    >>> code = 'TEST02'
    >>> geo = "TAKOGO ADRESA NET"
    >>> b.post(
    ...     siteURL,
    ...     "{'method':'convertAddress', 'params': {'code': '"+code+"', 'address': '"+geo+"'}}",
    ...     content_type='application/json')
    >>> b.contents
    '{"jsonrpc":"2.0","result":"0,0","id":"jsonrpc"}'

check if cache is not empty (it should contain 2 objects)

    >>> markers.getStatistics()[0]['entries']
    2

if the address is not correct, add additional parameter country and get country coordinates

    >>> code = 'TEST03'
    >>> geo = "TAKOGO ADRESA NET"
    >>> country = "RUSSIA"
    >>> b.post(
    ...     siteURL,
    ...     "{'method':'convertAddress', 'params': {'code': '"+code+"', 'address': '"+geo+"', 'country': '"+country+"'}}",
    ...     content_type='application/json')
    >>> b.contents
    '{"jsonrpc":"2.0","result":"61.52401,105.318756","id":"jsonrpc"}'

check if cache is not empty (it should contain 3 objects)

    >>> markers.getStatistics()[0]['entries']
    3

check if there are extra spaces in the beginning / in the end

    >>> code = 'TEST04'
    >>> geo = "          4600 A GOODFELLOW BLVD, ST LOUIS, MO, UNITED STATES          "
    >>> b.post(
    ...     siteURL,
    ...     "{'method':'convertAddress', 'params': {'code': '"+code+"', 'address': '"+geo+"'}}",
    ...     content_type='application/json')
    >>> b.contents
    '{"jsonrpc":"2.0","result":"38.6950519,-90.264156","id":"jsonrpc"}'


check if cache is not empty (it should contain 4 objects)

    >>> markers.getStatistics()[0]['entries']
    4


check for errors
----------------

pass numbers instead address

    >>> code = 'TEST05'
    >>> b.post(
    ...     siteURL,
    ...     "{'method':'convertAddress', 'params': {'code': '"+code+"', 'address': 12345}}",
    ...     content_type='application/json')
    >>> b.contents
    '{"jsonrpc":"2.0","result":"0,0","id":"jsonrpc"}'

pass empty parameters

    >>> b.post(
    ...     siteURL,
    ...     "{'method':'convertAddress', 'params': {}}",
    ...     content_type='application/json')
    >>> b.contents
    '{"jsonrpc":"2.0","result":"ERROR: code and address can not be empty","id":"jsonrpc"}'

check requests limit

    >>> geo = "4600 A GOODFELLOW BLVD, ST LOUIS, MO, UNITED STATES" # doctest: +SKIP
    >>> for i in range(0,20): # doctest: +SKIP
    ...    b.post(siteURL, "{'method':'convertAddress', 'params': {'code': 'LIMIT0"+str(i)+"', 'address': '"+geo+"'}}", content_type='application/json') # doctest: +SKIP

    >>> markers.getStatistics()[0]['entries'] # doctest: +SKIP
    25


Configlet
---------

unauthorized access

    >>> actor = Browser()
    >>> actor.handleErrors = False
    >>> actor.open("http://localhost/settings/geocoding/")
    Traceback (most recent call last):
    ...
    Unauthorized: settings

let's login

    >>> admin = Browser()
    >>> admin.handleErrors = False
    >>> admin.addHeader("Authorization", "Basic mgr:mgrpw")

check default settings set in the first tab

    >>> admin.open('http://localhost/settings/system/geocoding/')
    >>> print admin.contents
    <html>
    ...
      <label for="configlet-widgets-maxEntries" title="">Maximum cached entries</label>
      <span class="z-form-fieldRequired">&nbsp;</span>
    ...
        <input id="configlet-widgets-maxEntries"
               name="configlet.widgets.maxEntries"
               class="text-widget required int-field"
               value="3,000" type="text" />
    ...
      <label for="configlet-widgets-maxAge" title="">Maximum age of cached entries (seconds)</label>
      <span class="z-form-fieldRequired">&nbsp;</span>
    ...
        <input id="configlet-widgets-maxAge"
               name="configlet.widgets.maxAge"
               class="text-widget required int-field"
               value="604,800" type="text" />
    ...
      <label for="configlet-widgets-cleanupInterval" title="">Time between cache cleanups (seconds)</label>
      <span class="z-form-fieldRequired">&nbsp;</span>
    ...
        <input id="configlet-widgets-cleanupInterval"
               name="configlet.widgets.cleanupInterval"
               class="text-widget required int-field"
               value="300" type="text" />
    ...
    </html>

switch to the second tab

    >>> admin.open('http://localhost/settings/system/geocoding/index.html/stats')
    >>> print admin.contents
    <html>
    ...
      <h2>Cache Statistics</h2>
    ...
          <th>Hits</th>
          <td>0</td>
    ...
          <th>Misses</th>
          <td>5</td>
    ...
          <th>Size</th>
          <td>0.36Kb</td>
    ...
          <th>Entries</th>
          <td>5</td>
    ...
        <h2>Items in Cache</h2>
    ...
      <th></th>
      <th>Code</th>
      <th>Value</th>
    ...
        <td><input type="checkbox" name="code:list" value="TEST01" /></td>
        <td>TEST01</td>
        <td>38.6950519,-90.264156</td>
    ...
        <td><input type="checkbox" name="code:list" value="TEST02" /></td>
        <td>TEST02</td>
        <td>0,0</td>
    ...
        <td><input type="checkbox" name="code:list" value="TEST03" /></td>
        <td>TEST03</td>
        <td>61.52401,105.318756</td>
    ...
        <td><input type="checkbox" name="code:list" value="TEST04" /></td>
        <td>TEST04</td>
        <td>38.6950519,-90.264156</td>
    ...
        <td><input type="checkbox" name="code:list" value="TEST05" /></td>
        <td>TEST05</td>
        <td>0,0</td>
    ...
          <input type="submit" class="z-form-removebutton" style="width: auto" value="Invalidate selected" name="markers.invalidate" />
          <input type="submit" class="z-form-removebutton" style="width: auto" value="Invalidate all" name="markers.invalidateall" />
    ...
    </html>


add one object to the cache and check the statistic again

    >>> code = 'TEST06'
    >>> geo = "4600 A GOODFELLOW BLVD, ST LOUIS, MO, UNITED STATES"
    >>> b.post(
    ...     siteURL,
    ...     "{'method':'convertAddress', 'params': {'code': '"+code+"', 'address': '"+geo+"'}}",
    ...     content_type='application/json')
    >>> b.contents
    '{"jsonrpc":"2.0","result":"38.6950519,-90.264156","id":"jsonrpc"}'

    >>> admin.open('http://localhost/settings/system/geocoding/index.html/stats')
    >>> print admin.contents
    <html>
    ...
          <th>Hits</th>
          <td>0</td>
    ...
          <th>Entries</th>
          <td>6</td>
    ...
        <td><input type="checkbox" name="code:list" value="TEST06" /></td>
        <td>TEST06</td>
        <td>38.6950519,-90.264156</td>
    ...
    </html>

try to add this one object to the cache and check the statistic again

    >>> code = 'TEST06'
    >>> geo = "4600 A GOODFELLOW BLVD, ST LOUIS, MO, UNITED STATES"
    >>> b.post(
    ...     siteURL,
    ...     "{'method':'convertAddress', 'params': {'code': '"+code+"', 'address': '"+geo+"'}}",
    ...     content_type='application/json')
    >>> b.contents
    '{"jsonrpc":"2.0","result":"38.6950519,-90.264156","id":"jsonrpc"}'

    >>> admin.open('http://localhost/settings/system/geocoding/index.html/stats')
    >>> print admin.contents
    <html>
    ...
          <th>Hits</th>
          <td>1</td>
    ...
          <th>Entries</th>
          <td>6</td>
    ...
    </html>

checking invalidate selected button

    >>> admin.open('http://localhost/settings/system/geocoding/index.html/stats')
    >>> admin.getControl(name="code:list", index=0).value=['TEST02']
    >>> admin.getControl(name="markers.invalidate").click()
    >>> print admin.contents
    <html>
    ...
    ...<div class="statusMessage">Cache data has been invalidated.</div>
    ...
          <th>Entries</th>
          <td>5</td>
    ...
    </html>

checking deleteing all the elements from the tab

    >>> admin.open('http://localhost/settings/system/geocoding/index.html/stats')
    >>> admin.getControl(name="markers.invalidateall").click()

cache should be empty (display notification that there's nothing in cache)
    >>> print admin.contents
    <html>
    ...
    ...<div class="statusMessage">Cache data has been invalidated.</div>
    ...
        There are no any statistics.
    ...
    </html>



    >>> setSite(None)