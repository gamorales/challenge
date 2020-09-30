from dataclasses import dataclass

from dialog import ShowMessageDialog
from load_file import LoadIPFile
from lookup_ip import LookupIP

params_q = {
        "load": 1,
        "find": 3,
        "rdap": 1,
        "geoip": 1,
}


@dataclass
class Commands(object):
    command: str
    params: list

    def validate_params_qty(self, command, params_qty, valid_qty):
        """
        Check if the params quantity is ok
        """
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
        find <ip>: A regex query to search IP address
        rdap <ip>: Registration data access search for IP
        geoip <ip>: Geo-location lookup tool
        help: Prints help dialog
        exit: Exit
        """
        msg = ShowMessageDialog(message=message, title='Challenge Help')
        msg.showMessage()

    def run_command(self):
        qty = params_q.get(self.command, 0)
        if qty == 0:
            message = "\n\nInvalid command!"
            title = "Error"
        else:
            if self.validate_params_qty(self.command, len(self.params), qty):

                title = "Info"

                if self.command == "load":
                    reader = LoadIPFile(self.params[0])
                    if not reader.get_ip_list():
                        message = "\n\nNo data has been loaded!"
                        title = "Error"
                    else:
                        message = f"\n\n{len(reader.get_ip_list())} IP addresses has been loaded!"

                elif self.command in ["geoip", "rdap"]:
                    lookup_ip = LookupIP(self.params[0], self.command)
                    data = lookup_ip.check_ip()

                    if self.command == "rdap":
                        lookup_ip.important_keys = [
                                "handle", "startAddress", "endAddress", 
                                "ipVersion", "type"
                        ]
                    message = "\n\n" + str(lookup_ip.get_important_keys(data))

        msg = ShowMessageDialog(message=message, title=title)
        msg.showMessage()

        return message
