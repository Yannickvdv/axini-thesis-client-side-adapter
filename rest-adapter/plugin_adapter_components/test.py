from flask import Flask, request
import queue
import threading
import time

app = Flask(__name__)
http_response_queue = queue.Queue()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print("found")
    # get the request method and headers
    req_method = request.method
    req_headers = request.headers

    response = http_response_queue.get(timeout=10)
    return response            
    # return a string with the requested path, method, and headers
    return f"You want path: {path}\nRequest method: {req_method}\nRequest headers: {req_headers}\n"


def start_flask_app():
    app.run()

flask_thread = threading.Thread(target=start_flask_app, daemon=True)
flask_thread.start()

time.sleep(3)
http_response_queue.put("not_found")
time.sleep(20)