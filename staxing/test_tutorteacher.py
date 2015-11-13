import unittest
import sys

from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait
import datetime

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


@PastaDecorator.on_platforms(browsers)
class TestTutorTeacher(unittest.TestCase):
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

        # # # TODO: setup test assignments # # #

    def tearDown(self):
        ''''''
        self.driver.quit()
        status = (sys.exc_info() == (None, None, None))
        self.ps.update_job(self.driver.session_id, passed=status)

    def test_teacher_views_calendar(self):
        ''''''
        today = datetime.date.today()
        today = today.strftime('%B %Y')
        cal_date = self.wait.until(
            expect.presence_of_element_located(
                (By.XPATH,
                 '//div[contains(@class,"calendar-header-label")]' +
                 '/span')
            )
        ).text
        assert(cal_date == today), 'Calendar date is not %s' % today

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_student_scores(self):
        ''''''
        # login teacher
        # self.helper.user.login(self.driver, 
        #                       self.helper.user.name, 
        #                       self.helper.user.password,
        #                       self.helper.user.url)
        # select a course
        # self.helper.user.select_course(self.driver, category='Physics')
        # click on student scores
        # 'courses' in URL
        assert(), ''
        self.helper.teacher.goto_student_scores(self.driver)
        # verify see 'Student Scores'
        assert(), ''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_reference_book(self):
        ''''''
        # login teacher
        # self.helper.user.login(self.driver, 
        #                       self.helper.user.name, 
        #                       self.helper.user.password,
        #                       self.helper.user.url)  
        # select a course
        # self.helper.user.select_course(self.driver, category='Physics')      
        # click on Browse the book
        # 'courses' in URL 
        assert(), ''
        self.helper.user.view_reference_book(self.driver)
        # verify see ToC
        assert(), ''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_roster(self):
        ''''''
        # login teacher
        # self.helper.user.login(self.driver, 
        #                       self.helper.user.name, 
        #                       self.helper.user.password,
        #                       self.helper.user.url)         
        # select a course
        # self.helper.user.select_course(self.driver, category='Physics')
        # click on link for the user name
        self.driver.find_element(By.LINK_TEXT, self.helper.user.name).click()
        # verify 'Course Roster' in the drop list after clicking the name
        assert(), ''
        # click on link Course Roster
        self.driver.find_element(By.LINK_TEXT, 'Course Roster').click()
        # verify 'Roster' in the page
        assert(), ''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_removes_a_student_from_class(self):
        ''''''
        # login teacher
        # self.helper.user.login(self.driver, 
        #                       self.helper.user.name, 
        #                       self.helper.user.password,
        #                       self.helper.user.url)
        # go to course roster
        self.helper.user.select_course(self.driver, category='Physics')
        # verify 'Course Roster' in the drop list after clicking the name
        assert(), ''
        self.driver.find_element(By.LINK_TEXT, self.helper.user.name).click()
        self.driver.find_element(By.LINK_TEXT, 'Course Roster').click()
        # verify 'Roster' in the page
        assert(), ''
        # verify a student with a certain name in class
        assert(), ''
        # verify a button with 'Drop' for that student in the page
        assert(), ''
        # click on Drop for a student
        self.driver.find_element(By.XPATH, '//div[@class="tab-content"]/div[1]/div/table/tbody/tr[2]/td[3]/a[2]/span').click()
        # verify another button with 'Drop' in the page
        assert(), ''
        # confirm to drop
        self.driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-danger').click()
        # verify that student not in class now
        assert(), ''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_moves_a_student_between_periods(self):
        ''''''
        # login teacher
        # self.helper.user.login(self.driver, 
        #                       self.helper.user.name, 
        #                       self.helper.user.password,
        #                       self.helper.user.url)
        # go to course roster
        # self.helper.user.select_course(self.driver, category='Physics')
        self.driver.find_element(By.LINK_TEXT, self.helper.user.name).click()
        self.driver.find_element(By.LINK_TEXT, 'Course Roster').click()
        # verify it is the 1st period
        # verify a student exist in course
        assert(), ''
        # verify the 'Change Period' button exist for the student
        assert(), ''
        # click on Change Period
        self.driver.find_element(By.LINK_TEXT, 'Change Period').click()
        # choose the period to change to
        self.driver.find_element(By.XPATH, '//div[@class="popover-content"]//a[.="2nd"]').click()
        # verify that the student is now in second period
        assert(), ''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_reading_analytics_aggregate(self):
        ''''''
        # login teacher
        # self.helper.user.login(self.driver, 
        #                       self.helper.user.name, 
        #                       self.helper.user.password,
        #                       self.helper.user.url)
        # select a course 
        # self.helper.user.select_course(self.driver, category='Physics')
        # go to calendar
        self.helper.teacher.goto_calendar(self.driver)
        # verify 'calendar' in URL
        assert(), ''
        # click on a reading on the calendar, this is calendar specific so the current one might not exist
        self.driver.find_element(By.XPATH, '//div[@class="col-xs-12"]//label[.="HW Chapter 3"]').click()
        # verify 'Review Metrics' in the pop up window
        assert(), ''
        # click on Review Metrics
        self.driver.find_element(By.LINK_TEXT, 'Review Metrics').click()
        # verify 'summary' in URL
        assert(), ''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_performance_forecast_aggregate(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver, 
                               self.helper.user.name, 
                               self.helper.user.password,
                               self.helper.user.url)
        # select a course
        self.helper.user.select_course(self.driver, category='Physics')
        # go to performance forcast
        self.helper.teacher.goto_performance_forecast(self.driver)

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_performance_forecast(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver, 
                               self.helper.user.name, 
                               self.helper.user.password,
                               self.helper.user.url)
        # select a course
        self.helper.user.select_course(self.driver, category='Physics')
        # click on student scores
        self.helper.teacher.goto_student_scores(self.driver)
        # select and click on a student's name (name varies for students and courses)
        self.driver.find_element(By.LINK_TEXT, 'Lily Bart').click()
        # verify it shows the student's performance forecast

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_external_summary(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver, 
                               self.helper.user.name, 
                               self.helper.user.password,
                               self.helper.user.url)        
        # select a course
        self.helper.user.select_course(self.driver, category='Physics')
        # go to calendar
        self.helper.teacher.goto_calendar(self.driver)
        # click on an external assignment on the calendar


    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_homework_summary(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver, 
                               self.helper.user.name, 
                               self.helper.user.password,
                               self.helper.user.url)        
        # select a course
        self.helper.user.select_course(self.driver, category='Physics')
        # go to calendar
        self.helper.teacher.goto_calendar(self.driver)
        # click on a homework assignment on the calendar
        self.driver.find_element(By.XPATH, '//div[@class="col-xs-12"]//label[.="HW Chapter 3"]').click()

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_reading_summary(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver, 
                               self.helper.user.name, 
                               self.helper.user.password,
                               self.helper.user.url)        
        # select a course
        self.helper.user.select_course(self.driver, category='Physics')
        # go to calendar
        self.helper.teacher.goto_calendar(self.driver)
        # click on a reading assignment on the calendar
        self.driver.find_element(By.XPATH, '//div[@class="col-xs-12"]//label[.="Read 3.1 Acceleration Pt1"]').click()

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_event_summary(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver, 
                               self.helper.user.name, 
                               self.helper.user.password,
                               self.helper.user.url)        
        # select a course
        self.helper.user.select_course(self.driver, category='Physics')
        # go to calendar
        self.helper.teacher.goto_calendar(self.driver)
        # click on an event on the calendar
        self.driver.find_element(By.XPATH, '//div[@class="col-xs-12"]//label[.="test prep"]').click()

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_review_summary(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_homework(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver, 
                               self.helper.user.name, 
                               self.helper.user.password,
                               self.helper.user.url) 
        # select a course
        self.helper.user.select_course(self.driver, category='Physics')
        # go to student scores
        self.helper.teacher.goto_student_scores(self.driver)
        # click on a student's homework
        self.driver.find_element(By.XPATH, '//div[@class="fixedDataTableLayout_rowsContainer"]/div[4]/div[2]/div/div/div[2]/div/div[2]/div/div/div/a/span').click()
        

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_homework_details(self):
        ''''''


    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_reading(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver, 
                               self.helper.user.name, 
                               self.helper.user.password,
                               self.helper.user.url) 
        # select a course
        self.helper.user.select_course(self.driver, category='Physics')
        # click on student scores
        self.helper.teacher.goto_student_scores(self.driver)
        # click on a student's reading
        self.driver.find_element(By.XPATH, '//div[@class="fixedDataTableLayout_rowsContainer"]/div[4]/div[2]/div/div/div[2]/div/div[2]/div/div/div/a/span').click()
         

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_reading_details(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_single_student_review(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_views_class_review_details(self):
        ''''''

    @pytest.mark.skipif(NOT_STARTED, reason='Not started')
    def test_teacher_export_matches_student_scores(self):
        ''''''
        # login teacher
        self.helper.user.login(self.driver, 
                               self.helper.user.name, 
                               self.helper.user.password,
                               self.helper.user.url)
        # select a course
        self.helper.user.select_course(self.driver, category='Physics')
        # click on student scores
        self.helper.teacher.goto_student_scores(self.driver)
        # generate export
        self.driver.find_element(By.XPATH, '//div[@class="export-button-buttons"]//button[.="Generate Export"]').click()
        # download export
        self.driver.find_element(By.LINK_TEXT, 'Download Export').click()

