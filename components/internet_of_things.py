import json
import sys
from socket import AF_INET, SOCK_DGRAM, gethostname, socket
from subprocess import PIPE, Popen
from typing import Union
from urllib.request import urlopen

from speedtest import ConfigRetrievalError, Speedtest

from helper_functions.logger import logger
from peripherals.audio_output import say


def ip_info(phrase: str) -> None:
    """Gets IP address of the host machine.

    Args:
        phrase: Takes the spoken phrase an an argument and tells the public IP if requested.
    """
    if 'public' in phrase.lower():
        if not internet_checker():
            say(text="You are not connected to the internet sir!")
            return
        if ssid := get_ssid():
            ssid = f'for the connection {ssid} '
        else:
            ssid = ''
        if public_ip := json.load(urlopen('https://ipinfo.io/json')).get('ip'):
            output = f"My public IP {ssid}is {public_ip}"
        elif public_ip := json.loads(urlopen('http://ip.jsontest.com').read()).get('ip'):
            output = f"My public IP {ssid}is {public_ip}"
        else:
            output = 'I was unable to fetch the public IP sir!'
    else:
        ip_address = vpn_checker().split(':')[-1]
        output = f"My local IP address for {gethostname()} is {ip_address}"
    say(text=output)


def internet_checker() -> Union[Speedtest, bool]:
    """Uses speed test api to check for internet connection.

    Returns:
        ``Speedtest`` or bool:
        - On success, returns Speedtest module.
        - On failure, returns boolean False.
    """
    try:
        return Speedtest()
    except ConfigRetrievalError:
        return False


def get_ssid() -> str:
    """Gets SSID of the network connected.

    Returns:
        str:
        WiFi or Ethernet SSID.
    """
    process = Popen(
        ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'],
        stdout=PIPE)
    out, err = process.communicate()
    if error := process.returncode:
        logger.error(f"Failed to fetch SSID with exit code: {error}\n{err}")
    # noinspection PyTypeChecker
    return dict(map(str.strip, info.split(': ')) for info in out.decode('utf-8').splitlines()[:-1] if
                len(info.split()) == 2).get('SSID')


def vpn_checker() -> str:
    """Uses simple check on network id to see if it is connected to local host or not.

    Returns:
        str:
        Private IP address of host machine.
    """
    socket_ = socket(AF_INET, SOCK_DGRAM)
    socket_.connect(("8.8.8.8", 80))
    ip_address = socket_.getsockname()[0]
    socket_.close()
    if not (ip_address.startswith('192') | ip_address.startswith('127')):
        ip_address = 'VPN:' + ip_address
        info = json.load(urlopen('https://ipinfo.io/json'))
        sys.stdout.write(f"\rVPN connection is detected to {info.get('ip')} at {info.get('city')}, "
                         f"{info.get('region')} maintained by {info.get('org')}")
        say(text="You have your VPN turned on. Details on your screen sir! Please note that none of the home "
                 "integrations will work with VPN enabled.")
    return ip_address
