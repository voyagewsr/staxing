class StaxHelper(object):
    ''''''
    def __init__(self):
        ''''''
        self.user = User()
        self.teacher = Teacher()
        self.student = Student()
        self.admin = Admin()


class User(object):
    ''''''
    def use_site(self, url=''):
        ''''''

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
    def goto_admin_control(self):
        ''''''

    def goto_courses(self):
        ''''''

    def goto_ecosystems(self):
        ''''''
