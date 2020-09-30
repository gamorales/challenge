import re
from dataclasses import dataclass, field

from dialog import ShowMessageDialog
from load_file import LoadIPFile
from query_filter import QueryFilter
from lookup_ip import LookupIP

# Number of parameters per function
PARAMS_QTY = {
        "load": 1,
        "find": 1,
        "rdap": 1,
        "geoip": 1,
}


@dataclass
class Commands(object):
    command: str
    params: list
    data: list = field(default_factory=list)
    filtered_data: dict = field(default_factory=dict)

    def validate_params_qty(self, command, params_qty, valid_qty):
        """ Check if params quantity is ok """

        if params_qty != valid_qty:
            return False

        return True

    @staticmethod
    def print_help():
        message = """
        load <file>: Load file into memory.
        print [<var>]: Print a list with IPs in memory.
        geoip [<ip> | <range> | all]: Geo-location lookup tool. Ej: range(0:10)
        rdap [<ip> | <range> | all]: Registration data access search for IP. Ej: range(0:10)
        find <regex:ip>: A regex query to search IP addresses. Ej: find .*50
        help: Prints help dialog.
        exit: Exit.
        """
        print(message)

    def get_lookup_data(self, response):
        """ Get information from RDAP and GeoIP webpages """
        if self.params[0] == "all":
            if response.get("data", []):
                lookup_ip = LookupIP(
                    response.get("data", []),
                    self.command
                )
            else:
                return False
        elif self.params[0].startswith("range"):
            if response.get("data", []):
                range_found = re.search('\((.+?)\)', self.params[0])
                if range_found:
                    range_list = range_found.group(1).split(":")

                    if len(range_list) > 1:
                        lookup_ip = LookupIP(
                            response.get("data", []),
                            self.command,
                            start=int(range_list[0]),
                            end=int(range_list[1])
                        )
                    else:
                        lookup_ip = LookupIP(
                            response.get("data", []),
                            self.command,
                            start=0,
                            end=int(range_list[0])
                        )
            else:
                return False
        else:
            lookup_ip = LookupIP([self.params[0]], self.command)

        return lookup_ip

    def run_command(self, response, filtered={}):
        """ Run commands """

        qty = PARAMS_QTY.get(self.command, 0)
        if qty == 0:
            message = "Invalid command!"
        else:
            params_qty = self.validate_params_qty(
                self.command,
                len(self.params),
                qty
            )
            if params_qty:
                if self.command == "load":
                    reader = LoadIPFile(self.params[0])
                    reader.read_ip_list()
                    self.data = reader.get_ip_list()
                    if not self.data:
                        message = "No data has been loaded!"
                    else:
                        message = f"{len(self.data)} IP addresses has been loaded!"
                elif self.command == "find":
                    self.filtered_data = filtered

                    filtered_ips = QueryFilter(
                        response.get("data", []),
                        self.params[0]
                    )
                    filtered_ips.filter_ips()
                    self.filtered_data[f"a{len(self.filtered_data)+1}"] = filtered_ips.get_filtered_ips()

                    message = f"Filtered data in var A{len(self.filtered_data)}"
                    self.data = response.get("data", [])

                elif self.command in ["geoip", "rdap"]:
                    lookup_ip = self.get_lookup_data(response)

                    if lookup_ip:
                        lookup_ip.check_ip_list()
                        self.data = response.get("data", [])

                        message = "IPs has been consulted!"
                    else:
                        message = "No data has been loaded!"

            else:
                message = f"Invalid syntax for command <{self.command}>.\n"
                message += "Type help for more info."

        return {
            "msg": message,
            "data": self.data,
            "filter": self.filtered_data
        }
