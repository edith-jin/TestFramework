from selenium import webdriver


def open_browser(tag='Chrome'):
    driver = getattr(webdriver, tag)
    return driver