import os
import sys
import signal
import tkinter
import platform
import threading
import subprocess
import socket

MANAGE_PY_PATH = os.path.join(os.path.dirname(__file__), "manage.py")
INIT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "setup", "init_groups.py")

class SIMKN:
    def __init__(self, root):
        self.root = root
        self.root.title("Start / Stop Django Server")
        self.server_process = None

        # Top frame untuk tombol + IP input
        top_frame = tkinter.Frame(root)
        top_frame.pack(fill=tkinter.X, padx=10, pady=10)

        # Start/Stop button (kiri)
        self.start_button = tkinter.Button(top_frame, text="Start", width=15, command=self.toggle_start)
        self.start_button.pack(side=tkinter.LEFT)

        # Update button (sebelah kanan Start)
        self.update_button = tkinter.Button(top_frame, text="Update", width=15, command=self.update_action)
        self.update_button.pack(side=tkinter.LEFT, padx=(10, 0))

        # Spacer agar label IP tetap di kanan
        tkinter.Label(top_frame, text="").pack(side=tkinter.LEFT, expand=True)

        # Label + Entry untuk alamat IP (pojok kanan)
        self.ip_label = tkinter.Label(top_frame, text="Address:", font=("Arial", 10))
        self.ip_label.pack(side=tkinter.LEFT)

        self.address_var = tkinter.StringVar()
        self.address_entry = tkinter.Entry(top_frame, textvariable=self.address_var, width=30, justify='left', fg="blue")
        self.address_entry.configure(state='readonly')
        self.address_entry.pack(side=tkinter.LEFT)

        # Area log
        self.log_output = tkinter.Text(root, height=20, width=80)
        self.log_output.pack(padx=10, pady=10)

    def get_local_ip(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())
            if ip.startswith("127."):
                ip = socket.gethostbyname(socket.getfqdn())
            return ip
        except Exception:
            return "127.0.0.1"

    def toggle_start(self):
        if self.server_process is None:
            # Jalankan server
            if platform.system() == "Windows":
                self.server_process = subprocess.run(
                    [sys.executable, MANAGE_PY_PATH, "runserver", "0.0.0.0:8000", "--noreload"],
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
            else:
                self.server_process = subprocess.run(
                    [sys.executable, MANAGE_PY_PATH, "runserver", "0.0.0.0:8000", "--noreload"],
                    preexec_fn=os.setsid,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

            self.start_button.config(text="Stop")
            self.update_button.config(state="disabled")  # ⛔ Disable Update
            ip = self.get_local_ip()
            self.address_var.set(f"http://{ip}:8000")
            self.log_output.insert(tkinter.END, "Server started...\n")
            threading.Thread(target=self.read_output, daemon=True).start()
        else:
            # Hentikan server
            if platform.system() == "Windows":
                self.server_process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                os.killpg(os.getpgid(self.server_process.pid), signal.SIGTERM)

            self.server_process = None
            self.start_button.config(text="Start")
            self.update_button.config(state="normal")  # ✅ Enable Update
            self.address_var.set("")
            self.log_output.insert(tkinter.END, "Server stopped...\n")

    def read_output(self):
        while self.server_process and self.server_process.poll() is None:
            line = self.server_process.stdout.readline()
            if line:
                self.log_output.insert(tkinter.END, line)
                self.log_output.see(tkinter.END)

    def update_action(self):
        try:
            self.log_output.insert(tkinter.END, "🔄 Running `migrate`...\n")
            self.log_output.see(tkinter.END)

            migrate_result = subprocess.run(
                [sys.executable, MANAGE_PY_PATH, "migrate"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            self.log_output.insert(tkinter.END, migrate_result.stdout)

            self.log_output.insert(tkinter.END, "\n🚀 Running `init_groups.py`...\n")
            self.log_output.see(tkinter.END)

            with open(INIT_SCRIPT_PATH, "r") as f:
                result = subprocess.run(
                    [sys.executable, MANAGE_PY_PATH, "shell"],
                    stdin=f,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                self.log_output.insert(tkinter.END, result.stdout)

            self.log_output.insert(tkinter.END, "✅ Update finished.\n")
            self.log_output.see(tkinter.END)

        except Exception as e:
            self.log_output.insert(tkinter.END, f"❌ Error during update: {e}\n")
            self.log_output.see(tkinter.END)

# Menjalankan aplikasi
if __name__ == "__main__":
    root = tkinter.Tk()
    app = SIMKN(root)
    root.mainloop()
