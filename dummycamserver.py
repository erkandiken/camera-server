#!/usr/bin/python3
"""
Name: Camserver
Purpose: Serve raw bayer frames over HTTP
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import argparse

import numpy as np
import matplotlib.pyplot as plt

class CamServer_CaptureHandler():
    def __init__(self, imagefile):
        self.image = plt.imread(imagefile)
        assert self.image.shape[2] == 3 # Assert 3 channels


    def capture(self):
        x = self.image.astype(np.uint16)
        return x


class CamServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logging.info("Request path", self.path)
        if self.path == '/raw':
            self.send_response(200)

            # Capture the frame
            msg = self.server.capture_handler.capture()

            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('X-Array-Width', msg.shape[1])
            self.send_header('X-Array-Height', msg.shape[0])
            self.send_header('X-Array-Channels', msg.shape[2])
            self.send_header('X-Array-Type', msg.dtype)

            self.end_headers()

            self.wfile.write(msg.tobytes())
            return
        elif self.path == '/red':
            self.send_response(200)

            # Capture the frame
            msg = self.server.capture_handler.capture()

            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('X-Array-Width', msg.array.shape[1])
            self.send_header('X-Array-Height', msg.array.shape[0])
            self.send_header('X-Array-Channels', 1)
            self.send_header('X-Array-Type', msg.array.dtype)

            self.end_headers()

            self.wfile.write(msg.array[:, :, 0].tobytes())

if __name__ == '__main__':
    """ Parse commandline arguments """
    parser = argparse.ArgumentParser(description='Capture bayer frames and serve them over HTTP')
    parser.add_argument('--address', type=str, help='Binding address for the HTTP server', default='0.0.0.0')
    parser.add_argument('--port', type=int, help='Port the HTTP server will listen on', default=3000)

    parser.add_argument('imagefile', type=str, help='Image file the camserver will server')

    args = parser.parse_args()

    """ Configure logging """
    logging.basicConfig(level=0, format='%(asctime)-15s [%(levelname)s] %(message)s')
    logging.info("Starting CamServer")

    """ Run the server """
    server_address = (args.address, args.port)
    httpd = HTTPServer(server_address, CamServer_RequestHandler)
    httpd.capture_handler = CamServer_CaptureHandler(args.imagefile)
    logging.info("Serving on http://{}:{}".format(server_address[0], server_address[1]))

    httpd.serve_forever()
