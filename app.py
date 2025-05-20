import os
import sys
import signal
import socket
import platform
import threading
import subprocess
from PyQt5 import QtWidgets, QtCore

MANAGE_PY_PATH = os.path.join(os.path.dirname(__file__), "manage.py")
INIT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "setup", "init_groups.py")

class ProcessThread(QtCore.QObject):
    output_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.process = None
        self.thread = None
        self.running = False

    def start_process(self, cmd):
        self.running = True

        def run():
            try:
                if platform.system() == "Windows":
                    self.process = subprocess.Popen(
                        cmd,
                        creationflags=subprocess.CREATE_NO_WINDOW,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                else:
                    self.process = subprocess.Popen(
                        cmd,
                        preexec_fn=os.setsid,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )

                for line in self.process.stdout:
                    self.output_signal.emit(line)
                    if not self.running:
                        break
            finally:
                self.running = False

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()

    def stop_process(self):
        if self.process:
            try:
                if platform.system() == "Windows":
                    import ctypes
                    kernel32 = ctypes.WinDLL('kernel32')
                    kernel32.TerminateProcess(int(self.process._handle), 1)
                else:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except Exception as e:
                print(f"Error stopping process: {e}")
            self.process = None
        self.running = False

class SIMKN(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Start / Stop Django Server")
        self.server_process = None

        self.layout = QtWidgets.QVBoxLayout(self)

        top_layout = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton("Start")
        self.update_button = QtWidgets.QPushButton("Update")
        self.address_entry = QtWidgets.QLineEdit()
        self.address_entry.setReadOnly(True)
        self.address_entry.setStyleSheet("color: blue;")

        top_layout.addWidget(self.start_button)
        top_layout.addWidget(self.update_button)
        top_layout.addStretch()
        top_layout.addWidget(QtWidgets.QLabel("Address:"))
        top_layout.addWidget(self.address_entry)
        self.layout.addLayout(top_layout)

        self.log_output = QtWidgets.QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

        self.start_button.clicked.connect(self.toggle_start)
        self.update_button.clicked.connect(self.update_action)

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def add_log(self, text):
        self.log_output.append(text)

    def toggle_start(self):
        if not self.server_process or not self.server_process.running:
            self.server_process = ProcessThread()
            self.server_process.output_signal.connect(self.add_log)
            self.server_process.start_process([sys.executable, MANAGE_PY_PATH, "runserver", "0.0.0.0:8000", "--noreload"])
            self.start_button.setText("Stop")
            self.update_button.setEnabled(False)
            ip = self.get_local_ip()
            self.address_entry.setText(f"http://{ip}:8000")
            self.add_log("Server started...\n")
        else:
            self.server_process.stop_process()
            self.server_process = None
            self.start_button.setText("Start")
            self.update_button.setEnabled(True)
            self.address_entry.clear()
            self.add_log("Server stopped...\n")

    def update_action(self):
        try:
            self.add_log("\U0001F504 Running `migrate`...")
            kwargs = {}
            if platform.system() == "Windows":
                kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

            migrate_result = subprocess.run(
                [sys.executable, MANAGE_PY_PATH, "migrate"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                **kwargs
            )
            self.add_log(migrate_result.stdout)
            
            self.add_log("\n\U0001F680 Running `init_groups.py`...")
            with open(INIT_SCRIPT_PATH, "r") as f:
                script_content = f.read()

            shell_result = subprocess.run(
                [sys.executable, MANAGE_PY_PATH, "shell"],
                input=script_content,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                **kwargs
            )
            self.add_log(shell_result.stdout)
            self.add_log("\u2705 Update finished.\n")

        except Exception as e:
            self.add_log(f"\u274C Error during update: {e}\n")
            import traceback
            self.add_log(traceback.format_exc())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SIMKN()
    window.show()
    sys.exit(app.exec_())