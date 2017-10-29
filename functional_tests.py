from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		
		# Simone wants to record his endless list of vscreen thoughts and todos,
		# he's heard of a very cool website and goes to check it out like anyone.
		self.browser.get('http://localhost:8000')


		# He notices the page title and header mention to-do lists
		self.assertIn( 'To-Do' ,self.browser.title)
		
		self.fail('finish the test, test first, test first')

		# He is invited to enter a to-do item straight away

		# He types "Make america great again" into a textbox

		# When he hits enter, the page updates, and now the page lists
		# "1: Buy peacock feathers" as an item in a to-do list

		# There is still the todo entry fieldset, he enters "Make VScreen great Again"

		# The page updates again and shows both items.

		# Simone wonders if the site will remember his list, 
		# especially if he clears his cookies, then notices the site has generated
		# a uniqute url for him and there is some explanatory text to that effect.

		# Simone visits that url in an incoginto tab and his todo items are still there.

		# Satisfied he then goes back to browsing "the internet", but there's a niggling
		# feeling that he should remove those items and take it seriously. I mean what a tool!
		
if __name__ == '__main__':
	unittest.main(warnings='ignore')
