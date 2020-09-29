import re
from dataclasses import dataclass


@dataclass
class LoadIPFile(object):
    filename: str = ""

    def get_ip_list(self):
        try:
            with open(self.filename) as f:
                data = f.readlines()

            ip_list = []
            regex = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")

            for line in data:
                matches = regex.findall(line.strip())
                for match in matches:
                    ip_list.append(match)

            return ip_list
        except FileNotFoundError:
            return False


if __name__ == "__main__":
    ips = LoadIPFile("./list_of_ips.txt")
    lista = ips.get_ip_list()
    print(lista)
