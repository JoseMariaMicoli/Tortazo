"""
spider_man.py

Copyright 2006 Andres Riancho

This file is part of w3af, http://w3af.org/ .

w3af is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

w3af is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with w3af; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""

import w3af.core.controllers.output_manager as om
import w3af.core.data.url.HTTPResponse as HTTPResponse
import w3af.core.data.constants.ports as ports

from w3af.core.controllers.plugins.crawl_plugin import CrawlPlugin
from w3af.core.controllers.daemons.proxy import Proxy, w3afProxyHandler
from w3af.core.controllers.exceptions import RunOnce, ProxyException
from w3af.core.controllers.misc.decorators import runonce

from w3af.core.data.options.opt_factory import opt_factory
from w3af.core.data.options.option_list import OptionList
from w3af.core.data.parsers.url import URL
from w3af.core.data.dc.headers import Headers

# Cohny changed the original http://w3af/spider_man?terminate
# to http://127.7.7.7/spider_man?terminate because in Opera we got
# an error if we used the original one! Thanks Cohny!
TERMINATE_URL = URL('http://127.7.7.7/spider_man?terminate')


class spider_man(CrawlPlugin):
    """
    SpiderMan is a local proxy that will collect new URLs.

    :author: Andres Riancho (andres.riancho@gmail.com)
    :author: Alexander Berezhnoy < alexander.berezhnoy |at| gmail.com >
    """
    def __init__(self):
        CrawlPlugin.__init__(self)
        self._first_captured_request = True

        # User configured parameters
        self._listen_address = '127.0.0.1'
        self._listen_port = ports.SPIDERMAN

    @runonce(exc_class=RunOnce)
    def crawl(self, freq):
        
        # Create the proxy server
        try:
            self._proxy = Proxy(self._listen_address, self._listen_port,
                                self._uri_opener, self.create_p_h())
        except ProxyException, proxy_exc:
            om.out.error('%s' % proxy_exc)
        
        else:
            self._proxy.target_domain = freq.get_url().get_domain()
            
            msg = ('spider_man proxy is running on %s:%s.\nPlease configure '
                   'your browser to use these proxy settings and navigate the '
                   'target site.\nTo exit spider_man plugin please navigate to %s .'
                   % (self._listen_address, self._listen_port, TERMINATE_URL))
            om.out.information(msg)
            
            self._proxy.run()

    def append_fuzzable_request(self, freq):
        """
        Get a fuzzable request. Save it. Log it.

        This method is called from the proxyHandler.

        :return: None.
        """
        self.output_queue.put(freq)

        if self._first_captured_request:
            self._first_captured_request = False
            om.out.information('Requests captured with spider_man plugin:')

        om.out.information(str(freq))

    def ext_fuzzable_requests(self, response):
        for fr in self._create_fuzzable_requests(response):
            self.output_queue.put(fr)

    def stop_proxy(self):
        self._proxy.stop()

    def create_p_h(self):
        """
        This method returns closure which is dressed up as a proxyHandler.
        It's a trick to get rid of global variables.
        :return: proxyHandler constructor
        """
        def constructor(request, client_addr, server):
            return ProxyHandler(request, client_addr, server, self)

        return constructor

    def get_options(self):
        """
        :return: A list of option objects for this plugin.
        """
        ol = OptionList()

        d = 'IP address that the spider_man proxy will use to receive requests'
        o = opt_factory('listen_address', self._listen_address, d, 'string')
        ol.add(o)

        d = 'Port that the spider_man HTTP proxy server will use to receive requests'
        o = opt_factory('listen_port', self._listen_port, d, 'integer')
        ol.add(o)

        return ol

    def set_options(self, options_list):
        """
        This method sets all the options that are configured using the user interface
        generated by the framework using the result of get_options().

        :param OptionList: A dictionary with the options for the plugin.
        :return: No value is returned.
        """

        self._listen_address = options_list['listen_address'].get_value()
        self._listen_port = options_list['listen_port'].get_value()

    def get_long_desc(self):
        """
        :return: A DETAILED description of the plugin functions and features.
        """
        return """
        This plugin is a local proxy that can be used to give the framework
        knowledge about the web application when it has a lot of client side
        code like Flash or Java applets. Whenever a w3af needs to test an
        application with flash or javascript, the user should enable this plugin
        and use a web browser to navigate the site using spider_man proxy.

        The proxy will extract information from the user navigation and generate
        the necesary injection points for the audit plugins.

        Another feature of this plugin is to save the cookies that are sent by
        the web application, in order to be able to use them in other plugins.
        So if you have a web application that has a login with cookie session
        management you should enable this plugin, do the login through the browser
        and then let the other plugins spider the rest of the application for
        you. Important note: If you enable web_spider, you should ignore the "logout"
        link.

        Two configurable parameters exist:
            - listen_address
            - listen_port
        """


global_first_request = True


class ProxyHandler(w3afProxyHandler):

    def __init__(self, request, client_address, server, spider_man=None):
        self._version = 'spider_man-w3af/1.1'
        if spider_man is None:
            if hasattr(server, 'chainedHandler'):
                # see core.controllers.daemons.proxy.HTTPServerWrapper
                self._spider_man = server.chainedHandler._spider_man
        else:
            self._spider_man = spider_man
        self._uri_opener = self._spider_man._uri_opener
        w3afProxyHandler.__init__(self, request, client_address, server)

    def do_ALL(self):
        global global_first_request
        if global_first_request:
            global_first_request = False
            om.out.information(
                'The user is navigating through the spider_man proxy.')

        # Convert to url_object
        path = URL(self.path)

        if path == TERMINATE_URL:
            om.out.information('The user terminated the spider_man session.')
            self._send_end()
            self._spider_man.stop_proxy()
            return

        om.out.debug("[spider_man] Handling request: %s %s" %
                    (self.command, path))
        #   Send this information to the plugin so it can send it to the core
        freq = self._create_fuzzable_request()
        self._spider_man.append_fuzzable_request(freq)

        grep = True
        if path.get_domain() != self.server.w3afLayer.target_domain:
            grep = False

        try:
            response = self._send_to_server(grep=grep)
        except Exception, e:
            self._send_error(e)
        else:
            if response.is_text_or_html():
                self._spider_man.ext_fuzzable_requests(response)

            headers = response.get_headers()
            cookie_value, cookie_header = headers.iget('cookie', None)
            if cookie_value is not None:
                msg = 'The remote web application sent the following' \
                      ' cookie: "%s".\nw3af will use it during the rest ' \
                      'of the process in order to maintain the session.' 
                om.out.information(msg % cookie_value)
            self._send_to_browser(response)
        
    do_GET = do_POST = do_HEAD = do_ALL

    def _send_end(self):
        """
        Sends an HTML indicating that w3af spider_man plugin has finished its execution.
        """
        html = '<html>spider_man plugin finished its execution.</html>'
        html_len = str(len(html))
        headers = Headers([('Content-Length', html_len)])

        resp = HTTPResponse.HTTPResponse(200, html, headers,
                                         TERMINATE_URL, TERMINATE_URL,)
        self._send_to_browser(resp)
