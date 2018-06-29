import tkinter as tk
import tkinter.messagebox as msb

import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from camserver import CamServer_RequestHandler, CamServer_CaptureHandler

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.init_widgets()

    def init_widgets(self):
        self.lbl1 = tk.Label(self, text="Network address")
        self.address_entry = tk.Entry(self)
        self.port_entry = tk.Entry(self, width=5)
        self.lbl2 = tk.Label(self, text="Shutter speed (µs)")
        self.exp_spin = tk.Spinbox(self, from_=0, to=100000, increment=1000)
        self.btn = tk.Button(self, text="Start", command=self.start_btn)

        self.lbl1.grid(row=0, sticky=tk.W, padx=20, pady=10)
        self.address_entry.grid(row=0, column=1, sticky=tk.E)
        self.port_entry.grid(row=0, column=2, padx=20)

        self.lbl2.grid(row=1, sticky=tk.W, padx=20)
        self.exp_spin.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        self.exp_spin.columnconfigure(1)
        self.btn.grid(row=2, columnspan=3, pady=10)


        """ Set default values """
        self.address_entry.insert(0, "0.0.0.0")
        self.port_entry.insert(0, "3000")
    def start_btn(self):
        print("Button pressed")
        self.btn.destroy()

        address = self.address_entry.get()
        port = 3000
        try:
            port = int(self.port_entry.get())
            if(port < 1000 or port > 16000):
                raise 0
        except:
            msb.showerror("Error", "Invalid port number")
            self.master.destroy()

        """ Run the server """
        server_address = (args.address, args.port)
        httpd = HTTPServer(server_address, CamServer_RequestHandler)
        httpd.capture_handler = CamServer_CaptureHandler()
        logging.info("Serving on http://{}:{}".format(server_address[0], server_address[1]))

        httpd.serve_forever()

    

if __name__ == '__main__':
    logging.basicConfig(level=0, format='%(asctime)-15s [%(levelname)s] %(message)s')
    root = tk.Tk()
    root.title("CamServer")
    app = Application(master=root)
    app.mainloop()
    print("This is the end.")
