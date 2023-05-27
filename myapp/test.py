from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
driver = webdriver.Chrome(chrome_options = options, executable_path=r'C:\\Users\\aali5\\scrapper\\myapp\\chromedriver.exe')
driver.get('http://google.com/')
print("Chrome Browser Invoked")
driver.quit()