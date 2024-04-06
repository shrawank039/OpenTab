import streamlit as st
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import asyncio
import threading

browser = None

class Browser:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
    
    def start_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()

    def navigate(self, url):
        if not self.browser:
            self.start_browser()
        self.page.goto(url, wait_until='load')
        screenshot = self.page.screenshot()
        return screenshot

    def take_screenshot(self):
        if not self.page:
            raise ValueError('Page is not initialized. Please navigate to a URL first.')
        screenshot = self.page.screenshot()
        return screenshot
    
    def scroll_down(self, scroll_to_bottom=False):
        if not self.page:
            raise ValueError('Page is not initialized. Please navigate to a URL first.')
        if scroll_to_bottom:
            self.page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        else:
            self.page.evaluate('window.scrollTo(0, 0)')
        screenshot = self.page.screenshot()
        return screenshot
    
    def click(self, id):
        if not self.page:
            raise ValueError('Page is not initialized. Please navigate to a URL first.')
        self.page.click(id)
        print(f'Clicked on {id}')

    def search(self, id, text):
        if not self.page:
            raise ValueError('Page is not initialized. Please navigate to a URL first.')
        self.page.fill(id, text)
        self.page.press(id, 'Enter')
        print(f'Searched for {text}')
        self.page.wait_for_load_state('load')
        screenshot = self.page.screenshot()
        return screenshot
    

    def close_browser(self):
        self.page.close()
        self.browser.close()


def main():
    global browser
    browser = Browser()
    browser.start_browser()
    screenshot = browser.navigate('https://www.amazon.in/')
    #screenshot = browser.take_screenshot()
    #screenshot = browser.search('laptop')
    #browser.click('a[id="nav-hamburger-menu"]')
    #screenshot = browser.scroll_down(scroll_to_bottom=True)
    #browser.close_browser()
    st.image(screenshot)
    next()

def next():
    global browser
    if browser is None:
        st.write('Browser is not initialized. Please navigate to a URL first.')
        return
    screenshot = browser.search('#twotabsearchtextbox', 'laptop')
    st.image(screenshot)
    
st.set_page_config(
    page_title="OpenTab",
    layout="wide",
)

st.title('OpenTab')
#st.subheader("Powered by Function Calling in Gemini")


# Create two columns
col1, col2 = st.columns([1, 2])

# Use the first column for the chat input and history
with col1:
    #st.header('Chat')
    chat_history = st.text_area('Chat History', '', height=200)
    chat_input = st.text_input('Enter a prompt')

# Use the second column for the browser
with col2:
    st.header('Browser')
    url = st.text_input('Enter a URL', 'https://www.amazon.in/')
    if st.button('Browse'):
        main()
    if st.button('Search'):
        next()