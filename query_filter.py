import re
from dataclasses import dataclass, field


@dataclass
class QueryFilter(object):
    ip_list: list
    reg_exp: str = ""
    filtered_ip_list: list = field(default_factory=list)

    def filter_ips(self):
        r = re.compile(self.reg_exp)
        self.filtered_ip_list = list(filter(r.match, self.ip_list))

    def get_filtered_ips(self):
        return self.filtered_ip_list
