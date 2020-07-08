import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chrome_path', nargs='?', default='/usr/bin/chromedriver')
    parser.add_argument('--csv_path', '-csv', nargs='?', default='cookie_data.csv')
    parser.add_argument('--dump_dir', '-dump', nargs='?', default='dump')
    parser.add_argument('--range_start', '-start', nargs='?', default=0, type=int) # inclusive, assumes first row of data is 2
    parser.add_argument('--range_end', '-end', nargs='?', type=int)     # exclusive
    parser.add_argument('--hide_errors', '-e', default=True, action='store_false') 


    args = parser.parse_args()

    # Create new instance of Chrome in incognito mode
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path=args.chrome_path, chrome_options=option)

    # Create dump subfolder
    dump_dir = args.dump_dir
    os.makedirs(dump_dir, exist_ok=True)

    # Load csv
    cookie_df = pd.read_csv(args.csv_path)
    cookie_df.index += 2        # adjust for df 0 indexing

    range_start = args.range_start
    range_end = args.range_end
    if range_start < 2:
        range_start = 2
    if not range_end or range_end > len(cookie_df) + 2:
        range_end = len(cookie_df) + 2

    for i in range(range_start, range_end):
        try:
            cookie_name = cookie_df["cookie_name"][i]
            # print(cookie_name)    # Debug

            # Query cookiepedia with cookie name
            driver.get("https://cookiepedia.co.uk/cookies/" + cookie_name)

            # Save html to file in dump subfolder
            html = driver.page_source
            cur_file = open(dump_dir+"/file"+str(i)+".html", "w")
            cur_file.write(html)
            cur_file.close()

        except Exception as e:
            if not args.hide_errors:
                print("Error on cookie " + str(i) + ": " + str(e))

    print("done")


if __name__ == '__main__':
    main()




























# # import csv

# # with open('cookie_data.csv', newline='') as csvfile:
# # 	cookies = csv.reader(csvfile, delimiter=' ', quotechar='|')
# # 	print(cookies[0])


# import pandas as pd
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# cookie_df = pd.read_csv('cookie_data.csv')
# # i=0
# # print("cookie policy" + cookie_df["cookie_name"][i] + " " + cookie_df["cookie_domain"][i])


# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import os

# option = webdriver.ChromeOptions()
# option.add_argument("--incognito")
# # option.add_argument('headless')

# # # # option.add_argument("--no-startup-window")

# # Create new Instance of Chrome in incognito mode
# driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=option)

# # Go to desired website
# driver.get("http://www.google.com")


# que=driver.find_element_by_xpath("//input[@name='q']")
# # que.send_keys("cookie policy cnn")
# i = 0
# que.send_keys("cookie policy" + cookie_df["cookie_name"][i] + " " + cookie_df["cookie_domain"][i])
# que.send_keys(Keys.RETURN)

# # # https://stackoverflow.com/questions/19225173/how-to-click-on-the-first-result-on-google-using-selenium-python
# # result = driver.find_elements_by_xpath('//ol[@id="rso"]/li')[0]  # make a list of results and get the first one
# # result.find_element_by_xpath("./div/h3/a").click() # click its href

# results = driver.find_elements_by_xpath('//div[@class="r"]/a/h3')  # finds webresults
# results[1].click() # clicks the first one


# timeout = 20
# try:
#     # Wait until the final element [Avatar link] is loaded.
#     # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
#     # the last things to be loaded.
#     WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='sliding-popup']")))
# except TimeoutException:
#     print("Timed out waiting for page to load")
#     driver.quit()


# text = driver.find_elements_by_tag_name("a href")
# for item in text:
# 	print(item)
# 	if "cookie" in item.get_attribute("innerText").lower():
# 		print("here")
# 		item.click()
# 		continue


# print("done")


