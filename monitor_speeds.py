import speedtest
import pandas as pd
from datetime import datetime
import time


def get_measurements():
    speed_test = speedtest.Speedtest()
    try:
        best_server_json = speed_test.get_best_server()
    except Exception as e:
        return (0, 0, 0, 0, 0)

    # Get connection parameters
    sponsor = best_server_json.get("sponsor")
    host_address = best_server_json.get("host")
    
    # Get download and upload from speedtest
    download = speed_test.download()
    upload = speed_test.upload()
    # Get ping
    ping = speed_test.results.ping

    download_mbs = round(download / (10**6), 2)
    upload_mbs = round(upload / (10**6), 2)
    return ping, download_mbs, upload_mbs, sponsor, host_address


def update_csv(internet_speeds):
    # Get today's date in the form Month/Day/Year
    date_today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    file_name = "connection_monitor_log.csv"
    try:
        # Try to open, otherwise create new csv.
        csv_dataset = pd.read_csv(file_name, index_col="Date")
    except:
        csv_dataset = pd.DataFrame(
            list(),
            columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)", "Sponsor (DC)", "Endpoint"]
        )

    # Add our results to df
    results_df = pd.DataFrame(
        [[ internet_speeds[0], internet_speeds[1], internet_speeds[2], internet_speeds[3], internet_speeds[4]]],
        columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)", "Sponsor (DC)", "Endpoint"],
        index=[date_today]
    )

    new_df = csv_dataset.append(results_df, sort=False)
    new_df.to_csv(file_name, index_label="Date")


if __name__ == '__main__':
    UPDATE_INTERVAL_MIN = 5
    counter = 0
    while True:
        time_now = datetime.now().strftime("%H:%M:%S")
        counter += 1
        print(f"[{time_now}] Starting iteration number {counter}")
        new_speeds = get_measurements()
        print(f"Got results, Download:{new_speeds[1]}, Upload: {new_speeds[2]}")
        update_csv(new_speeds)
        print(f"Sleeping for {UPDATE_INTERVAL_MIN} minutes")
        time.sleep(60 * UPDATE_INTERVAL_MIN)
