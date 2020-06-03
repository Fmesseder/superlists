from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    """Functional test definition"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_later(self):
        #The user goes to check out the homepage of a new app
        self.browser.get('http://localhost:8000')

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
        time.sleep(2)
        self.check_for_row_in_list_table("1: Buy peacock feathers")

        #There is still a text box inviting the user to add another item.
        #The user enters "Use the peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)

        #the page updates again and now show both items on the users list
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table("2: Use peacock feathers to make a fly")

        #The user wonders whether the site will remember the list.
        #Then the user sees that the site has generated a unique URL for her
        #-- there will be some more explanatory text here
        self.fail('Finish the test')

        #the user visits the URL and the todo list is still there

        #The End

if __name__ == '__main__':
    unittest.main(warnings='ignore')
