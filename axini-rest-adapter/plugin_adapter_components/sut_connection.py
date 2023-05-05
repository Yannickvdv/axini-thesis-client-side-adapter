from flask import Flask
app = Flask(__name__)

class RestInterface:

    """
    Constructor
    """
    def __init__(self, logger, response_received):
        self.logger = logger
        self.response_received = response_received
        self.browser = None


    """
    Special function: class name
    """
    def __name__(self):
        return "Sut"


    """
    Connects to the SUT and prepares it for testing.
    """
    def start(self):
        self.logger.info("Sut", "")
        app.run(debug=True)


    """
    Prepares the SUT for a new test case.
    """
    def reset(self):
        self.logger.info("Sut", "")


    """
    Perform any cleanup if the selenium has stopped
    """
    def stop(self):
        self.logger.info("Sut", "The REST API has been spun down")


    """
    Parse the SUT's response and add it to the response stack from the
    Handler class.
    """
    def handle_response(self, response):
        self.logger.debug("Sut", "Add response: {}".format(response))
        self.response_received(response)


    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path, request):
        print(request)
        return 'You want path: %s' % path
