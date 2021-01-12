import time
import instaloader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from instaloader.exceptions import BadCredentialsException
from selenium.webdriver.support import expected_conditions as EC


def get_non_following_back(username, password):
    insta = instaloader.Instaloader()

    try:
        insta.login(username, password)
    except BadCredentialsException:
        print("Bad  Credentials.")
        exit()

    print("Logged in to instaLoader.")

    profile = instaloader.Profile.from_username(insta.context, username)

    excludes = open('./excludes.txt').read().splitlines()
    followers = []
    followings = []
    non_following_back = []

    for follower in profile.get_followers():
        followers.append(follower.username)

    for following in profile.get_followees():
        followings.append(following.username)

    for following in followings:
        if following not in followers and following not in excludes:
            non_following_back.append(following)

    return non_following_back


# Every element which is found by xpath may change in the future
def unfollow(insta_username, insta_pass, non_following_back):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)

    driver.get('https://www.instagram.com/accounts/login/')
    dom = driver.find_element_by_xpath('//*')
    wait = WebDriverWait(driver, 15)

    wait.until(EC.presence_of_element_located((By.NAME, 'username')))

    username = dom.find_element_by_name('username')
    password = dom.find_element_by_name('password')
    login_button = dom.find_element_by_xpath('//*[@class="sqdOP  L3NKy   y3zKF     "]')

    username.clear()
    password.clear()

    username.send_keys(insta_username)
    password.send_keys(insta_pass)

    login_button.click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'logged-in')))

    print("Logged in to instagram.")

    for nonFollowing in non_following_back:
        founded_unfollow = False

        driver.get(f"https://www.instagram.com/{nonFollowing}/")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]')))

        while not founded_unfollow:
            try:
                driver.find_element_by_xpath('//*[@class="_5f5mN    -fzfL     _6VtSN     yZn4P   "]').click()
                founded_unfollow = True
            except StaleElementReferenceException:
                pass

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="aOOlW -Cab_   "]')))

        driver.find_element_by_xpath('//*[@class="aOOlW -Cab_   "]').click()

        print(f"Unfollowed: {nonFollowing}.")

        # Set to 30 so instagram won't recognize it's a bot, but you can toy around with this as much as you like.
        # I'm not responsible if you get banned ¯\_(ツ)_/¯

        time.sleep(30)

    driver.close()
    print("Finished Unfollowing.")


def main():
    insta_username = input("Enter username:")
    insta_pass = input("Enter password:")

    non_following_back = get_non_following_back(insta_username, insta_pass)
    unfollow(insta_username, insta_pass, non_following_back);


if __name__ == '__main__':
    main()
