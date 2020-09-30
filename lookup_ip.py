import requests
import json
from dataclasses import dataclass


@dataclass
class LookupIP(object):
    ip: str
    type_lookup: str = "geoip"
    important_keys = [
            "ip", "country_code", "country_name", "region_code", "region_name",
            "city", "zip_code", "time_zone", "latitude", "longitude",
            "metro_code"
    ]

    def get_important_keys(self, response):
        """ Extract just a few keys from endpoints response"""

        resp = json.loads(response)
        return json.dumps(
                dict((k, resp[k]) for k in self.important_keys if k in resp),
                indent=4, sort_keys=True
        )

    def check_ip(self):
        """ Consume endpoints for GeoIP and RDAP"""

        if "geoip" in self.type_lookup:
            url = f"https://freegeoip.app/json/{self.ip}"
        else:
            url = f"https://rdap.lacnic.net/rdap/ip/{self.ip}"

        resp = requests.get(url)

        if resp.status_code == 200:
            data = resp.json()
            return json.dumps(data, indent=4, sort_keys=True)
        else:
            return f"IP address {self.ip} is not real"
