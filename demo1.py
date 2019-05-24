from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.get('https://www.baidu.com')