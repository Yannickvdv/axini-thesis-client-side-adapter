import json
from datetime import datetime
from xml.etree import ElementTree
from .http_adapter_labels import Get, Post, Answer
import requests

class HttpSut:
    """
    Constructor
    """
    def __init__(self, logger, response_received):
        self.logger = logger
        self.response_received = response_received
        self.channel = "server_side"

    """
    Special function: class name
    """
    def __name__(self):
        return "Sut"

    """
    Perform any cleanup if the selenium has stopped
    """
    def stop(self):
        self.logger.info("Sut", "Http requests to the server have been stopped")

    """
    Parse the SUT's response and add it to the response stack from the
    Handler class.
    """
    def handle_response(self, response):
        self.logger.debug("Sut", "Add response: {}".format(response))
        code = int(response.status_code)
        headers = dict(response.headers)
        body = response.text
        response_label = None

        if 'xml' in headers.get('content-type', ''):
            document = ElementTree.fromstring(body)
            hash = ElementTree.ElementTree(document).getroot().attrib
            response_label = Answer(code, json.dumps(headers), json.dumps(hash)).getDir(self.channel)

            self.logger.info("Sut", f"Answer is an XML message: {response_label}")
        else:
            response_label = Answer(code, json.dumps(headers), body).getDir(self.channel)

            self.logger.info("Sut", f"Answer is a JSON message: {response_label}")
        
        self.response_received(response_label)

    def perform_post_request(self, body, headers, uri):
        self.logger.info("Sut", f"POST request for endpoint: {uri}")
        try:
            response = requests.post(url=uri, data=body, headers=headers)
            self.logger.info("Sut", f"POST answer for endpoint: {uri}")
            self.handle_response(response)
        except Exception as e:
            # TODO: handle error
            print(str(e))
            # self.adapter_core.send_error(str(e))

    def perform_get_request(self, headers, uri):
        self.logger.info("Sut", f"GET request for endpoint: {uri}")

        try:
            response = requests.get(uri, headers=headers)
            self.logger.info("Sut", "GET answer for endpoint: {uri}")
            self.handle_response(response)
        except Exception as e:
            # TODO: handle error
            print(str(e))
            # self.adapter_core.send_error(str(e))
