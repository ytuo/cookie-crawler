from bs4 import BeautifulSoup
import pandas as pd
import argparse

def writeCookieFunction(cookie_rownum, file_name, df, dump_dir, csv_dest, update=True):
    try:
        soup = BeautifulSoup(open(dump_dir+"/"+file_name), features="html.parser")
        purpose = soup.select("#content-left > p:nth-child(3) > strong")[0].text
    except OSError as fe:
        raise
    except Exception as e:
        purpose = "N/A"

    df.purpose[cookie_rownum] = purpose

    if update:
        df.to_csv(csv_dest, index=False)

    return purpose

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cookie_rownum', nargs='?', default=0, type=int)
    parser.add_argument('--csv_path', '-csv', nargs='?', default='cookie_data.csv')
    parser.add_argument('--csv_dest_path', '-dest', nargs='?')
    parser.add_argument('--file_name', nargs='?', default=0, type=int)
    parser.add_argument('--dump_dir', '-dump', nargs='?', default='dump')
    parser.add_argument('--range_start', '-start', nargs='?', default=0, type=int) # inclusive, assumes first row of data is 2
    parser.add_argument('--range_end', '-end', nargs='?', type=int)             # exclusive
    parser.add_argument('--update_interval', '-i', nargs='?', default=10, type=int)
    parser.add_argument('--hide_errors', '-e', default=True, action='store_false') 

    args = parser.parse_args()

    # Load csv
    cookie_df = pd.read_csv(args.csv_path)
    cookie_df.index += 2        # adjust for df 0 indexing

    # Set up result output csv
    if args.csv_dest_path:
        save_path = args.csv_dest_path
    else:
        save_path = args.csv_path
        
    # Setup loop range
    range_start = args.range_start
    range_end = args.range_end
    if range_start < 2:
        range_start = 2
    if not range_end or range_end > len(cookie_df) + 2:
        range_end = len(cookie_df) + 2

    # Set up purpose column
    if not ("purpose" in cookie_df.columns):
        cookie_df["purpose"] = ""

    if args.cookie_rownum:      # Query specific cookie 
        try:
            purpose = writeCookieFunction(args.cookie_rownum, args.file_name, cookie_df, args.dump_dir, save_path)
            print(purpose)
        except Exception as e:
            if not args.hide_errors:
                print("error: " + str(e))
    else:               # Run on all cookies in csv
        for i in range(range_start, range_end):
            try:
                writeCookieFunction(i, "file"+str(i)+".html", cookie_df, args.dump_dir, save_path, i%args.update_interval == 0)
            except Exception as e:
                if not args.hide_errors:
                    print("Error on cookie " + str(i) + ": " + str(e))

        cookie_df.to_csv(save_path, index=False)

if __name__ == '__main__':
    main()