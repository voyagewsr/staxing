import os
from selenium import webdriver


class StaxHelper(object):
    ''''''
    LOCAL = False
    REMOTE = not LOCAL

    def __init__(self):
        ''''''
        self.user = User()
        self.teacher = Teacher()
        self.student = Student()
        self.admin = Admin()
        self.email = Email()

    @classmethod
    def run_on(cls, remote=True, pasta_user=None, capabilities=None):
        if remote:
            return webdriver.Remote(
                command_executor=(
                    'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' %
                    (pasta_user.get_user(), pasta_user.get_access_key())
                ),
                desired_capabilities=capabilities
            )
        return webdriver.Chrome()


class User(object):
    ''''''
    def __init__(self, username=None, password=None, site=None):
        ''''''
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
        ''''''
        if url is not '':
            self.url = url
        return self.url

    def login(self):
        ''''''

    def logout(self):
        ''''''

    def select_course(self):
        ''''''

    def view_reference_book(self):
        ''''''


class Teacher(object):
    ''''''
    def __init__(self, username=None, password=None):
        ''''''
        self.name = username if username is not None \
            else os.environ['TEACHER_USER']
        self.password = password if password is not None \
            else os.environ['TEACHER_PASSWORD']

    def add_assignment(self):
        ''''''

    def change_assignment(self):
        ''''''

    def delete_assignment(self):
        ''''''

    def goto_calendar(self):
        ''''''

    def goto_performance_forecast(self):
        ''''''

    def goto_student_scores(self):
        ''''''


class Student(object):
    ''''''
    def __init__(self, username=None, password=None):
        ''''''
        self.name = username if username is not None \
            else os.environ['STUDENT_USER']
        self.password = password if password is not None \
            else os.environ['STUDENT_PASSWORD']

    def work_assignment(self):
        ''''''

    def goto_past_work(self):
        ''''''

    def goto_performance_forecast(self):
        ''''''

    def practice(self):
        ''''''


class Admin(object):
    ''''''
    def __init__(self, username=None, password=None):
        ''''''
        self.name = username if username is not None \
            else os.environ['ADMIN_USER']
        self.password = password if password is not None \
            else os.environ['ADMIN_PASSWORD']

    def goto_admin_control(self):
        ''''''

    def goto_courses(self):
        ''''''

    def goto_ecosystems(self):
        ''''''


class Email(object):
    ''''''
    def __init__(self, username=None, email=None, password=None):
        ''''''
        self.name = username if username is not None\
            else os.environ['TEST_EMAIL_USER']
        self.email = email if email is not None \
            else os.environ['TEST_EMAIL_ACCOUNT']
        self.password = password if password is not None \
            else os.environ['TEST_EMAIL_PASSWORD']
