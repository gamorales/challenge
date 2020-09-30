import requests
import json
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor


@dataclass
class LookupIP(object):
    ip_list: list
    type_lookup: str = "geoip"
    start: int = 0
    end: int = 0

    def check_ip_list(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            if self.end > 0 and self.start >= 0:
                executor.map(
                    self.check_ip,
                    self.ip_list[self.start:self.end]
                )
            else:
                executor.map(self.check_ip, self.ip_list)

    def check_ip(self, ip):
        """ Consume endpoints for GeoIP and RDAP"""
        if "geoip" in self.type_lookup:
            url = f"https://freegeoip.app/json/{ip}"
        else:
            url = f"https://rdap.lacnic.net/rdap/ip/{ip}"

        resp = requests.get(url)

        if resp.status_code == 200:
            data = resp.json()
            print(json.dumps(data, indent=4, sort_keys=True))
        else:
            print(f"IP address {ip} is not ok!")
