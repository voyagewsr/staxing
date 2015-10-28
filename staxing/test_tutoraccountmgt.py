import unittest
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait

from pastasauce import PastaSauce, PastaDecorator
from . import StaxHelper


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
browsers = [browsers[3]]
standard_window = (1440, 800)
compressed_window = (700, 500)


@PastaDecorator.on_platforms(browsers)
class TestTutorAcctMgt(unittest.TestCase):
    ''''''
    def setUp(self):
        self.ps = PastaSauce()
        self.helper = StaxHelper()
        self.desired_capabilities['name'] = self.id()
        self.driver = StaxHelper.run_on(
            StaxHelper.LOCAL, self.ps, self.desired_capabilities
        )
        self.driver.implicitly_wait(15)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.set_window_size(*standard_window)
        self.rword = self.helper.user.assignment.rword

    def tearDown(self):
        self.driver.quit()
        status = (sys.exc_info() == (None, None, None))
        self.ps.update_job(self.driver.session_id, passed=status)

    def test_user_registration(self):
        self.driver.get('https://accounts-qa.openstax.org/')
        assert('Sign in with' in self.driver.title), 'Unable to load page'
        self.driver.find_element(By.LINK_TEXT, 'Sign up').click()
        username = 'testuser_%s' % self.rword(5)
        first_name = 'Test User'
        last_name = self.rword(6)
        self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'register_username')
            )
        ).send_keys(username)
        self.driver.find_element(By.ID, 'register_password'). \
            send_keys('password')
        self.driver.find_element(By.ID, 'register_password_confirmation'). \
            send_keys('password')
        self.driver.find_element(
            By.XPATH, '//input[@class="standard" and @name="commit"]'
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'Finish setting up my account')
            )
        ).click()
        self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'register_username')
            )
        ).send_keys(username)
        self.driver.find_element(By.ID, 'register_title'). \
            send_keys(self.rword(2))
        self.driver.find_element(By.ID, 'register_first_name'). \
            send_keys(first_name)
        self.driver.find_element(By.ID, 'register_last_name'). \
            send_keys(last_name)
        self.driver.find_element(By.ID, 'register_suffix'). \
            send_keys(self.rword(2))
        self.driver.find_element(By.ID, 'register_full_name'). \
            send_keys('%s %s' % (first_name, last_name))
        self.driver.find_element(By.LINK_TEXT, 'Terms of Use').click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[@class="close"]')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.LINK_TEXT, 'Privacy Policy')
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//button[@class="close"]')
            )
        ).click()
        i_agree = self.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'register_i_agree')
            )
        )
        if not i_agree.is_selected():
            i_agree.click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.ID, 'register_submit')
            )
        ).click()
        assert('Your Account' in self.driver.title), 'Incorrect URL: %s' % \
            self.driver.current_url

    def test_user_login_standard(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: %sx%s, not %sx%s' %
             (size['width'], str(*size)))
        # open the test URL and click the login button
        self.driver.get(self.helper.user.url)
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        self.driver.find_element(By.LINK_TEXT, 'Login').click()
        # enter the username and password
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.helper.admin.name)
        self.driver.find_element(By.ID, 'password'). \
            send_keys(self.helper.admin.password)
        # click on the sign in button to log in
        self.driver.find_element(
            By.XPATH, '//button[text()="Sign in"]'
        ).click()
        # look for the user drop down menu and click to open it
        self.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'dropdown-toggle')
            )
        ).click()
        # is the log out link visible?
        logout = self.driver.find_element(By.CLASS_NAME, 'logout')
        assert('Log Out' in logout.text), 'Log out not visible'

    def test_user_login_compact(self):
        # resize the window to be closer to a mobile display width
        self.driver.set_window_size(*compressed_window)
        size = self.driver.get_window_size()
        assert(compressed_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*compressed_window))
        # open the test URL and click the login button within the sub-menu
        self.driver.get(self.helper.user.url)
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        user_menu = self.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'navbar-toggle')
            )
        )
        assert(user_menu.is_displayed()), 'Menu not visible'
        user_menu.click()
        login = self.wait.until(
            expect.presence_of_element_located(
                (By.LINK_TEXT, 'Login')
            )
        )
        assert(login.is_displayed()), 'Login link not visible'
        login.click()
        # enter the username and password
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.helper.admin.name)
        self.driver.find_element(By.ID, 'password'). \
            send_keys(self.helper.admin.password)
        # click on the sign in button to log in
        self.driver.find_element(
            By.XPATH, '//button[text()="Sign in"]').click()
        # look for the user drop down menu and click to open it
        user_menu = self.wait.until(
            expect.presence_of_element_located(
                (By.CLASS_NAME, 'navbar-toggle')
            )
        )
        assert(user_menu.is_displayed()), 'User menu not visible'
        user_menu.click()

    def test_accounts_login(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*standard_window))
        # open the test URL and click the login button within the sub-menu
        self.driver.get('https://accounts-qa.openstax.org/')
        assert('Sign in with' in self.driver.title), 'Unable to load page'
        # enter the username and password
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.helper.user.name)
        self.driver.find_element(By.ID, 'password'). \
            send_keys(self.helper.user.password)
        # click on the sign in button to log in
        self.driver.find_element(
            By.XPATH, '//button[text()="Sign in"]').click()
        # is the logged in user's login visible?
        self.driver.find_element(
            By.LINK_TEXT, self.helper.user.name).click()

    def test_account_login_failure(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*standard_window))
        self.driver.get('https://accounts-qa.openstax.org/')
        assert('Sign in with' in self.driver.title), 'Unable to load page'
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys('not_a_user_94720475')
        self.driver.find_element(By.ID, 'password'). \
            send_keys('failed_password')
        self.driver.find_element(By.XPATH,
                                 '//button[text()="Sign in"]').click()
        error_message = self.driver.find_element(By.XPATH,
                                                 '//p//strong/parent::*')
        assert('Incorrect' in error_message.text)

    def test_course_select(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*standard_window))
        self.driver.get(self.helper.user.url)
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        login = self.wait.until(
            expect.presence_of_element_located(
                (By.LINK_TEXT, 'Login')
            )
        )
        assert(login.is_displayed()), 'Login link not visible'
        login.click()
        self.driver.find_element(By.ID, 'auth_key'). \
            send_keys(self.helper.teacher.name)
        self.driver.find_element(By.ID, 'password'). \
            send_keys(self.helper.teacher.password)
        self.driver.find_element(By.XPATH, '//button[text()="Sign in"]'). \
            click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//div[@data-title="Physics"]//a')
            )
        ).click()
        dashboard = self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH, '//a[@class="navbar-brand active"]')
            )
        )
        assert('Physics' in dashboard.text)

    def test_password_reset(self):
        # resize the window to the standard HISD monitor width
        size = self.driver.get_window_size()
        assert(standard_window == (size['width'], size['height'])), \
            ('Window size set to: ' + str(*size) +
             ', not ' + str(*standard_window))
        self.driver.set_window_size(*standard_window)
        self.driver.get('https://accounts-qa.openstax.org/')
        assert('Sign in with' in self.driver.title), 'Unable to load page'
        link = self.driver.find_element(By.LINK_TEXT, 'Forgot password?')
        link.click()
        username = self.wait.until(
            expect.visibility_of_element_located(
                (By.ID, 'forgot_password_username')
            )
        )
        username.send_keys(self.helper.email.name)
        submit = self.driver.find_element(By.NAME, 'commit')
        submit.click()
        reset_message = self.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'ui-icon-info')
            )
        )
        reset_message = reset_message.find_element(By.XPATH, '..')
        assert('Password reset' in reset_message.text), 'Reset failed'
        body = self.driver.find_element(By.TAG_NAME, 'body')
        import platform
        if platform.system() is 'Darwin':  # Mac
            body.send_keys(Keys.COMMAND + 't')
        else:
            body.send_keys(Keys.CONTROL + 't')
        self.driver.get('https://mail.google.com/')
        assert('Gmail' in self.driver.title), 'Gmail login not available'
        username = self.driver.find_element(By.ID, 'Email')
        username.send_keys(self.helper.email.email)
        next_button = self.driver.find_element(By.ID, 'next')
        next_button.click()
        password = self.driver.find_element(By.ID, 'Passwd')
        password.send_keys(self.helper.email.password)
        stay_signed_in = self.driver.find_element(By.ID, 'PersistentCookie')
        if stay_signed_in.is_selected():
            stay_signed_in.click()
        next_button = self.driver.find_element(By.ID, 'signIn')
        next_button.click()
        try:
            reset_email = self.wait.until(
                expect.visibility_of_element_located(
                    (By.CLASS_NAME, 'y6')
                )
            )
        except:
            raise(AssertionError('Email message not received'))
        reset_email.click()
        try:
            reset_link = self.wait.until(
                expect.presence_of_element_located(
                    (By.XPATH, '//a[contains(@href, "accounts-qa")]')
                )
            )
        except:
            raise(AssertionError('Oops, wrong e-mail message'))
        link = reset_link.get_attribute('href')
        self.driver.close()
        self.driver = StaxHelper.run_on(
            StaxHelper.LOCAL, self.ps, self.desired_capabilities
        )
        self.driver.implicitly_wait(15)
        self.driver.set_window_size(*standard_window)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.get(link)
        new_password = self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH, '//input[@name="reset_password[password]"]')
            )
        )
        new_password.send_keys(self.helper.email.password)
        repeat_password = self.driver.find_element(
            By.ID, 'reset_password_password_confirmation'
        )
        repeat_password.send_keys(self.helper.email.password)
        submit = self.driver.find_element(By.NAME, 'commit')
        submit.click()
        reset_message = self.wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'ui-icon-info')
            )
        )
        reset_message = reset_message.find_element(By.XPATH, '..')
        assert('reset successfully' in reset_message.text)

    def test_ost_logo_click_user_not_logged_in(self):
        url = 'https://tutor-qa.openstax.org/'
        anchor = '#home'
        self.driver.get(url)
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//a[@class="navbar-brand" and @href="%s"]' % anchor)
            )
        ).click()
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//a[@class="navbar-brand" and @href="%s"]' % anchor)
            )
        )
        assert(self.driver.current_url is (url + anchor))

    def test_ost_logo_click_user_logged_in(self):
        self.helper.user.login(self.driver, 'teacher01', 'password')
        assert('OpenStax Tutor' in self.driver.title), 'Unable to load page'
        self.wait.until(
            expect.element_to_be_clickable(
                (By.XPATH,
                 '//a[contains(@class,"navbar-brand") ' +
                 'and @href="/dashboard/"]')
            )
        ).click()

        assert(False), 'Incomplete'
