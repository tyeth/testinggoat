from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(unittest.TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
		
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		
		# Simone wants to record his endless list of vscreen thoughts and todos,
		# he's heard of a very cool website and goes to check it out like anyone.
		self.browser.get('http://localhost:8000')


		# He notices the page title and header mention to-do lists
		self.assertIn( 'To-Do' ,self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text	
		self.assertIn('To-Do', header_text)
		
		
		# He is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')  
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# He types "Make america great again" into a textbox
		inputbox.send_keys('Make america great again')
		
		# When he hits enter, the page updates, and now the page lists
		# "1: Make america great again" as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)	
		time.sleep(10)  


		#		 self.assertTrue(
		#			 any(row.text == '1: Make america great again' for row in rows),
		#			f"New to-do item did not appear in table. Contents were:\n{table.text}"
		#		 )
		
		# There is still the todo entry fieldset, he enters "Make VScreen great Again"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Make VScreen great Again')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		
		# The page updates again and shows both items.
		self.check_for_row_in_list_table('1: Make america great again')
		self.check_for_row_in_list_table('2: Make VScreen great Again')
		
		# Simone wonders if the site will remember his list, 
		# especially if he clears his cookies, then notices the site has generated
		# a uniqute url for him and there is some explanatory text to that effect.
		self.fail('finish the test, test first, test first')

		# Simone visits that url in an incoginto tab and his todo items are still there.

		# Satisfied he then goes back to browsing "the internet", but there's a niggling
		# feeling that he should remove those items and take it seriously. I mean what a tool!
		
if __name__ == '__main__':
	unittest.main(warnings='ignore')
