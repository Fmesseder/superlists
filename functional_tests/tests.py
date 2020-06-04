from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    """Functional test definition"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return

            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise # -*- coding: utf-8 -*-
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        #The user goes to check out the homepage of a new app
        self.browser.get(self.live_server_url)

        #The user notices that the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #The user is invited to enter a todo item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                            'Enter a to-do item')

        #The user types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        #When the user hits enter, the pages updates, and now the page
        #lists "1: Buy peacock feathers" as an item in a todo list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        #There is still a text box inviting the user to add another item.
        #The user enters "Use the peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        #the page updates again and now show both items on the users list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #User starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')

        #The user types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        #When the user hits enter, the pages updates, and now the page
        #lists "1: Buy peacock feathers" as an item in a todo list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        #User notices that her list has a unique URL
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')

        #User 2 comes to the saved_items

        ##We use a new browser session to make sure no information of user 1
        ##is coming through from cookies, etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #user 2 visits the home page. There is no sign of user 1 list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('Use peacock feathers to make a fly',page_text)

        #user 2 starts a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy milk")

        #user 2 gets his own URL
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)

        #again, there is no trace of user1 list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('Buy milk',page_text)
        
        #The End
