from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define the chromedriver service
s = Service(ChromeDriverManager().install())

# Instantiate the webdriver
driver = webdriver.Chrome(service=s)

# The base URL for the pages to scrape
page_URL = "https://www.spoj.com/problems/classical/sort=0,start={}"

# Function to get all the problem links from the SPOJ problems page
def get_problem_links(url):
    # Load the URL in the browser
    driver.get(url)
    # Wait for 5 seconds to ensure the page is fully loaded
    time.sleep(5)
    # Find all the problem link elements on the page
    link_elements = driver.find_elements(By.CSS_SELECTOR, "table.problems > tbody > tr > td > a")
    # Extract the href attribute from the link elements and store the links in a list
    links = [link.get_attribute("href") for link in link_elements]
    return links

# List to store the final list of links
my_ans = []

# Specify the number of pages you want to scrape (e.g., 5 pages)
num_pages = 10

# Loop through the pages you're interested in
for page in range(num_pages):
    # Calculate the start index for the page
    start = page * 50
    # Construct the URL for the page
    page_url = page_URL.format(start)
    # Call the function to get the problem links from the SPOJ problems page
    page_links = get_problem_links(page_url)
    # Append the links to the final list
    my_ans += page_links

# Remove any duplicates that might have been introduced in the process
my_ans = list(set(my_ans))

# Open a file to write the results to
with open('spoj_problems.txt', 'a') as f:
    # Iterate over each link in the final list
    for link in my_ans:
        # Write each link to the file, followed by a newline
        f.write(link+'\n')

# Print the total number of links found
print(len(my_ans))

# Close the browser
driver.quit()