import re
from dataclasses import dataclass, field


@dataclass
class LoadIPFile(object):
    filename: str
    ip_list: list = field(init=False)

    def __post_init__(self):
        self.ip_list = self.read_ip_list()

    def read_ip_list(self):
        try:
            with open(self.filename) as f:
                data = f.readlines()

            regex = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
            ip_list = []
            for line in data:
                matches = regex.findall(line.strip())
                for match in matches:
                    ip_list.append(match)

            return ip_list
        except FileNotFoundError:
            return False

    def get_ip_list(self):
        return self.ip_list


if __name__ == "__main__":
    ips = LoadIPFile("./ist_of_ips.txt")

    if not ips.get_ip_list():
        print("No data")
    else:
        print(ips.get_ip_list())
        print(len(ips.get_ip_list()))
