from __future__ import unicode_literals

import threading
from django.test.simple import DjangoTestSuiteRunner
from django.core.servers.basehttp import run, get_internal_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
from splinter.driver.webdriver.firefox import WebDriver
from mock import patch


BROWSER = None


class TestSuiteRunner(DjangoTestSuiteRunner):
    def setup_test_environment(self, **kwargs):
        super(TestSuiteRunner, self).setup_test_environment(**kwargs)
        handler = get_internal_wsgi_application()
        handler = StaticFilesHandler(handler)

        def start_server():
            with patch('django.core.servers.basehttp.WSGIRequestHandler.log_message'):
                run('0.0.0.0', 65432, handler, ipv6=False, threading=False)
        thread = threading.Thread(target=start_server)
        thread.daemon = True
        thread.start()

        global BROWSER
        BROWSER = SingleVisitFirefoxDriver()

    def teardown_test_environment(self, **kwargs):
        BROWSER.quit()
        super(TestSuiteRunner, self).setup_test_environment(**kwargs)


class SingleVisitFirefoxDriver(WebDriver):
    def visit(self, url):
        self.driver.get(url)
