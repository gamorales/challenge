import requests
import json
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor


@dataclass
class LookupIP(object):
    ip_list: list
    type_lookup: str = "geoip"
    important_keys = [
            "ip", "country_code", "country_name", "region_code", "region_name",
            "city", "zip_code", "time_zone", "latitude", "longitude",
            "metro_code"
    ]

    def get_important_keys(self, response):
        """ Extract just a few keys from endpoints response"""

        for record in response:
            resp = json.loads(record)
            print(json.dumps(
                dict((k, resp[k]) for k in self.important_keys if k in resp),
                indent=4, sort_keys=True
            ))

    def check_ip_list(self):
        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.map(self.check_ip, self.ip_list)

        #return list(map(self.check_ip, self.ip_list))

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
