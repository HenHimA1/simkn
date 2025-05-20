import os
import sys
import signal
import socket
import tkinter as tk
from tkinter import scrolledtext
import platform
import threading
import subprocess

# Constants for subprocess
DETACHED_PROCESS = 0x00000008
CREATE_NO_WINDOW = 0x08000000

MANAGE_PY_PATH = os.path.join(os.path.dirname(__file__), "manage.py")
INIT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "setup", "init_groups.py")

class ProcessThread:
    def __init__(self):
        self.process = None
        self.thread = None
        self.running = False
        
    def start_process(self, cmd):
        self.running = True

        def run():
            if platform.system() == "Windows":
                # Gunakan CREATE_NO_WINDOW flag untuk mencegah window console muncul di Windows
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
            
            # Read output
            while self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line and hasattr(self, 'output_callback') and self.output_callback:
                    self.output_callback(line)
            
            # Jika proses selesai secara normal
            self.running = False

        self.thread = threading.Thread(target=run, daemon=True)
        self.thread.start()
    
    def set_output_callback(self, callback):
        self.output_callback = callback

    def stop_process(self):
        if self.process:
            try:
                if platform.system() == "Windows":
                    # Gunakan Win32 API untuk mengakhiri proses dengan lebih bersih
                    # tanpa menampilkan jendela pesan
                    import ctypes
                    kernel32 = ctypes.WinDLL('kernel32')
                    kernel32.TerminateProcess(int(self.process._handle), 1)
                else:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except Exception as e:
                print(f"Error stopping process: {e}")
            self.process = None
        self.running = False
        
class SIMKN:
    def __init__(self, root):
        self.root = root
        self.root.title("Start / Stop Django Server")
        self.server_process = None

        # Top frame untuk tombol + IP input
        top_frame = tk.Frame(root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        # Start/Stop button (kiri)
        self.start_button = tk.Button(top_frame, text="Start", width=15, command=self.toggle_start)
        self.start_button.pack(side=tk.LEFT)

        # Update button (sebelah kanan Start)
        self.update_button = tk.Button(top_frame, text="Update", width=15, command=self.update_action)
        self.update_button.pack(side=tk.LEFT, padx=(10, 0))

        # Spacer agar label IP tetap di kanan
        tk.Label(top_frame, text="").pack(side=tk.LEFT, expand=True)

        # Label + Entry untuk alamat IP (pojok kanan)
        self.ip_label = tk.Label(top_frame, text="Address:", font=("Arial", 10))
        self.ip_label.pack(side=tk.LEFT)

        self.address_var = tk.StringVar()
        self.address_entry = tk.Entry(top_frame, textvariable=self.address_var, width=30, justify='left', fg="blue")
        self.address_entry.configure(state='readonly')
        self.address_entry.pack(side=tk.LEFT)

        # Area log dengan scrollbar
        self.log_output = scrolledtext.ScrolledText(root, height=20, width=80)
        self.log_output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Event handler untuk closing window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Tidak benar-benar terhubung, hanya menetapkan target tujuan
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def add_log(self, text):
        self.log_output.insert(tk.END, text)
        self.log_output.see(tk.END)
        # Memperbarui UI
        self.root.update_idletasks()

    def toggle_start(self):
        if not self.server_process or not self.server_process.running:
            # Jalankan server
            self.server_process = ProcessThread()
            self.server_process.set_output_callback(self.add_log)
            self.server_process.start_process([sys.executable, MANAGE_PY_PATH, "runserver", "0.0.0.0:8000", "--noreload"])
            self.start_button.config(text="Stop")
            self.update_button.config(state="disabled")  # ⛔ Disable Update
            ip = self.get_local_ip()
            self.address_var.set(f"http://{ip}:8000")
            self.add_log("Server started...\n")
        else:
            if self.server_process:
                self.server_process.stop_process()
            self.server_process = None
            self.start_button.config(text="Start")
            self.update_button.config(state="normal")  # ✅ Enable Update
            self.address_var.set("")
            self.add_log("Server stopped...\n")

    def update_action(self):
        try:
            self.add_log("🔄 Running `migrate`...\n")

            # Gunakan flags khusus untuk mencegah window console muncul
            kwargs = {}
            if platform.system() == "Windows":
                kwargs["creationflags"] = CREATE_NO_WINDOW
            
            migrate_process = subprocess.run(
                [sys.executable, MANAGE_PY_PATH, "migrate"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                **kwargs
            )
            self.add_log(migrate_process.stdout)
                
            self.add_log("\n🚀 Running `init_groups.py`...\n")

            # Read the script content
            with open(INIT_SCRIPT_PATH, "r") as f:
                script_content = f.read()
            
            # Run the script in Django shell
            shell_process = subprocess.run(
                [sys.executable, MANAGE_PY_PATH, "shell"],
                input=script_content,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                **kwargs
            )
            self.add_log(shell_process.stdout)

            self.add_log("✅ Update finished.\n")

        except Exception as e:
            self.add_log(f"❌ Error during update: {e}\n")
            import traceback
            self.add_log(traceback.format_exc())

    def on_closing(self):
        if self.server_process:
            self.server_process.stop_process()
        self.root.destroy()

# Menjalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = SIMKN(root)
    root.mainloop()