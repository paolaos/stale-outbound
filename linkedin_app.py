import requests
import json
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
import streamlit as st

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

def extract_text_from_html(input_file_path):
    # Parse the HTML file into an lxml HTML object
    with open(input_file_path, 'rb') as file:
        html_content = file.read()
        tree = html.fromstring(html_content)

    # Extract the visible text content from the HTML
    visible_text = tree.text_content()

    visible_text = visible_text.replace("LinkedIn", "FunnyCorp")

    # Split the visible text into lines and filter out empty or whitespace-only lines
    lines = [line.strip() for line in visible_text.splitlines() if line.strip()]
    lines = lines[6:293]
    # Join the filtered lines back into visible text
    cleaned_visible_text = '\n'.join(lines) 
    return cleaned_visible_text

def extract_information(raw_text, product="an AI-powered lead generation and client engagement software"):
    api_key = "Nice try, loser"  # Replace with your actual API key
    # Define the API key and endpoint
    ENDPOINT = 'https://api.openai.com/v1/chat/completions'
    
    # Construct headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Define the parameters of your prompt
    data = {
        "temperature": 0.5,
        "model": "gpt-4",
        "messages": [{"role": "user", "content": f"I am an SDR, and I am selling {product}. I am looking to extract useful information from a piece of raw text obtained from a webpage. Please analyze the text and provide details that could be crucial for sales outreach of the product I want to sell. Ignore any line that is not relevant or that is unrelated to the request, and if you do not find anything feel free to let me know. Please return only 3 important pieces of information, and tell me what relevancy it could have with the product I want to sell: {raw_text}"}],
        "top_p": 1,
        "n": 1,
        "stop": None,
        "presence_penalty": 0,
        "frequency_penalty": 0
    }

    # Make the POST request
    response = requests.post(ENDPOINT, headers=headers, data=json.dumps(data))

    # Handle the response
    if response.status_code == 200:
        # The request was successful
        result = response.json()
        resp = result["choices"][0]["message"]["content"]
        return resp
    else:
        # The request failed
        print(f"Error: {response.status_code}, {response.text}")

def extract_linkedin_profile_info(profile_url, product_info):
    """Extracts the name, title, and education of a given LinkedIn profile.

    Args:
        profile_url: The URL of the LinkedIn profile.

    Returns:
        A dictionary containing the name, title, and education of the LinkedIn profile.
    """

    extract_html(profile_url)
    extracted_text = extract_text_from_html("page.html")
    resp = extract_information(extracted_text, product_info)
    return resp

def perform_analysis(profile_url, product_info):
    
    t0 = time.time()
    # Get the LinkedIn profile URL
    # Extract the profile information
    profile_info = extract_linkedin_profile_info(profile_url, product_info)
    # Print the profile information
    t1 = time.time()
    total = t1-t0
    print(f"Total workflow time: {total}")
    return profile_info

def entrypoint():
    st.title('Information extraction for personalization')
    profile_url = st.text_input("LinkedIn Profile URL", value="", max_chars=None, key=None, type="default", placeholder="https://www.linkedin.com/in/othmane-baddou/")
    product_info = st.text_input("Product to sell", value="", max_chars=None, key=None, type="default", placeholder="An AI-powered lead generation and client engagement software")
    if st.button('Submit') and (profile_url != "" and product_info != ""):
        profile_info = perform_analysis(profile_url, product_info)
        st.write(profile_info)


entrypoint()