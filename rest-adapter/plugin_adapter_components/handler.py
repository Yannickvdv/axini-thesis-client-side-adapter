import sys
import time
import threading
from decimal import Decimal
from datetime import date
from .sut_connection import RestInterface
from .adapter_core import AdapterCore

sys.path.insert(0, './api')
import label_pb2

"""
Domain specific adapter component. These are all the specific adapter methods
that need to be implemented for a specific SUT.

When a response is received from the SUT, the adapter_core.send_response
method should be called
"""


class Handler:
    def __init__(self, logger, channel):
        self.adapter_core: AdapterCore | None = None # callback to adapter; register separately
        self.configuration = []

        # Initialize empty SUT connections
        self.sut_connection: RestInterface | None = None

        # Initialize logger
        self.logger = logger
        self.channel = channel


    """
    Set the adapter core object reference.
    param [AdapterCore] adapter_core
    """
    def register_adapter_core(self, adapter_core):
        self.adapter_core = adapter_core


    """
    SUT SPECIFIC

    The SUT has produced a response which needs to be passed on to AMP.
    param[[channel, key, type, value]]
    """
    def send_respone(self, label_name, parameters_type={}, parameters_value={}):
        self.logger.debug("Handler", "response received: {}".format(label_name))
        if self.adapter_core:
            self.adapter_core.send_response(self.response(label_name, parameters_type, parameters_value),
            None, time.time_ns())

    """
    SUT SPECIFIC

    Prepare the SUT to start testing.
    """
    def start(self):
        self.sut_connection = RestInterface(self.logger, self.send_respone)
        self.sut_connection.start()


    """
    SUT SPECIFIC

    Prepare the SUT for the next test case.
    return [Dict, String] [response, exception_message]
    """
    def reset(self):
        self.logger.info("Handler", "Resetting the sut for new test cases")
        

    """
    SUT SPECIFIC

    Stop the SUT from testing.
    """
    def stop(self):
        self.logger.info("Handler", "Stopping the plugin adapter from plugin handler")

        if self.sut_connection:
            self.sut_connection.stop()
            self.sut_connection = None
        else:
            self.logger.debug("Handler", "Sut connection has not yet been initialized")

        self.logger.debug("Handler", "Finished stopping the plugin adapter from plugin handler")


    """
    Generate a protobuf Stimulus Label.
    return [label_pb2.Label]
    """
    def stimulus(self, label_name, parameters={}):
        return self.generate_type_label(label_name, 0, parameters)


    """
    Generate a protobuf Response Label.
    return [label_pb2.Label]
    """  
    def response(self, label_name, parameters_type={}, parameters_value={}):
        if parameters_value == {}:
            return self.generate_type_label(label_name, 1, parameters_type)
        else:
            return self.generate_value_label(label_name, 1, parameters_type, parameters_value)


    """
    SUT SPECIFIC

    The labels supported by the adapter.
    return [label_pb2.Label]
    """
    def supported_labels(self):
        return [

                self.stimulus('not_found', {'status': 'integer'}),
                self.stimulus('found', {'status': 'integer', 'body': 'string'}),
        ]
    
    
    """
    SUT SPECIFIC

    Processes a stimulus of a given Label message. This method also sets the
    timestamp and physical label on the Label object. The BrokerConnection
    handles the confirmation to TestManager itself.
    param [label_pb2.Label] label
    return [String] The physical label.
    """
    def stimulate(self, label):
        physical_label = None
        label_name = label.label

        # TODO: Implement threading        
        # new_thread = threading.Thread(target=self.threaded_simulate, args=(label,))
        # new_thread.start()

        if self.sut_connection:
            if label_name == 'found':
                self.sut_connection.add_http_response_to_queue(
                    self.get_param_value(label, 'status'),
                    self.get_param_value(label, 'body'))

            elif label_name == 'not_found':
                self.sut_connection.add_http_response_to_queue(
                    self.get_param_value(label, 'status'))

            else: 
                raise Exception(f"Unsupported stimulus {label.label!r}")
   

        return physical_label
    

    """
    TODO ADD ARRAY AND HASH TYPES

    Generate a protobuff label object with default type values.
    param [String] label_name
    param [label_pb2.Label.LabelType] label_type
    param [dict] parameters
    return [label_pb2.Label]
    """
    def generate_type_label(self, label_name, label_type, parameters={}):
        pb_params = []

        # Create all the google protobuff Label:Paramater objects
        for param_name, param_type in parameters.items():
            pb_value = self.instantiate_label_value(param_type)[0]

            param = label_pb2.Label.Parameter(name=param_name, value=pb_value)
            pb_params += [param]

        pb_label = label_pb2.Label(label=label_name,
                                   type=label_type,
                                   channel=self.channel,
                                   parameters=pb_params)

        pb_label.timestamp = time.time_ns()

        return pb_label


    """
    TODO ADD ARRAY AND HASH TYPES

    Generate a protobuf Label containing parameters with filled in values.
    param [String] channel
    param [String] label_name
    param [label_pb2.Label.LabelType] label_type
    param [dict] parameters_type
    param [dict] parameters_value
    return [label_pb2.Label]
    """
    def generate_value_label(self, label_name, label_type, parameters_type, parameters_value):
        pb_params = []

        # Create all the google protobuff Label:Paramater objects
        for param_name, param_type in parameters_type.items():
            value = parameters_value.get(param_name)

            pb_value = label_pb2.Label.Parameter.Value()

            if param_type == "string":
                pb_value.string = value
            elif param_type == "integer":
                pb_value.integer = value
            elif param_type == "decimal":
                pb_value.decimal = value
            elif param_type == "boolean":
                pb_value.boolean = value
            elif param_type == "date":
                pb_value.date = value
            elif param_type == "time":
                pb_value.time = value
            elif param_type == "array":
                pb_value.array = value
            else:
                self.logger.warning("Handler", "UNKNOWN TYPE FOR PARAM/STIMULUS in generate value: {}".format(param_type))

            param = label_pb2.Label.Parameter(name=param_name, value=pb_value)
            pb_params += [param]

        pb_label = label_pb2.Label(label=label_name,
                                   type=label_type,
                                   channel=self.channel,
                                   parameters=pb_params)

        pb_label.timestamp = time.time_ns()

        return pb_label

    """
    Instantiate a label type. In case a struct is wanted, define a dictionary
    using the wanted keys with instantiated values.
    param [String] param_type
    return [label_pb2.Label.Parameter.Value]
    """
    def instantiate_label_value(self, param_type):
        pb_value = label_pb2.Label.Parameter.Value()
        value = None

        # Check for array data type
        if isinstance(param_type, list):
            value = self.instantiate_label_value(param_type[0])[1]
            pb_value.array = value
            return pb_value

        if param_type == "string":
            pb_value.string = 'string'
            value = 'string'
        elif param_type == "integer":
            pb_value.integer = 1
            value = 1
        elif param_type == "decimal":
            pb_value.decimal = Decimal(1.0)
            value = Decimal(1.0)
        elif param_type == "boolean":
            pb_value.boolean = True
            value = True
        elif param_type == "date":
            pb_value.date = date.today()
            value = date.today()
        elif param_type == "time":
            pb_value.time = time.time_ns()
            value = time.time_ns()
        else:
            self.logger.warning("Handler", "UNKNOWN TYPE FOR PARAM/STIMULUS in generate type: {}".format(param_type))

        return pb_value, value

    """
    Obtain the value of a parameter from a label.
    param [label_pb2.Label] label
    param [String] param_name
    return [value]
    """
    def get_param_value(self, label, param_name):
        for param in label.parameters:
            if param.name == param_name:
                if param.value.HasField("string"):
                    return param.value.string
                elif param.value.HasField("integer"):
                    return param.value.integer
                elif param.value.HasField("decimal"):
                    return param.value.decimal
                elif param.value.HasField("boolean"):
                    return param.value.boolean
                elif param.value.HasField("date"):
                    return param.value.date
                elif param.value.HasField("time"):
                    return param.value.time
                elif param.value.HasField("array"):
                    return param.value.array
                elif param.value.HasField("struct"):
                    return param.value.struct
                elif param.value.HasField("hash_value"):
                    return param.value.hash_value
                else:
                    message = "Received an unknown label type"
                    if self.adapter_core:
                        self.adapter_core.send_error(message)
          
                    self.logger.debug("Handler", message)
                    return 0

        message = "Could not find param " + param_name + " in label " + label
        if self.adapter_core:
                self.adapter_core.send_error(message)

        self.logger.debug("Handler", message)