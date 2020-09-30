import re
from dataclasses import dataclass, field


@dataclass
class LoadIPFile(object):
    filename: str
    ip_list: list = field(default_factory=list)

    def read_ip_list(self):
        try:
            with open(self.filename) as f:
                data = f.readlines()

            regex = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
            for line in data:
                matches = regex.findall(line.strip())
                for match in matches:
                    self.ip_list.append(match)

        except FileNotFoundError:
            self.ip_list = []

    def get_ip_list(self):
        return self.ip_list


if __name__ == "__main__":
    ips = LoadIPFile("./list_of_ips.txt")
    ips.read_ip_list()

    if not ips.get_ip_list():
        print("No data")
    else:
        print(ips.get_ip_list())
        print(len(ips.get_ip_list()))
