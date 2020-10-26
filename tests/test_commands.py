from ..commands import Commands


class TestCommands():
    def setup(self):
        self.cmd = Commands("load", "../list_of_ips.txt")
        self.response = self.cmd.run_command()

    def test_load(self):
        
