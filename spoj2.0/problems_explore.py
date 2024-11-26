# Import required packages
import os
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

# Define the base URL for the problems
base_url = "https://www.spoj.com/problems/classical/"

# Read the file with problem names/URLs
def get_array_of_links():
    arr = []  # Array to store the lines of the file
    # Open the file
    with open("spoj_problems.txt", "r") as file:
        # Read each line one by one
        for line in file:
            arr.append(line.strip())
    return arr

# Create a folder for storing the problem data
QDATA_FOLDER = "Qdata"
os.makedirs(QDATA_FOLDER, exist_ok=True)

# Function to scrape problem data
def scrape_problem_data(url, index):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "prob")))

        heading_element = driver.find_element(By.CLASS_NAME, "prob")
        heading = heading_element.find_element(By.TAG_NAME, "h2").text

        body_element = driver.find_element(By.ID, "problem-body")
        body = body_element.text

        print(heading)

        if heading:
            add_text_to_index_file(heading)
            add_link_to_Qindex_file(url)
            create_and_add_text_to_file(str(index), body)

        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

# Helper functions for writing data to files
def add_text_to_index_file(text):
    index_file_path = os.path.join(QDATA_FOLDER, "index.txt")
    with open(index_file_path, "a") as index_file:
        index_file.write(text + "\n")

def add_link_to_Qindex_file(text):
    index_file_path = os.path.join(QDATA_FOLDER, "Qindex.txt")
    with open(index_file_path, "w", encoding="utf-8", errors="ignore") as Qindex_file:
        Qindex_file.write(text)

def create_and_add_text_to_file(file_name, text):
    folder_path = os.path.join(QDATA_FOLDER, file_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name + ".txt")
    with open(file_path, "w", encoding="utf-8", errors="ignore") as new_file:
        new_file.write(text)

# Get the array of problem URLs
arr = get_array_of_links()
index = 1

# Scrape data for each problem
for link in arr:
    success = scrape_problem_data(link, index)
    if success:
        index += 1

# Quit the driver
driver.quit()
