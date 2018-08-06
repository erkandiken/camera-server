import tkinter as tk
import tkinter.messagebox as msb

import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from holmos_camera_server.dummycamserver import CamServer_RequestHandler, CamServer_CaptureHandler

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.httpd = None
        self.shutter_speed = tk.StringVar()

        self.pack()
        self.init_widgets()
        master.protocol('WM_DELETE_WINDOW', self.on_close)
        self.shutter_speed.set(0)
        self.shutter_speed.trace('w', self.on_shutter_value)


    def init_widgets(self):
        self.lbl1 = tk.Label(self, text="Network address")
        self.address_entry = tk.Entry(self)
        self.port_entry = tk.Entry(self, width=5)
        self.lbl2 = tk.Label(self, text="Shutter speed (µs)")
        self.exp_spin = tk.Spinbox(self, from_=0, to=100000, increment=1000,
                textvariable=self.shutter_speed)
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
        server_address = (address, port)
        self.httpd = HTTPServer(server_address, CamServer_RequestHandler)
        self.httpd.capture_handler = CamServer_CaptureHandler('image_150318.jpg')

        # Serve the HTTP stream in a separate thread to avoid GUI blocking
        self.httpd_thread = threading.Thread(target=self.httpd.serve_forever)
        self.httpd_thread.daemon = True
        self.httpd_thread.start()

        logging.info("Serving on http://{}:{}".format(server_address[0], server_address[1]))

    def on_shutter_value(self, shutter_var, blank, mode):
        shutter_value = int(self.exp_spin.get())
        # FOR REAL PICAM: self.httpd.capture_handler.cam.shutter_speed = shutter_value


    def on_close(self):
        """ End the HTTP Server and join its thread with the GUI thread. """
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.httpd_thread.join()
        self.master.destroy()


if __name__ == '__main__':
    logging.basicConfig(level=0, format='%(asctime)-15s [%(levelname)s] %(message)s')
    root = tk.Tk()
    root.title("CamServer")
    app = Application(master=root)
    app.mainloop()
