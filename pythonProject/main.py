import sys
import subprocess
import pkg_resources
import os

# Required packages from requirements.txt
requirements_path = os.path.join(os.path.dirname(__file__), './requirements.txt')
with open(requirements_path) as f:
    required = f.read().splitlines()

installed = {pkg.key for pkg in pkg_resources.working_set}
missing = set(required) - installed

if missing:
    print(f"Installing missing packages: {', '.join(missing)}")
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing])

from PyQt5 import QtWidgets
from gui.gui_manager import MyMainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()