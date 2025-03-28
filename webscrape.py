from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from io import StringIO

options = Options()
options.page_load_strategy = 'normal'
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")
options.add_argument("--window-size=1200,800")

executable_path='/Users/jp/Downloads/chromedriver-mac-arm64/chromedriver'

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

website = "https://www.breakingpoint.gg/stats/advanced?orderBy=bp_rating"

def initiliaze_driver_settings():
    pass

def get_tournament_stats(website: str):
    pass

driver.get(website)

table = driver.find_element(By.TAG_NAME, "table")

# Extract table content
html_content = table.get_attribute('outerHTML')

# Close the driver
driver.quit()

# Wrap HTML in StringIO to avoid FutureWarning
html_buffer = StringIO(html_content)
df = pd.read_html(html_buffer)[0]

print(df)