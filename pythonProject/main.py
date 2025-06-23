import sys
import subprocess
import importlib.metadata
import os

# Required packages from requirements.txt
requirements_path = os.path.join(os.path.dirname(__file__), './requirements.txt')
with open(requirements_path) as f:
    required = f.read().splitlines()

installed = {pkg.metadata['name'].lower() for pkg in importlib.metadata.distributions()}
missing = set(required) - installed

if missing:
    print(f"Installing missing packages: {', '.join(missing)}")
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing])

# Import after ensuring dependencies are installed
from PyQt5 import QtWidgets
from gui.gui_manager import MyMainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()