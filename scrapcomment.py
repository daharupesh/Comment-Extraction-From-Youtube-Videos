from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time


def ScrapComment(url):
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    
    # Create the Service object
    service = Service(GeckoDriverManager().install())
    
    # Pass the Service object instead of executable_path
    driver = webdriver.Firefox(service=service, options=option)
    
    driver.get(url)
    prev_h = 0
    while True:
        height = driver.execute_script("""
                function getActualHeight() {
                    return Math.max(
                        Math.max(document.body.scrollHeight, document.documentElement.scrollHeight),
                        Math.max(document.body.offsetHeight, document.documentElement.offsetHeight),
                        Math.max(document.body.clientHeight, document.documentElement.clientHeight)
                    );
                }
                return getActualHeight();
            """)
        driver.execute_script(f"window.scrollTo({prev_h},{prev_h + 200})")
        # Adjust the sleep value based on your network connection
        time.sleep(1)
        prev_h += 200  
        if prev_h >= height:
            break
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    title_text_div = soup.select_one('#container h1')
    title = title_text_div and title_text_div.text
    
    comment_div = soup.select("#content #content-text")
    comment_list = [x.text for x in comment_div]
    
    print(title, comment_list)


if __name__ == "__main__":

    urls = [
        "https://www.youtube.com/watch?v=g5Q7k6qMyyU",
        
    ]
    ScrapComment(urls[0])
