import time
import random
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from lxml.html import fromstring


def load_driver():
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--window-size=375,2000')
    options.add_argument('--disable-dev-shm-usage')      
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def extract_html(profile_url):
    driver = load_driver()
    redirected = True
    while redirected:
        driver.get(profile_url)
        current_url = driver.current_url
        if not current_url.startswith("https://www.linkedin.com/authwall"):
            redirected = False
        else:
            random_delay = random.uniform(2, 5)
            print(f"Waiting for {random_delay:.2f} seconds...")
            time.sleep(random_delay)
        
    random_delay = random.uniform(2, 5)
    print(f"Waiting for {random_delay:.2f} seconds...")
    time.sleep(random_delay)

    # Get the page source (HTML content)
    page_source = driver.page_source

    # Save the HTML content to a file
    with open("page.html", "w", encoding="utf-8") as file:
        file.write(page_source)
        
    return page_source


def clean_html(raw_html):
    html_element = fromstring(raw_html)

    list_elements_to_remove = [
        "/html/body/div[1]",
        "/html/body/div[4]/div/div/section",
        "/html/body/header"
    ]

    for el in list_elements_to_remove:
        try:
            elements_to_remove = html_element.xpath("//div[@class='remove-me']")
            for element in elements_to_remove:
                element.getparent().remove(element)
        except Exception as e:
            print(f"Error removing element {el}: {str(e)}")

    cleaned_html = html.tostring(html_element, encoding="utf-8").decode("utf-8")
    # Save the HTML content to a file
    with open("clean.html", "w", encoding="utf-8") as file:
        file.write(cleaned_html)
    return cleaned_html

def extract_information():
    return 0

def extract_linkedin_profile_info(profile_url):
    """Extracts the name, title, and education of a given LinkedIn profile.

    Args:
        profile_url: The URL of the LinkedIn profile.

    Returns:
        A dictionary containing the name, title, and education of the LinkedIn profile.
    """

    raw_html = extract_html(profile_url)
    # raw_html = open("page.html").read()
    cleaned_html = clean_html(raw_html)
    print(cleaned_html)
    # analyzed_html = extract_information(cleaned_html)

    # response = requests.get(profile_url)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # print(response.text)

    # Extract the name
    # name = soup.find('h1', class_='pv-profile-name').text

    # # Extract the title
    # title = soup.find('h2', class_='pv-top-card-section-title').text

    # # Extract the education
    # education = []
    # for education_item in soup.find_all('li', class_='pv-education-entity'):
    #     education.append(education_item.find('h3').text)

    # return {
    #     'name': name,
    #     'title': title,
    #     'education': education,
    # }

    return 0


if __name__ == '__main__':
    # Get the LinkedIn profile URL
    profile_url = 'https://www.linkedin.com/in/paola-os/'

    # Extract the profile information
    profile_info = extract_linkedin_profile_info(profile_url)

    # Print the profile information
    print(profile_info)


"""
Remove
#artdeco-global-alert-container > div > section
/html/body/div[4]/div/div/section
/html/body/header

CLICK ON /html/body/main/section[1]/div/section/section[1]/div/div[2]/div[1]/h1

"""