import ftplib
import os
import shutil
import time
import schedule
from datetime import date


def initiate_ftp_connection(url, username, password):
    ftp = ftplib.FTP(url)
    ftp.login(username,
              password)
    return ftp


def list_files_from_server(ftp):
    try:
        return ftp.nlst()
    except ftplib.error_perm as resp:
        if str(resp) == "550 No files found":
            log_to_file("No files in this directory")
        return []


def download_files_to_dir(ftp, path, filenames):
    try:
        for filename in filenames:
            ftp.retrbinary("RETR " + filename, open(os.path.join(path, filename), 'wb').write)
            log_to_file(f"downloaded file: {filename}")
    except ftplib.error_perm as resp:
        log_to_file(f"An error occoured while downloading files, the server returned: {resp}")


def move_files(source, destination):
    shutil.move(source, destination)
    log_to_file(f"Moved files from {source} to {destination}")


def create_downloaded_files_dir():
    cwd = os.getcwd()
    downloaded_files_dir = os.path.join(cwd, r'downloaded_files')
    if not os.path.exists(downloaded_files_dir):
        os.makedirs(downloaded_files_dir)
    return downloaded_files_dir


def automated_file_transfer():
    log_to_file("Started file transfer...")

    ftp = initiate_ftp_connection("ftp.dlptest.com", "dlpuser", "rNrKYTX9g7z3RgJRmxWuGHbeu")

    filenames = list_files_from_server(ftp)

    dowloaded_files_dir = create_downloaded_files_dir()

    download_files_to_dir(ftp, dowloaded_files_dir, filenames)

    move_files(dowloaded_files_dir, os.path.join(os.getcwd(), "destination_folder"))


def log_to_file(message):
    with open(f"log_{date.today()}", "a+") as log_file:
        log_file.write(message + '\n')


def main():
    schedule.every().day.at("19:49").do(automated_file_transfer)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main()
