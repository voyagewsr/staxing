#StaxHelper
##Constants:
<code>LOCAL</code>  <pre>Use ChromeDriver locally</pre>
<code>REMOTE</code> <pre>Use Sauce Labs</pre>
<code>CONDENSED_WIDTH</code>    <pre>Compact screen max width</pre>
<code>WAIT_TIME</code>  <pre>Standard time in seconds to wait for a command</pre>
	<code>READING</code>   <pre>Assignment type: reading</pre>
	<code>HOMEWORK</code>	<pre>Assignment type: homework</pre>
	<code>EXTERNAL<code>   <pre>Assignment type: external</pre>
	<code>EVENT</code> <pre>Assignment type: event</pre>
	<code>REVIEW</code>    <pre>Assignment type: review</pre>

##Methods:
-------
<code>StaxHelper.run_on</code>  <pre>Run tests locally or on Sauce Labs</pre>
<code>_Class Method_ remote=True</code> <pre>(<code>bool</code>)</pre>
<code>pasta_user=None</code>    <pre>(<code>pastasauce.PastaSauce</code>)</pre>
<code>capabilities=None</code>  <pre>(<code>dict</code>)</pre>

<code>user	# A user object
 	username=None (str)
 	password=None (str)
 	site=None (str)

user.get_site	Access a particular Tutor site
 	driver    (selenium.webdriver)

user.set_site   Change the site URL
 	url=''    (str)

user.login 	Tutor login control
 	driver    (selenium.webdriver)
 	username=None (str)
 	password=None (str)
 	url=None  (str)

user.open_user_menu User menu opener
 	driver 	(selenium.webdriver)

user.logout	Logout control
 	driver 	(selenium.webdriver)

user.tutor_logout	Tutor logout
 	driver 	(selenium.webdriver)

user.accounts_logout	Accounts logout
    driver 	(selenium.webdriver)

user.select_course	Course selection
 	driver 	(selenium.webdriver)
 	title=None 	(str)
 	category=None 	(str)

user.view_reference_book	Access the reference book
 	driver 	(selenium.webdriver)
------
teacher	A teacher object
    username=None 	(str)
    password=None 	(str)

teacher.add_assignment	Add an assignment
 	driver 	(selenium.webdriver)
 	assignment 	(str constant)
 	args 	(dict)

teacher.change_assignment	Alter an existing assignment
 	driver 	(selenium.webdriver)
 	assignment	(str constant)
 	args	(dict)

teacher.delete_assignment	Delete an existing assignment (if available)
 	driver                (selenium.webdriver)
 	assignment            (str constant)
 	args                  (dict)

teacher.goto_menu_item	Go to a specific user menu item
    driver                 (selenium.webdriver)
    item                   (str)

teacher.goto_calendar	Return the teacher to the calendar dashboard
    driver                 (selenium.webdriver)

teacher.goto_performance_forecast	Access the performance forecast page
    driver	               (selenium.webdriver)

teacher.goto_student_scores	Access the student scores page
    driver                 (selenium.webdriver)
------
student	A student object
    username=None          (str)
    password=None	         (str)

student.work_assignment	Work an assignment
    title                  (str)
    total_segments         (‘all’ or int)

student.goto_past_work	View work for previous weeks
    [no arguments]

student.goto_performance_forecast	View the student performance forecast
 	[no arguments]

student.practice	Complete a set of 5 practice problems
    section                (str)
------
admin	An administrator object
    username=None          (str)
    password=None          (str)

admin.goto_admin_control	Access the administrator controls
    [no arguments]

admin.goto_courses	Access the course admin control
    [no arguments]

admin.goto_ecosystems	Access the ecosystem admin control
    [no arguments]
</code>
