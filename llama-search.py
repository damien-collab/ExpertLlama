import os
import requests
from googleapiclient.discovery import build
# import beautifulsoup4
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import streamlit as st




# text inputs
api_key = st.text_input("Google API Key", value=os.getenv("GOOGLE_API_KEY"), type="password")
search_engine_id = st.text_input("Google Search Engine ID", value=os.getenv("GOOGLE_SEARCH_ENGINE_ID"))




def search(query, num_results=1):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=search_engine_id, num=num_results).execute()
    return res.get('items', [])

def fetch_content_with_selenium(url):
    options = webdriver.FirefoxOptions()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    
    try:
        # Try waiting for a known element
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article, main"))
        )
    except Exception as e:
        print(f"Primary wait failed: {e}")
        try:
            # Fallback strategy: wait for body if specific elements are not found
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except Exception as fallback_e:
            print(f"Fallback wait failed: {fallback_e}")
            driver.quit()
            return ""
    
    content = driver.page_source
    driver.quit()
    
    soup = BeautifulSoup(content, 'html.parser')
    return clean_text(soup)

def clean_text(soup):
    for script in soup(["script", "style", "header", "footer", "nav", "form"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def print_results_and_fetch_content(results):
    for i, result in enumerate(results, start=1):
        title = result.get('title')
        link = result.get('link')
        snippet = result.get('snippet')
        
        print(f"Result {i}:")
        print(f"Title: {title}")
        print(f"URL: {link}")
        print(f"Snippet: {snippet}\n")
        
        # Fetch and print content
        # content = fetch_content_with_selenium(link)
        # print(f"Content of URL:\n{content}...")  # Print first 500 characters of the content
        # print("-" * 80)

if __name__ == "__main__":
    query = "what is the price of bitcoin?"
    results = search(query)
    print_results_and_fetch_content(results)
