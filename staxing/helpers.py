import os
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
from requests import HTTPError


class StaxHelper(object):
    ''''''
    LOCAL = False  # use ChromeDriver locally
    REMOTE = not LOCAL  # use Sauce Labs
    CONDENSED_WIDTH = 767  # pixels
    WAIT_TIME = 15  # seconds

    def __init__(self):
        '''
        Initialize helper classes
        '''
        self.user = User()
        self.teacher = Teacher()
        self.student = Student()
        self.admin = Admin()
        self.email = Email()

    @classmethod
    def run_on(cls, remote=True, pasta_user=None, capabilities=None):
        '''
        Ready the correct WebDriver
        '''
        if remote:
            if pasta_user is None:
                raise(TypeError('Sauce Labs user required for remote testing'))
            return webdriver.Remote(
                command_executor=(
                    'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' %
                    (pasta_user.get_user(), pasta_user.get_access_key())
                ),
                desired_capabilities=capabilities
            )
        return webdriver.Chrome()


class User(object):
    '''
    General use class functions
    '''
    def __init__(self, username=None, password=None, site=None):
        '''
        Set test defaults
        -----------------
        User: generic teacher
        Site: tutor-qa.openstax.org
        '''
        self.name = username if username is not None \
            else os.environ['TEACHER_USER']
        self.password = password if password is not None \
            else os.environ['TEACHER_PASSWORD']
        self.url = site if site is not None \
            else os.environ['SERVER_URL']
        if self.url[0:5] != 'https' and self.url[0:5] != 'http:':
            self.url = 'https://' + self.url
        if self.url is None:
            raise(ValueError('URL: "' + str(self.url) + '" is not valid'))

    def use_site(self, url=''):
        '''
        Change site URL
        '''
        if url is not '':
            self.url = url
        return self.url

    def login(self, driver, username=None, password=None, url=None):
        '''
        Tutor login control

        Requires a Tutor or Accounts instance
        Branching to deal with standard or compact screen widths
        '''
        url_address = self.url if url is None else url
        try:
            # open the URL
            driver.get(url_address)
            # if coming from Tutor, click on the login button
            if 'tutor' in url_address:
                # check to see if the screen width is normal or condensed
                if driver.get_window_size()['width'] <= \
                        StaxHelper.CONDENSED_WIDTH:
                    # get small-window menu toggle
                    is_collapsed = driver.find_element(
                        By.XPATH,
                        '//button[contains(@class,"navbar-toggle")]'
                    )
                    # check if the menu is collapsed and, if yes, open it
                    if('collapsed' in is_collapsed.get_attribute('class')):
                        is_collapsed.click()
                driver.find_element(By.LINK_TEXT, 'Login').click()
            # enter the username and password
            driver.find_element(By.ID, 'auth_key'). \
                send_keys(self.name if username is None else username)
            driver.find_element(By.ID, 'password'). \
                send_keys(self.password if password is None else password)
            # click on the sign in button
            driver.find_element(
                By.XPATH, '//button[text()="Sign in"]'
            ).click()
        except Exception:
            return (False, 'Log in failed')
        return (True, 'Log in successful')

    def logout(self, driver):
        '''
        Logout control
        '''
        url_address = driver.current_url

        try:
            if 'tutor' in url_address:
                self.tutor_logout(driver)
            elif 'accounts' in url_address:
                self.accounts_logout(driver)
            else:
                raise HTTPError('Not an OpenStax URL')
        except HTTPError as ex:
            raise ex
        except Exception:
            return (False, 'Logout failed')
        return (True, 'Logout successful')

    def tutor_logout(self, driver):
        '''
        Tutor logout helper

        ToDo: branching to handle if a toggle is already open
        '''
        size = driver.get_window_size()
        wait = WebDriverWait(driver, StaxHelper.WAIT_TIME)
        if size['width'] <= StaxHelper.CONDENSED_WIDTH:
            # compressed window display on Tutor
            wait.until(
                expect.visibility_of_element_located(
                    (By.CLASS_NAME, 'navbar-toggle')
                )
            ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.CLASS_NAME, 'dropdown-toggle')
            )
        ).click()
        wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//button[@aria-label="Sign out"]')
            )
        ).click()

    def accounts_logout(self, driver):
        '''
        Accounts logout helper
        '''
        driver.find_element(By.LINK_TEXT, 'Sign out').click()

    def select_course(self, driver, title, category):
        '''
        Course selection

        ToDo: allow selection of course 3 or higher
        '''
        if 'dashboard' not in driver.current_url:
            return (True, 'No course selection available')
        if title:
            uses_option = 'title'
            course = title
        elif category:
            uses_option = 'category'
            course = category
        else:
            return (False, 'Unknown course selection "%s"' %
                    title if title else category)
        wait = WebDriverWait(driver, StaxHelper.WAIT_TIME)
        try:
            wait.until(
                expect.element_to_be_clickable(
                    (By.XPATH, '//div[@data-%s="%s"]//a' %
                     (uses_option, course))
                )
            ).click()
        except Exception:
            return (False, 'Course selection failed')
        return (True, 'Course %s selected' % course)

    def view_reference_book(self):
        '''
        Access the reference book

        ToDo: all
        '''


class Teacher(object):
    '''
    Teacher controls
    '''
    def __init__(self, username=None, password=None):
        '''
        Initialize with provided or environmental credentials
        '''
        self.name = username if username is not None \
            else os.environ['TEACHER_USER']
        self.password = password if password is not None \
            else os.environ['TEACHER_PASSWORD']

    def add_assignment(self, assignment):
        '''
        Add an assignment

        ToDo: all
        '''

    def change_assignment(self):
        '''
        Alter an existing assignment

        ToDo: all
        '''

    def delete_assignment(self):
        '''
        Delete an existing assignment (if available)

        ToDo: all
        '''

    def goto_calendar(self):
        '''
        Return the teacher to the calendar dashboard

        ToDo: all
        '''

    def goto_performance_forecast(self):
        '''
        Access the performance forecast page

        ToDo: all
        '''

    def goto_student_scores(self):
        '''
        Access the student scores page

        ToDo: all
        '''


class Student(object):
    '''
    Student controls
    '''
    def __init__(self, username=None, password=None):
        '''
        Initialize with provided or environmental credentials
        '''
        self.name = username if username is not None \
            else os.environ['STUDENT_USER']
        self.password = password if password is not None \
            else os.environ['STUDENT_PASSWORD']

    def work_assignment(self):
        '''
        Work an assignment

        ToDo: all
        '''

    def goto_past_work(self):
        '''
        View work for previous weeks

        ToDo: all
        '''

    def goto_performance_forecast(self):
        '''
        View the student performance forecast

        ToDo: all
        '''

    def practice(self):
        '''
        Complete a set of 5 practice problems

        ToDo: all
        '''


class Admin(object):
    '''
    Admin controls
    '''
    def __init__(self, username=None, password=None):
        '''
        Initialize with provided or environmental credentials
        '''
        self.name = username if username is not None \
            else os.environ['ADMIN_USER']
        self.password = password if password is not None \
            else os.environ['ADMIN_PASSWORD']

    def goto_admin_control(self):
        '''
        Access the administrator controls

        ToDo: all
        '''

    def goto_courses(self):
        '''
        Access the course admin control

        ToDo: all
        '''

    def goto_ecosystems(self):
        '''
        Access the ecosystem admin control

        ToDo: all
        '''


class Email(object):
    '''
    Test account for e-mail messaging with a live Gmail account
    '''
    def __init__(self, username=None, email=None, password=None):
        '''
        Initialize with provided or environmental credentials
        '''
        self.name = username if username is not None\
            else os.environ['TEST_EMAIL_USER']
        self.email = email if email is not None \
            else os.environ['TEST_EMAIL_ACCOUNT']
        self.password = password if password is not None \
            else os.environ['TEST_EMAIL_PASSWORD']
