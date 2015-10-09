from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.ui import WebDriverWait


class Assignment(object):
    '''
    Shortcut functions to add, edit, and delete assignments
    '''
    READING = 'reading'
    HOMEWORK = 'homework'
    EXTERNAL = 'external'
    EVENT = 'event'
    REVIEW = 'review'

    WAIT_TIME = 15

    def __init__(self):
        '''
        Provide a switch-style dictionary to add assignments
        '''
        self.add = {
            Assignment.READING:
            (
                lambda driver, name, description, periods, reading_list, state:
                self.add_new_reading(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    readings=reading_list,
                    status=state)
            ),
            Assignment.HOMEWORK:
            (
                lambda driver, name, description, periods, problems, state:
                self.add_new_homework(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    problems=problems,
                    status=state)
            ),
            Assignment.EXTERNAL:
            (
                lambda driver, name, instruction, periods, url, state:
                self.add_new_external(
                    driver=driver,
                    title=name,
                    description=instruction,
                    periods=periods,
                    assignment_url=url,
                    status=state)
            ),
            Assignment.EVENT:
            (
                lambda driver, name, description, periods, state:
                self.add_new_event(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    status=state)
            ),
            Assignment.REVIEW:
            (
                lambda driver, name, description, periods, problems, url,
                state:
                self.add_new_review(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    assessments=problems,
                    assignment_url=url,
                    status=state)
            ),
        }
        self.edit = {
            Assignment.READING:
            (
                lambda driver, name, description, periods, reading_list, state:
                self.change_reading(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    readings=reading_list,
                    status=state)
            ),
            Assignment.HOMEWORK:
            (
                lambda driver, name, description, periods, problems, state:
                self.change_homework(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    problems=problems,
                    status=state)
            ),
            Assignment.EXTERNAL:
            (
                lambda driver, name, instruction, periods, url, state:
                self.change_external(
                    driver=driver,
                    title=name,
                    description=instruction,
                    periods=periods,
                    assignment_url=url,
                    status=state)
            ),
            Assignment.EVENT:
            (
                lambda driver, name, description, periods, state:
                self.change_event(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    status=state)
            ),
            Assignment.REVIEW:
            (
                lambda driver, name, description, periods, problems, url,
                state:
                self.change_review(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    assessments=problems,
                    assignment_url=url,
                    status=state)
            ),
        }
        self.remove = {
            Assignment.READING:
            (
                lambda driver, name, description, periods, reading_list, state:
                self.delete_reading(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    readings=reading_list,
                    status=state)
            ),
            Assignment.HOMEWORK:
            (
                lambda driver, name, description, periods, problems, state:
                self.delete_homework(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    problems=problems,
                    status=state)
            ),
            Assignment.EXTERNAL:
            (
                lambda driver, name, instruction, periods, url, state:
                self.delete_external(
                    driver=driver,
                    title=name,
                    description=instruction,
                    periods=periods,
                    assignment_url=url,
                    status=state)
            ),
            Assignment.EVENT:
            (
                lambda driver, name, description, periods, state:
                self.delete_event(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    status=state)
            ),
            Assignment.REVIEW:
            (
                lambda driver, name, description, periods, problems, url,
                state:
                self.delete_review(
                    driver=driver,
                    title=name,
                    description=description,
                    periods=periods,
                    assessments=problems,
                    assignment_url=url,
                    status=state)
            ),
        }

    def open_assignment_menu(self, driver):
        '''
        Open the Add Assignment menu if it is closed
        '''
        assignment_menu = driver.find_element(
            By.XPATH, '//button[contains(@class,"dropdown-toggle")]')
        # if the Add Assignment menu is not open
        if 'open' not in assignment_menu.find_element(By.XPATH, '..'). \
                get_attribute('class'):
            assignment_menu.click()

    def add_new_reading(self, driver, title, description, periods, readings,
                        status):
        '''
        Add a new reading assignment

        driver:      WebDriver - Selenium WebDriver instance
        title:       string - assignment title
        description: string - assignment description or additional instructions
        periods:     dict - key:   string <period name> OR 'all'
                            value: tuple  (<open date>, <close date>)
        readings:    [string] - chapter and section numbers to include in the
                                assignment
        '''
        try:
            self.open_assignment_menu(driver)
            driver.find_element(By.LINK_TEXT, 'Add Reading').click()
            wait = WebDriverWait(driver, Assignment.WAIT_TIME)
            wait.until(
                expect.visibility_of_element_located(
                    (By.CLASS_NAME, 'panel-body')
                )
            )
            driver.find_element(By.ID, 'reading-title').send_keys(title)
            driver.find_element(
                By.XPATH,
                '//div[contains(@class,"assignment-description")]//textarea' +
                '[contains(@class,"form-control")]'). \
                send_keys(description)
            if 'all' in periods:  # assign the same dates for all periods
                opens_on, closes_on = periods['all']
                driver.find_element(By.ID, 'hide-periods-radio').click()
                driver.find_element(
                    By.XPATH,
                    '//div[contains(@class,"-assignment-open-date")]//input'). \
                    send_keys(opens_on)
                driver.find_element(
                    By.XPATH,
                    '//div[contains(@class,"-assignment-due-date")]//input'). \
                    send_keys(closes_on)
            else:
                count = 0
                last = len(periods)
                for period in periods:
                    count += 1
                    if count > last:
                        break
                    if periods[period] is 'all' or period is 'skip':
                        continue
                    opens_on, closes_on = periods[period]
                    driver.find_element(
                        By.XPATH,
                        '//input[@id="period-toggle-' +
                        '%s"]/../following-sibling::div//input' % count). \
                        send_keys(opens_on)
                    driver.find_element(
                        By.XPATH,
                        '//input[@id="period-toggle-' +
                        '%s"]/../following-sibling::div/following-' % count +
                        'sibling::div//input'). \
                        send_keys(closes_on)
        except:
            return (False, 'Assignment creation failed')
        raise NotImplementedError
        return (True, 'Reading %s added.' % title)

    def add_new_homework(self, driver, title, description, periods, problems,
                         status):
        '''

        '''
        raise NotImplementedError

    def add_new_external(self, driver, title, description, periods,
                         assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def add_new_event(self, driver, title, description, periods, status):
        '''

        '''
        raise NotImplementedError

    def add_new_review(self, driver, title, description, periods, assessments,
                       assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def change_reading(self, driver, title, description, periods, readings,
                       status):
        '''

        '''
        raise NotImplementedError

    def change_homework(self, driver, title, description, periods, problems,
                        status):
        '''

        '''
        raise NotImplementedError

    def achange_external(self, driver, title, description, periods,
                         assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def change_event(self, driver, title, description, periods, status):
        '''

        '''
        raise NotImplementedError

    def change_review(self, driver, title, description, periods, assessments,
                      assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def delete_reading(self, driver, title, description, periods, readings,
                       status):
        '''

        '''
        raise NotImplementedError

    def delete_homework(self, driver, title, description, periods, problems,
                        status):
        '''

        '''
        raise NotImplementedError

    def delete_external(self, driver, title, description, periods,
                        assignment_url, status):
        '''

        '''
        raise NotImplementedError

    def delete_event(self, driver, title, description, periods, status):
        '''

        '''
        raise NotImplementedError

    def delete_review(self, driver, title, description, periods, assessments,
                      assignment_url, status):
        '''

        '''
        raise NotImplementedError
