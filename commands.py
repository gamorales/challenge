import re
from dataclasses import dataclass, field

from dialog import ShowMessageDialog
from load_file import LoadIPFile
from lookup_ip import LookupIP

# Number of parameters per function
PARAMS_QTY = {
        "load": 1,
        "find": 3,
        "rdap": 1,
        "geoip": 1,
}


@dataclass
class Commands(object):
    command: str
    params: list
    data: list = field(default_factory=list)

    def validate_params_qty(self, command, params_qty, valid_qty):
        """ Check if params quantity is ok """

        if params_qty != valid_qty:
            msg = ShowMessageDialog(
                message=f"\n\nInvalid syntax for command <{command}>."
                        "Type help for more info.",
                title="Error"
            )
            msg.showMessage()
            return False

        return True

    @staticmethod
    def print_help():
        message = """
        load <file>: Load file into memory
        print: Print a list with IPs loaded
        geoip [<ip> | <range> | all]: Geo-location lookup tool. Ej: range(0:10)
        rdap [<ip> | <range> | all]: Registration data access search for IP. Ej: range(0:10)
        find <regex:ip>: A regex query to search IP address
        help: Prints help dialog
        exit: Exit
        """
        print(message)

    def run_command(self, response):
        """ Run commands """

        qty = PARAMS_QTY.get(self.command, 0)
        if qty == 0:
            message = "Invalid command!"
        else:
            if self.validate_params_qty(self.command, len(self.params), qty):

                if self.command == "load":
                    reader = LoadIPFile(self.params[0])
                    reader.read_ip_list()
                    self.data = reader.get_ip_list()
                    if not self.data:
                        message = "No data has been loaded!"
                    else:
                        message = f"{len(self.data)} IP addresses has been loaded!"

                elif self.command in ["geoip", "rdap"]:
                    if self.params[0] == "all":
                        lookup_ip = LookupIP(
                            response.get("data", []),
                            self.command
                        )
                    elif self.params[0].startswith("range"):
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
                        lookup_ip = LookupIP([self.params[0]], self.command)

                    ip_list = lookup_ip.check_ip_list()
                    self.data = response.get("data", [])

                    if self.command == "rdap":
                        lookup_ip.important_keys = [
                                "handle", "startAddress", "endAddress",
                                "ipVersion", "type"
                        ]

                    lookup_ip.get_important_keys(ip_list)
                    message = ""

        return {"msg": message, "data": self.data}
