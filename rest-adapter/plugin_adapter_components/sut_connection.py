from flask import Flask, request
from flask_cors import CORS, cross_origin
import threading
from queue import Queue

# responses should be a tuple of status and body
json_response_queue: Queue[tuple[int, str]] = Queue()

class RestInterface:

    """
    Constructor
    """
    def __init__(self, logger, response_received):
        self.logger = logger
        self.response_received = response_received
        self.browser = None
        self.flask_thread = None

        self.app = Flask(__name__)
        CORS(self.app)

        # @self.app.route('/', defaults={'path': ''})
        # @self.app.route('/<path:path>', methods=['GET', 'POST'])
        # def catch_all(path):
        #     # get the request method and headers
        #     req_method = request.method
        #     req_headers = request.headers

        #     # TODO: parse the request to see if it is checking inventory 
        #     self.handle_response("post_booking")

        #     # Wait for the response from the queue
        #     response = json_response_queue.get(timeout=5)

        #     return self.app.response_class(
        #         status=response[0],
        #         response=response[1]
        #     )

        @self.app.route('/properties/<int:id>', methods=['GET'])
        def handleGetProperty(id):
            self.handle_response("get_property")

            return waitForResponse()
        
        @self.app.route('/booking', methods=['POST'])
        def handlePostBooking():
            self.handle_response("post_booking")

            return waitForResponse()

        def waitForResponse():
            # Wait for the response from the queue which is sent by AMP
            response = json_response_queue.get(timeout=10)
        
            return self.app.response_class(
                status=response[0],
                response=response[1]
            )

    """
    Special function: class name
    """
    def __name__(self):
        return "Sut"

   
    """
    Connects to the SUT and prepares it for testing.
    """
    def start(self):
        self.logger.info("Sut", "Starting the flask endpoint")
        self.flask_thread = threading.Thread(target=self.start_flask_app)
        self.flask_thread.setDaemon(True)
        self.flask_thread.start()


    def start_flask_app(self):
        self.app.run()

    """
    Prepares the SUT for a new test case.
    """
    def reset(self):
        self.logger.info("Sut", "Resetting REST API started")
        self.stop()
        self.start()
        self.logger.info("Sut", "Resetting REST API completed")



    """
    Perform any cleanup if the selenium has stopped
    """
    def stop(self):
        # if self.flask_thread: 
        #     self.flask_thread.join()
        self.logger.info("Sut", "The REST API has been spun down")


    """
    Parse the SUT's response and add it to the response stack from the
    Handler class.
    """
    def handle_response(self, response):
        self.logger.debug("Sut", "Add response: {}".format(response))
        self.response_received(response)


    def add_http_response_to_queue(self, status_code, body={}):
        json_response_queue.put((status_code, body))
        