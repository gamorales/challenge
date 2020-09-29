from dataclasses import dataclass

from dialog import ShowMessageDialog
from load_file import LoadIPFile

params_q = {
        "load": {"params": 1, "func": ""},
        "find": 3,
        "rdap": 2,
        "geoip": {"params": 1, "func": ""},
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
        qty = params_q.get(self.command, "").get("params", 0)
        if self.validate_params_qty(self.command, len(self.params), qty):
            print(f"COMANDO: {self.command}")
            print(f"PARAMS: {self.params})")
        else:
            print("Error en el comando")
