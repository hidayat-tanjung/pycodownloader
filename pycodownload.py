import os
import time
import argparse
import requests
from colorama import Fore
print(Fore.BLUE)
banner = """

██████╗ ██╗   ██╗ ██████╗ ██████╗ ██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ 
██╔══██╗╚██╗ ██╔╝██╔════╝██╔═══██╗██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗
██████╔╝ ╚████╔╝ ██║     ██║   ██║██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║
██╔═══╝   ╚██╔╝  ██║     ██║   ██║██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║
██║        ██║   ╚██████╗╚██████╔╝██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝
╚═╝        ╚═╝    ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                                                                                                                                              
     [!] PycoDownload
     [!] By : X3NUX
     [!] Youtube: LINUXPLOITER
     [!] www.linuxploiter.com
"""
print(banner)
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class DownloadManager:
    def __init__(self, url, dest_path, chunk_size=8192, retries=3, backoff_factor=0.5):
        self.url = url
        self.dest_path = dest_path
        self.chunk_size = chunk_size
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.session = requests.Session()
        self.retry = Retry(total=self.retries, backoff_factor=self.backoff_factor, status_forcelist=[500, 502, 503, 504])
        self.session.mount('http://', HTTPAdapter(max_retries=self.retry))
        self.session.mount('https://', HTTPAdapter(max_retries=self.retry))

        if os.path.exists(self.dest_path) and os.path.getsize(self.dest_path) > 0:
            self.downloaded_size = os.path.getsize(self.dest_path)
        else:
            self.downloaded_size = 0

    def download(self):
        headers = {
            'Range': f'bytes={self.downloaded_size}-' if self.downloaded_size > 0 else None,
        }

        response = self.session.get(self.url, headers=headers, stream=True)

        if response.status_code == 200:
            with open(self.dest_path, 'ab') as f:
                for chunk in response.iter_content(self.chunk_size):
                    f.write(chunk)
                    self.downloaded_size += len(chunk)

        elif response.status_code == 206:  # Partial Content
            with open(self.dest_path, 'ab') as f:
                for chunk in response.iter_content(self.chunk_size):
                    f.write(chunk)
                    self.downloaded_size += len(chunk)

        else:
            print(f'Failed to download the file. Status code: {response.status_code}')
            return False

        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple download manager.')
    parser.add_argument('url', help='The URL of the file to download.')
    parser.add_argument('dest_path', help='The destination path of the downloaded file.')
    args = parser.parse_args()

    download_manager = DownloadManager(args.url, args.dest_path)

    if download_manager.download():
        print('Download completed.')
    else:
        print('Download failed.')