from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

#################################################################################################""""
#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

The soundfile module (https://python-soundfile.readthedocs.io/)
has to be installed!

"""
import argparse
import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)

q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def recorder():
    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])
        if args.filename is None:
            args.filename = titre +".wav"

        # Make sure the file is opened before recording anything:
        with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                        channels=args.channels, subtype=args.subtype) as file:
            with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                channels=args.channels, callback=callback):
                print('#' * 80)
                print('press Ctrl+C to stop the recording')
                print('#' * 80)
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(args.filename))
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
###########################################################################        
driver_path = "C:\Temp\chromedriver_win32\\chromedriver.exe"
brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

option = webdriver.ChromeOptions()
option.binary_location = brave_path

chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")

#option.add_experimental_option("ask_widevine_install", "false")
driver = webdriver.Chrome(executable_path=driver_path, options=option)

driver.get("https://accounts.spotify.com/fr/login?continue=https%3A%2F%2Fopen.spotify.com%2F")
driver.find_element(By.ID, 'login-username').send_keys("")
password = driver.find_element(By.ID, 'login-password').send_keys("")
submit = driver.find_element(By.ID, 'login-button').click()
# cookies = driver.get_cookies()
# print(cookies)
time.sleep(10)
driver.get("https://open.spotify.com/collection/tracks")
time.sleep(20)
print("attend encre un peu")
submitc = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/button').click()
# body = driver.find_element(By.ID, "passwd-id")
# body.send_keys(" and some", Keys.ARROW_DOWN)

time.sleep(2)

html = driver.page_source
titre0 = html.split("<title>")
titreb = titre0[1].split("</title>")
# print(titre0[1])
titre = titreb[0]
print(titre)
# print(type)
print('#' * 80)
temps0=html.split('aria-valuetext="')
temps1=(temps0[1]).split("/")
temps2=(temps1[1]).split('"')
debut0 = temps1[0].split(':')
debut =  int(debut0[0])*60 + int(debut0[1])
print('début=',debut)
fin0 = temps2[0].split(':')
fin = int(fin0[0])*60 + int(fin0[1])
print('fin=',fin)
tempsattente = fin - debut
print('tempsattente=',tempsattente)

import schedule
import time
import datetime

schedule.every(5).seconds.do(recorder())
