import requests
import json
from dataclasses import dataclass

# https://freegeoip.app/json/181.234.128.130


@dataclass
class GeoIP(object):
    ip: str

    def check_geoip(self):
        url = f"https://freegeoip.app/json/{self.ip}"
        resp = requests.get(url)

        if resp.status_code == 200:
            data = resp.json()
            return json.dumps(data, indent=4, sort_keys=True)
        else:
            return f"IP address {self.ip} is not real"
