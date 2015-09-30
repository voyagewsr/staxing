import unittest
import pytest
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from pastasauce import PastaSauce, PastaDecorator


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
browsers = [browsers[2]]
standard_window = (1024, 768)
compressed_window = (700, 500)
# skip control
COMPLETE = True
IN_PROGRESS = False
INCOMPLETE = True


@PastaDecorator.on_platforms(browsers)
class TestTutorAcctMgt(unittest.TestCase):
    ''''''
    def setUp(self):
        ''''''
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        self.driver = webdriver.Remote(
            command_executor='http://%s:%s@ondemand.saucelabs.com:80/wd/hub' %
            (self.ps.get_user(), self.ps.get_access_key()),
            desired_capabilities=self.desired_capabilities)
        self.driver.implicitly_wait(10)

    @pytest.mark.skipif(COMPLETE, reason='Complete')
    def test_user_login_standard(self):
        self.driver.set_window_size(*standard_window)
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*standard_window))
        self.driver.get('https://tutor-qa.openstax.org/')
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        login = self.driver.find_element_by_link_text('Login')
        login.click()
        username = self.driver.find_element_by_id('auth_key')
        username.send_keys('admin')
        password = self.driver.find_element_by_id('password')
        password.send_keys('password')
        sign_in = self.driver.find_element_by_xpath('//button[text()=' +
                                                    '"Sign in"]')
        sign_in.click()
        wait = WebDriverWait(self.driver, 15)
        user_menu = wait.until(
            expect.presence_of_element_located((By.CLASS_NAME,
                                               'dropdown-toggle'))
        )
        user_menu.click()
        assert('Log Out' in
               self.driver.find_element(By.CLASS_NAME, 'logout').text)

    @pytest.mark.skipif(COMPLETE, reason='Complete')
    def test_user_login_compact(self):
        self.driver.set_window_size(*compressed_window)
        size = self.driver.get_window_size()
        assert(compressed_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*compressed_window))
        self.driver.get('https://tutor-qa.openstax.org/')
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        wait = WebDriverWait(self.driver, 15)
        user_menu = wait.until(
            expect.presence_of_element_located((By.CLASS_NAME,
                                               'navbar-toggle'))
        )
        assert(user_menu.is_displayed()), 'Menu not visible'
        user_menu.click()
        login = wait.until(
            expect.presence_of_element_located((By.LINK_TEXT,
                                               'Login'))
        )
        assert(login.is_displayed()), 'Login link not visible'
        login.click()
        username = self.driver.find_element_by_id('auth_key')
        username.send_keys('admin')
        password = self.driver.find_element_by_id('password')
        password.send_keys('password')
        sign_in = self.driver.find_element_by_xpath('//button[text()=' +
                                                    '"Sign in"]')
        sign_in.click()
        user_menu = wait.until(
            expect.presence_of_element_located((By.CLASS_NAME,
                                               'navbar-toggle'))
        )
        assert(user_menu.is_displayed()), 'User menu not visible'
        user_menu.click()
        user_sub_menu = wait.until(
            expect.presence_of_element_located((By.CLASS_NAME,
                                               'dropdown-toggle'))
        )
        user_sub_menu = self.driver.find_element(By.CLASS_NAME,
                                                 'dropdown-toggle')
        assert(user_sub_menu.is_displayed()), 'User sub-menu not visible'
        user_sub_menu.click()
        logout = self.driver.find_element(By.XPATH, '//button[@aria-label=' +
                                          '"Sign out"]')
        assert(logout.is_displayed()), 'Log Out not visible'

    @pytest.mark.skipif(IN_PROGRESS, reason='In progress')
    def test_accounts_login(self):
        self.driver.get('https://accounts-qa.openstax.org/')
        assert('Sign in with' in self.driver.title), 'Unable to load page'
        assert(False), 'Incomplete test'

    def tearDown(self):
        self.driver.quit()
        status = (sys.exc_info() == (None, None, None))
        self.ps.update_job(self.driver.session_id, passed=status)
