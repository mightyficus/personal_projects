###
# Tutorial from NeuralNine @ https://www.youtube.com/watch?v=SPM1tm2ZdK4
# Get the amazon price of a specific book linked on a website
#
# For testing xpath queries, go to xpather.com
###

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Leaves Browser open even if script has concluded
options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options = options)

# Open browser and navigate to https://neuralnine.com
driver.get("https://www.neuralnine.com")
driver.maximize_window()

# get all anchor tags on current page
links = driver.find_elements("xpath", "//a[@href]")

# iterate through links and click on the one that contains "Books"
for link in links:
    if "Books" in link.get_attribute("innerHTML"):
        link.click()
        break

'''
xpath breakdown
"//div                                          look for a div container
[                                               that meets the following condition
contains(@class, 'elementor-column-wrap')       contains a class called 'elementor-column-wrap'
]
[                                               If it meets that condition, then filter by
.//h2                                           Any child headers
[                                               That meet the condition               
text()[contains(., '7 IN 1)                     The text of the object (header) itself (.) contains the string '7 IN 1'
]
]
#                                               We know that the div container we want only has two links, so we can further filter by that
[                                               The object returned by the last expression (div container) must meet the following condition
count(.//a)=2                                   count of all the anchor tags as children must = 2
]
//a                                             object returns the anchor tags
"
''' 

book_links = driver.find_elements("xpath",
                                  "//div[contains(@class, 'elementor-column-wrap')][.//h2[text()[contains(., '7 IN 1')]]][count(.//a)=2]//a")

for book in book_links:
    print(book.get_attribute("href"))


# after this it dowsn't really work, because amazon forces a captcha if it detects selenium. But the theory will apply to other websites
book_links[0].click()

# switch to new tab
driver.switch_to.window(driver.window_handles[1])

time.sleep(3)

'''
xpath breakdown
//a                                             get all of the anchor tags
[                                               which meet the following condition
.//span                                         has at least one child span tag
[                                               which meets the following condition
text()[contains(., 'Paperback')]                the object (span) itself (.) contains the text 'Paperback
]
]
//span                                          from these anchor tags, we want the span elements
[                                               which meet the following condition
text()[contains(., '$')]                        The text of the object (span) itself (.) contains the string '$'
]
'''

buttons = driver.find_elements("xpath", "//a[.//span[text()[contains(., 'Paperback')]]]//span[text()[contains(., '$')]]")

for button in buttons:
    print(button.get_attribute('innerHTML'))