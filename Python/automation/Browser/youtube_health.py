'''
Get youtube health stats using selenium + xpath
Currently, I'm using the "Stats for nerds" info that is visible by right-clicking the video 
and selecting "Stats for nerds". This gives me a bunch of info, including Connection Speed (in Kbps),
Network Activity (in KB), and Buffer Health (in seconds). I'll check the buffer health against the
time left in the video (using duration of the video and current time).

These might be available even if the "stats for nerds
Static video (non-livestream):
<span class="ytp-time-current">xx:xx</span>             Current timestamp, exists in live, but hidden
<span class="ytp-time-duration">xx:xx</span>            Duration of video, exists in live, but hidden

Right-click video -> "Stats for nerds"
<div class="html5-video-info-panel ytp-sfn" data-layer="4">
    <div class="html5-video-info-panel-content ytp-sfn-content">
        <div style>
            <div>Connection Speed</div>
            <span>
                <span> XXXX Kbps</span>                 Connection Speed, also in live
            </span>
        </div>
        <div style>
            <div>Network Activity</div>
            <span>
                <span> XXXX KB</span>                   Network Activity, also in live, but not useful info
            </span>
        </div>
        <div>
            <div>Buffer Health</div>
            <span>
                <span> XX.XX s</span>                   Buffer Health, also in live
            </span>
        </div>
        <div style>
            <div>Live Latency</div>
            <span>
                <span> xx:xxs</span>                    Live Latency
            </span>
        </div>
        
<button class="ytp-live-badge ytp-button" disabled>     Indicates video is live
 ::before
 "Live"
</button>
'''

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
# sets the driver to wait at least 10s for an element to be found before returning an error
# Known as an "implicit" wait
#driver.implicitly_wait(10)

# Can also use an "explicit wait", which polls the website for x amount of seconds or until an element is available
# If the element is not found before the timeout, the program will return an error
errors = [NoSuchElementException, ElementNotInteractableException]
wait = WebDriverWait(driver, 25, ignored_exceptions=errors)

url = "https://www.youtube.com/watch?v=p8M7FTVVn70"

driver.get(url)
driver.maximize_window()

'''
//button[@class='ytp-large-play-button ytp-button]
'''

# starts playing the current video by clicking on following element:
# <button class="ytp-large-play-button ytp-button"...>
play_button = driver.find_element('xpath', '//button[@class="ytp-large-play-button ytp-button"]')
ActionChains(driver).click(play_button).perform()

# Open Stats for nerds popup for video info
# It looks like once this pop-up is opened, the stats can always be retreived, even if the pop-up isn't visible
video_player = driver.find_element('xpath', '//div[contains(@class, "html5-video-player")]')
ActionChains(driver).context_click(video_player).perform()
stats_for_nerds = driver.find_element('xpath', '//div[contains(text(), "Stats for nerds")]')
ActionChains(driver).click(stats_for_nerds).perform()

# Need to check if an ad is playing, and wait until the ad is over or skip it.
# It's probably possible to click the "skip" button once it shows up, but the button doesn't show up immediately,
# and not all ads will have the "skip" button, so it will probably be better to wait until the ad  goes away. We're not in a rush.
# We should be able to check if an ad is playing by looking for this element:

# Check if an ad is playing by checking if this element exists:
# <div class="ytp-ad-player-overlay-layout" id="player-overlay-layout:t" style>
# This element should exist even if the skip button doesn't
# Then wait until the skip button appears, and press it
try:
    driver.find_element('xpath', '//div[@class="ytp-ad-player-overlay-layout"]')
    print("Ad is currently playing")
    skip_button = driver.find_element('xpath', '//button[@class="ytp-skip-ad-button"]')
    print("Found skip button")
    wait.until(lambda d: skip_button.is_displayed())
    ActionChains(driver).click(skip_button).perform()
    
except NoSuchElementException as e:
        print(f"No ad playing, or error: {str(e).split('\n')[0]}")

# Live video logic
# wait until the latency stat comes up
wait.until(lambda d: driver.find_element('xpath', '//div[text()[contains(., "Live Latency")]]').is_displayed())
latency = driver.find_element('xpath', '//div[text()[contains(., "Live Latency")]]/..//span[text()[contains(., "s")]]')
buffer_health = driver.find_element('xpath', '//div[text()[contains(., "Buffer Health")]]/..//span[text()[contains(., "s")]]')

# Gather video quality data for live stream
time.sleep(5)
latency_stats = []
buffer_health_stats = []
# eventually we'll turn this into a while loop that catches an early termination error, outputs the stats, and exits
for i in range(10):
    print(f"Current Latency: {latency.get_attribute('innerHTML')[:-1]}s, Current Buffer Health: {buffer_health.get_attribute('innerHTML')[:-2]}s")
    
    # If latency or buffer health == 0, it probably just hasn't started recording
    if float(latency.get_attribute('innerHTML')[:-1]) == 0 or float(buffer_health.get_attribute('innerHTML')[:-2]) == 0:
        print("Buffer health or Latency is 0s, skipping...")
    else:
        latency_stats.append(float(latency.get_attribute('innerHTML')[:-1]))
        buffer_health_stats.append(float(buffer_health.get_attribute('innerHTML')[:-2]))

    time.sleep(1)
   
# Print stats
print()
print('----------------------------------')
print(f"Average Latency: {sum(latency_stats)/len(latency_stats):.2f}s")
print(f"Latency Min/Max: {min(latency_stats):.2f}s/{max(latency_stats):.2f}s")
print()
print(f"Average Buffer Health: {sum(buffer_health_stats)/len(buffer_health_stats):.2f}s")
print(f"Buffer Health Min/Max: {min(buffer_health_stats):.2f}s/{max(buffer_health_stats):.2f}s")

# current_latency = driver.find_element('xpath', '//div[@class="html5-video-info-panel-content ytp-sfn-content"]//div[12]//div[1]')
# print(current_latency.get_attribute('innerHTML'))