from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def iframes(driver):
    for iframe in driver.find_elements(By.CSS_SELECTOR, 'iframe'):
        driver.switch_to.frame(iframe)
        yield iframe
        yield from iframes(driver)
        driver.switch_to.parent_frame()
    driver.switch_to.default_content()

    
def close_ad_(driver, element='#pclose-btn'):
    driver.find_element(By.CSS_SELECTOR, element).click()
    print('ad blocked')


def close_ad(driver, element='#pclose-btn'):
    try:
        close_ad_(driver, element)
        return
    except NoSuchElementException:
        pass
    
    for _ in iframes(driver):
        try:
            close_ad_(driver, element)
            break
        except NoSuchElementException:
            pass
    driver.switch_to.default_content()


def get_article_info(node):
    a = node.find_element(By.XPATH, './ancestor::a[position() = 1]')
    url = a.get_attribute('href')
    title = node.text
    row = node.find_element(By.XPATH, './ancestor::*[contains(concat(" ", normalize-space(@class), " "), " queryly_item_row ")][position() = 1]')
    subtitle_node = row.find_element(By.CSS_SELECTOR, '.queryly_item_description')
    subtitle = subtitle_node.text

    return {
        'url': url,
        'title': title,
        'subtitle': subtitle
    }

def get_articles(driver):
    return [
        get_article_info(node) for node in
        driver.find_elements(By.CSS_SELECTOR, '.queryly_item_title')
    ]
