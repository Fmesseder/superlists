from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    """Functional test definition"""

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_later(self):
        #The user goes to check out the homepage of a new app
        self.browser.get('http://localhost:8000')

        #The user notices that the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')

        #The user is invited to enter a todo item

        #The user types "Buy peacock feathers" into a text box

        #When the user hits enter, the pages updates, and now the page
        #lists "1: Buy peacock feathers" as an item in a todo list

        #There is still a text box inviting the user to add another item.
        #The user enters "Use the peacock feathers to make a fly"

        #The page updates again and now shows both items on the list

        #The user wonders whether the site will remember the list.
        #Then the user sees that the site has generated a unique URL for her
        #-- there will be some more explanatory text here

        #the user visits the URL and the todo list is still there

        #The End

if __name__ == '__main__':
    unittest.main(warnings='ignore')
