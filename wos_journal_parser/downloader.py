import re
import time
import random
import logging

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from wos_journal_parser import config
from wos_journal_parser import logging_config

class Downloader:
  
  USER_AGENTS = (
    'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Iron/28.0.1550.1 Chrome/28.0.1550.1',
    'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.16',
  )
  
  logger = logging.getLogger(__name__)
  
  def __init__(self, data_path='data/', headless=False):
    self.headless = headless
    self.data_path = Path(data_path)
    self.driver_path = config.DRIVER_PATH
    self.driver = None
    self.files_dir = None
    
    self.create_raw_dir()
    
  def create_raw_dir(self):
    self.files_dir = (self.data_path / 'raw')
    self.logger.info(f"Created directory: {self.files_dir.absolute()}")
    self.files_dir.mkdir(exist_ok=True, parents=True)
    
  def setup(self):
    options = Options()
    options.headless = self.headless
    options.set_preference("general.useragent.override", random.choice(self.USER_AGENTS))
    profile_path = "/home/platon/.mozilla/firefox/ytjpgxrb.selenium/"
    options.profile = FirefoxProfile(profile_directory=profile_path)
    service = Service(executable_path=self.driver_path)
    self.driver = webdriver.Firefox(service=service, options=options)
    
  def __enter__(self):
    self.setup()
    return self
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    if self.driver:
      self.driver.quit()
  
  def _get_page_source(self, url):
    self.driver.get(url)
    self.logger.info(f"Navigated to URL: {url}")
    return self.driver.page_source
  
  def _save_current_page(self, page_number : int, source: str):
    file_path = self.files_dir / f"page_{page_number}.html"
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(source)
    self.logger.info(f"Saved page: {page_number} to {file_path}.")
  
  
  def _go_to_next_page(self, next_page_number) -> bool:
    try:
      self.logger.info(f"Trying to navigate to page: {next_page_number}")
      next_page_link = WebDriverWait(self.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@class='page-link' and text()='{str(next_page_number)}']"))
      )
      next_page_link.click()
      # sleep_seconds = random.randint(2, 5)
      # self.logger.info(f"Sleeping for {sleep_seconds} seconds before next page.")
      # time.sleep(sleep_seconds)
      return True
    except NoSuchElementException:
      self.logger.warning("No more pages found!")
      return False
    except Exception as e:
      self.logger.error(f"Error navigation to next page: {e}")
      return False

  def download(self):
    
    url = 'https://wos-journal.info'
    self.logger.info(f"Navigation to page URL: '{url}'.")
    self._get_page_source(url)
    self.logger.info("Successfully loaded organization page.")
    
    page_number = 0
    while True:
      self._save_current_page(page_number, self.driver.page_source)
      page_number+=1
      if not self._go_to_next_page(next_page_number=page_number):
        break
      
    self.logger.info("Download process finished.")
