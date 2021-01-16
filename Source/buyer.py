import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# manages needed libraries


def setup(driver):  # logs into the website and configures settings

    driver.get("https://rolimons.com/deals")
    time.sleep(3)

    buttons = driver.find_elements_by_class_name("dropdown-item")
    # finds the button for the dropdown item

    driver.find_element_by_id("filter-category-dropdown").click()
    time.sleep(1)

    for button in buttons:  # iterates through each button
        if button.get_attribute("data-category") == "filter_below_30_percent":  # clicks the dropdown to filter only items with a 30% deal
            button.click()
    
    return driver


def buy_item(link, driver):  # goes to the Roblox page where the item is beign sold and purchases it
    try:
        driver.get(link)

        driver.find_element_by_class_name("btn-fixed-width-lg").click()
        driver.implicitly_wait(10)
        # clicks initial buy button

        driver.find_element_by_id("confirm-btn").click()
        driver.implicitly_wait(10)
        # confirms purchase

        time.sleep(3)
    except:
        pass


def get_driver():  # creates web driver
    
    options_driver = Options()
    options_driver.add_argument("--log-level=3")
    # defines extra driver options

    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options_driver)
    # creates the web driver

    return driver


used_links = []

driver = get_driver()
driver.get("https://roblox.com/login")
# goes to Roblox login page

input("Please log into Roblox.  Click ENTER to continue... ")
# wats for user to log in to Roblox

driver = setup(driver)
counter = 0
# sets up the driver and page

while True:
    try:
        if counter == 30:  # reloads the page every interval
            driver = setup(driver)
            counter = 0

        deals = driver.find_elements_by_xpath("//a[@href]")

        for deal in deals:  # iterates through page links
            try:
                deal = deal.get_attribute("href")

                if "roblox.com" in deal and deal not in used_links:  # if links are to Roblox items, go there
                    buy_item(deal, driver)
                    used_links.append(deal)
                    # buys item and stores link

                    driver = setup(driver)
                    # sets up the driver and page

            except:
                pass
        
        time.sleep(5)
        counter += 1
        # wait a few seconds before continuing

    except:
        pass