import unittest
import sys

# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
# import datetime

from pastasauce import PastaSauce, PastaDecorator
from . import StaxHelper

NOT_STARTED = True
if NOT_STARTED:
    import pytest

browsers = [{
    "platform": "Windows 10",
    "browserName": "internet explorer",
    "version": "11"
}, {
    "platform": "OS X 10.11",
    "browserName": "safari",
    "version": "8.1"
}, {
    "platform": "Windows 7",
    "browserName": "internet explorer",
    "version": "11.0",
    "screenResolution": "1440x900"
}, {
    "platform": "Windows 7",
    "browserName": "chrome",
    "version": "44.0",
    "screenResolution": "1440x900"
}, {
    "platform": "Windows 7",
    "browserName": "firefox",
    "version": "40.0",
    "screenResolution": "1440x900"
}, {
    "platform": "OS X 10.9",
    "browserName": "iPhone",
    "version": "7.1",
    "deviceName": "iPad Retina (64-bit)",
    "deviceOrientation": "portrait"
}]
# use 1 browser setup
browsers = [browsers[4]]
standard_window = (1440, 800)
compressed_window = (700, 500)

published_assignments = {
    'basic_reading': {},
    'basic_homework': {},
    'basic_external': {},
    'basic_review': {},
    'basic_event': {},
    'multi-period_reading': {},
    'multi-period_homework': {},
    'multi-period_external': {},
    'mutli-period_review': {},
    'multi-period_event': {},
    'multi-section_reading': {},
    'multi-section_homework': {},
    'multi-section_review': {}
}

draft_assignments = {
    'basic_reading': {},
    'basic_homework': {},
    'basic_external': {},
    'basic_review': {},
    'basic_event': {}
}

delete_assignments = {
    'basic_reading': {},
    'basic_homework': {},
    'basic_external': {},
    'basic_review': {},
    'basic_event': {}
}


@PastaDecorator.on_platforms(browsers)
class TestTutorAssignments(unittest.TestCase):
    ''''''
    def setUp(self):
        self.ps = PastaSauce()
        self.helper = StaxHelper()
        self.desired_capabilities['name'] = self.id()
        teacher = self.helper.user.name
        teacher_password = self.helper.user.password
        self.driver = StaxHelper.run_on(
            StaxHelper.LOCAL, self.ps, self.desired_capabilities
        )
        self.driver.implicitly_wait(15)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.set_window_size(*standard_window)
        self.helper.user.login(self.driver, teacher, teacher_password,
                               self.helper.user.url)
        self.helper.user.select_course(self.driver, category='Physics')

    def tearDown(self):
        ''''''
        self.driver.quit()
        status = (sys.exc_info() == (None, None, None))
        self.ps.update_job(self.driver.session_id, passed=status)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_assignment_basic_homework(self):
        ''''''
