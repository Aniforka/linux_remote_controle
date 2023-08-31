import os
import subprocess

class Service:
    def __init__(self, title, status):
        self.title = title
        self.status = status
        self.isChecked = "checked" if status else ""

    def enabling(self):
        os.system(f"systemctl start {self.title}")
        os.system(f"systemctl enable {self.title}")

    def disabling(self):
        os.system(f"systemctl stop {self.title}")
        os.system(f"systemctl disable {self.title}")

    def restart(self):
        if not self.status:
            self.status = 1
            self.isChecked = "checked"

        os.system(f"systemctl restart {self.title}")

    def toggle(self):
        if self.status:
            self.status = 0
            self.isChecked = ""
            self.disabling()
        else:
            self.status = 1
            self.isChecked = "checked"
            self.enabling()

    def get_directory(self):
        cmd = f"systemctl show {self.title} --property=WorkingDirectory"
        result = str(subprocess.check_output(cmd, shell=True))

        return result.split('=')[1][:-3]
