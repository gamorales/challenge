import json
import csv
import yaml
import re
from dataclasses import dataclass, field

from dialog import ShowMessageDialog
from load_file import LoadIPFile
from query_filter import QueryFilter
from lookup_ip import LookupIP

# Number of parameters per function
PARAMS_QTY = {
    "load": [1],
    "filter": [1],
    "rdap": [1, 2],
    "geoip": [1, 2],
    "save": [4]
}


@dataclass
class Commands(object):
    command: str
    params: list
    data: list = field(default_factory=list)
    filtered_data: dict = field(default_factory=dict)

    def validate_params_qty(self, command, params_qty, valid_qty):
        """ Check if params quantity is ok """

        if params_qty in valid_qty:
            return True

        return False

    @staticmethod
    def print_help():
        message = """
        load <file>: Load file into memory.
        print [<var>]: Print a list with IPs in memory.
        geoip [<ip> | <range> [<var>] | all]: Geo-location lookup tool. e.g.: range(0:10)
        rdap [<ip> | <range> [<var>] | all]: Registration data access search for IP. e.g.: range(0:10)
        filter <regex:ip>: A regex query to search IP addresses. e.g.: filter .*50
        save (<var> | all) <type> <filename> [<filetype>]: Save data into a file (default JSON). e.g. save all geoip file json
        help: Prints help dialog.
        exit: Exit.
        """
        print(message)

    def get_lookup_data(self, response, filtered):
        """  Get information from RDAP and GeoIP webpages """

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
                range_found = re.search("\((.+?)\)", self.params[0])
                if range_found:
                    range_list = range_found.group(1).split(":")

                    ip_range_list = response.get("data", []) if len(self.params) == 1 else filtered[self.params[1]]

                    if len(range_list) > 1:
                        lookup_ip = LookupIP(
                            ip_range_list,
                            self.command,
                            start=int(range_list[0]),
                            end=int(range_list[1])
                        )
                    else:
                        lookup_ip = LookupIP(
                            ip_range_list,
                            self.command,
                            start=0,
                            end=int(range_list[0])
                        )
            else:
                return False
        else:
            lookup_ip = LookupIP([self.params[0]], self.command)

        return lookup_ip

    def load_file(self):
        reader = LoadIPFile(self.params[0])
        reader.read_ip_list()
        self.data = reader.get_ip_list()
        if not self.data:
            message = "No data has been loaded!"
        else:
            message = f"{len(self.data)} IP addresses has been loaded!"

        return message

    def set_filtered_data(self, response, filtered):
        self.filtered_data = filtered

        filtered_ips = QueryFilter(
            response.get("data", []),
            self.params[0]
        )
        filtered_ips.filter_ips()
        self.filtered_data[f"a{len(self.filtered_data)+1}"] = filtered_ips.get_filtered_ips()

        self.data = response.get("data", [])

        return f"Filtered data in var A{len(self.filtered_data)}"

    def lookup_data(self, response, filtered):
        lookup_ip = self.get_lookup_data(response, filtered)

        if lookup_ip:
            lookup_ip.check_ip_list()
            self.data = response.get("data", [])

            message = "IPs has been consulted!"
        else:
            message = "No data has been loaded!"

        self.filtered_data = filtered

        return message

    def save_data(self, data, command, filename, filetype="json"):
        if filetype not in ["json", "csv", "yaml"]:
            return "Filetype not allowed!"
        else:
            lookup_ip = LookupIP(data, command)
            if lookup_ip:
                lookup_data = lookup_ip.check_ip_list()

                with open(f"{filename}.{filetype}", "w") as outfile:
                    if filetype == "json":
                        outfile.write("[\n")
                        for _ in lookup_data:
                            json.dump(eval(_), outfile, indent=4, sort_keys=True)
                            outfile.write(",")
                        outfile.write("]")
                    elif filetype == "yaml":
                        for _ in lookup_data:
                            yaml.dump(eval(_), outfile)
                    elif filetype == "csv":
                        writer = csv.DictWriter(outfile, fieldnames=lookup_data.keys())
                        writer.writeheader()
                        for index in lookup_data:
                            writer.writerow(index)

                message = "File created successfully!"
            else:
                message = "No data has been loaded!"

            return message

    def run_command(self, response, filtered={}):
        """ Run commands """
        self.data = response.get("data", [])
        self.filtered_data = filtered

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
                    message = self.load_file()
                elif self.command == "filter":
                    message = self.set_filtered_data(response, filtered)
                elif self.command in ["geoip", "rdap"]:
                    message = self.lookup_data(response, filtered)
                elif self.command == "save":
                    if self.params[0] == "all":
                        message = self.save_data(
                            response.get("data", []),
                            self.params[1],
                            self.params[2],
                            self.params[3]
                        )
                    else:
                        message = self.save_data(
                            filtered[self.params[0]],
                            self.params[1],
                            self.params[2],
                            self.params[3]
                        )
            else:
                message = f"Invalid syntax for command <{self.command}>.\n"
                message += "Type help for more info."

        return {
            "msg": message,
            "data": self.data,
            "filter": self.filtered_data
        }
