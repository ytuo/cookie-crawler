import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chrome_path', nargs='?', default='/usr/bin/chromedriver')
    parser.add_argument('--csv_path', '-csv', nargs='?', default='cookie_data.csv')
    # csv contents will be copied to dest file after at least one run with the original csv
    # So use destination csv as the original csv_path after one run to avoid column being overwritten
    parser.add_argument('--csv_dest_path', '-dest', nargs='?')
    parser.add_argument('--range_start', '-start', nargs='?', default=0, type=int) # inclusive, assumes first row of data is 2
    parser.add_argument('--range_end', '-end', nargs='?', type=int) # exclusive
    parser.add_argument('--update_interval', '-i', nargs='?', default=10, type=int)
    parser.add_argument('--hide_errors', '-e', default=True, action='store_false') 


    args = parser.parse_args()

    # Create new instance of Chrome in incognito mode
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path=args.chrome_path, chrome_options=option)

    # Load csv
    cookie_df = pd.read_csv(args.csv_path)
    cookie_df.index += 2        # adjust for df 0 indexing

    # Set up result output csv
    if args.csv_dest_path:
        save_path = args.csv_dest_path
    else:
        save_path = args.csv_path

    # Set up purpose column
    if not ("purpose" in cookie_df.columns):
        cookie_df["purpose"] = ""

    # Set up range
    range_start = args.range_start
    range_end = args.range_end
    if range_start < 2:
        range_start = 2
    if not range_end or range_end > len(cookie_df) + 2:
        range_end = len(cookie_df) + 2

    cookies_seen = set()

    for i in range(range_start, range_end):
        try:
            cookie_name = cookie_df["cookie_name"][i]

            if cookie_name in cookies_seen:
                continue

            cookies_seen.add(cookie_name)
            # Query url
            driver.get("https://cookiepedia.co.uk/cookies/" + cookie_name)
            que = driver.find_element_by_xpath('//div[@id="content-left"]/p/strong')

            cookie_df.purpose[i] = que.text

            # Save to csv backup frequency
            if i % args.update_interval == 0:
                cookie_df.to_csv(save_path, index=False)
                # print(i)      # Debug
        except Exception as e:
            if not args.hide_errors:
                print("Error on cookie " + str(i) + ": " + str(e))

    # Save results
    cookie_df.to_csv(save_path, index=False)
    print("done")


if __name__ == '__main__':
    main()

