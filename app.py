import streamlit as st
from playwright.sync_api import sync_playwright

def run_browser(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        screenshot = page.screenshot()
        browser.close()
        return screenshot

st.title('Web Browser Command Center')

url = st.text_input('Enter a URL', 'https://www.google.com')

if st.button('Browse'):
    screenshot = run_browser(url)
    st.image(screenshot)