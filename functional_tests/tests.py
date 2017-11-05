from django.test import LiveServerTestCase
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
	
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		
	def tearDown(self):
		self.browser.quit()
		
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
					raise e
				time.sleep(0.5)

				
	def test_multiple_users_can_start_lists_at_different_urls(self):
		# simone starts a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Make VScreen great Again')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Make VScreen great Again')
		
		# he notices that his list has a unique url
		simone_list_url = self.browser.current_url
		self.assertRegex(simone_list_url, '/lists/.+')
		
		# Now a new user, Nathan, comes along to the site
		
		## we use a new browser session to make sure that no information of simone's 
		## is coming through from cookies etc.
		self.browser.quit()
		self.browser =  webdriver.Firefox()
		
		# Nathan visits the homepage. There is no sign of Simone's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Make america great again', page_text)
		self.assertNotIn('Make VScreen great Again', page_text)
		
		# Nathan starts a new list by entering a new item. He is less crazy than Simone.
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy Milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy Milk')
		
		# Nathan gets his own url
		nathan_list_url = self.browser.current_url
		self.assertRegex(nathan_list_url, '/lists/.+')
		self.assertNotEqual(nathan_list_url,simone_list_url)
		
		# Again, there is no trace of Simone's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Make america great again',page_text)
		self.assertIn('Buy Milk',page_text)
		
		# Satisfied they both go back to sleep
	
	def test_can_start_a_one_person_list_and_retrieve_it_later(self):
		
		# Simone wants to record his endless list of vscreen thoughts and todos,
		# he's heard of a very cool website and goes to check it out like anyone.
		self.browser.get(self.live_server_url)


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
		time.sleep(1)  
		self.wait_for_row_in_list_table('1: Make america great again')
		
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
		self.wait_for_row_in_list_table('2: Make VScreen great Again')
		self.wait_for_row_in_list_table('1: Make america great again')
		
		# Simone wonders if the site will remember his list, 
		# especially if he clears his cookies, then notices the site has generated
		# a uniqute url for him and there is some explanatory text to that effect.
		self.fail('finish the test, test first, test first')

		# Simone visits that url in an incoginto tab and his todo items are still there.

		# Satisfied he then goes back to browsing "the internet", but there's a niggling
		# feeling that he should remove those items and take it seriously. I mean what a tool!
		
