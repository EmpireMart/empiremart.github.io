from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os.path
import csv
import requests
from os import path
from csv import writer
from csv import reader

class BookScraper:
	results =[]

	with open("Book_Bulk.csv", "r") as csv_file:
		csv_reader = csv.reader(csv_file)
		
		next(csv_file)   

		for line in csv_reader:

			# chrome_options = webdriver.ChromeOptions()
			# chrome_options.add_argument('headless')
			# chrome_options.add_argument('window-size=1920x1080')
			# chrome_options.add_argument("disable-gpu")
			PATH = "C:\Program Files (x86)\chromedriver.exe"
			driver = webdriver.Chrome(PATH)

			driver.get("https://www.bookdepository.com/")

			Search = WebDriverWait(driver, 10).until(
					EC.presence_of_element_located((By.XPATH, '//*[@id="book-search-form"]/div[1]/input[1]'))
					)
			Search.clear()
			Search.send_keys(line[3])
			Search.send_keys(Keys.RETURN)

			driver.maximize_window()
			wait = WebDriverWait(driver, 2)

			fname = "Scraped_Book_Data.csv"
			fileexist = 1
			if not path.exists(fname):
				fileexist = 0
			f = open(fname, "a", encoding="utf-8")

			if fileexist==0:
				f.write("Title,Author,Language,Genre,Book Format,Publisher,Year,Price")

			try:
				title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.item-info h1"))).text
				newtitle = '"{0}"'.format(title)
				print(newtitle)

			except:
				newtitle = "Not Available"
				print(newtitle)

			try:
				author = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.author-info.hidden-md span[itemprop='author'] span"))).text
				newauthor = '"{0}"'.format(author)
				print(newauthor)

			except:
				newauthor = "Not Available"
				print(newauthor)

			language = "English"

			try:
				genre = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.active"))).text
				newgenre = '"{0}"'.format(genre)
				print(newgenre)

			except:
				newgenre = "Not Available"
				print(newgenre)

			try:
				bookformat = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.item-info li"))).text
				print(bookformat)

			except:
				bookformat = "Not Available"
				print(bookformat)

			try:
				publisher = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.biblio-info-wrap span[itemprop='publisher'] span"))).text
				newpublisher = '"{0}"'.format(publisher)
				print(newpublisher)

			except:
				publisher = "Not Available"
				newpublisher = '"{0}"'.format(publisher)
				print(newpublisher)

			try:
				date = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.biblio-info-wrap span[itemprop='datePublished']"))).text
				year = date[-4:]
				print(year)

			except:
				year = "Not Available"
				print(year)

			try:
				price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.item-info-wrap span[class='sale-price']"))).text
				price = price.replace('A','')
				print(price)

			except:

				try:
					price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.item-info-wrap p"))).text
					price = price.replace('List price: A','')
					print(price)

				except:
					price = "Not Available"
					print(price)

			finally:
				f.write("\n" + newtitle + "," + newauthor + "," + language + "," + newgenre + "," + bookformat + "," + newpublisher + "," + year + "," + price)
				driver.quit()

if __name__ == '__main__':
	scraper = BookScraper()
	scraper.run()
