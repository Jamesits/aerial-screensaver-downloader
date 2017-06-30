from __future__ import print_function
import requests
import sys
import os

proxies = {}
# you may need:
# proxies = {
#   'http': 'http://localhost:1080',
#   'https': 'http://localhost:1080',
# }
headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
)


def download_file(url, local_filename):
    r = requests.get(url, headers=headers, stream=True, proxies=proxies)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


print("Fetching metadata")
metadata = requests.get(
    "https://s1.mzstatic.com/us/r1000/000/Features/atv/AutumnResources/videos/entries.json", headers=headers, proxies=proxies).json()
for entry in metadata:
    for video in entry['assets']:
        url = video['url']
        filename = url.split('/')[-1]
        print("Downloading {}...".format(video['url']), end='')
        sys.stdout.flush()
        try:
            if os.path.isfile(filename):
                print("SKIP")
            else:
                download_file(url, filename + ".download")
                os.rename(filename + ".download", filename)
                print("OK")
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception as e:
            print(e)
