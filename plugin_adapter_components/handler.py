import sys
import time
from decimal import Decimal
from threading import Thread
from datetime import date
from .sut_connection import SeleniumInterface
from .adapter_core import AdapterCore

sys.path.insert(0, './api')
from api.label_pb2 import Label
"""
Domain specific adapter component. These are all the specific adapter methods
that need to be implemented for a specific SUT.

When a response is received from the SUT, the adapter_core.send_response
method should be called
"""

# ALIASES
Parameter = Label.Parameter
Value = Parameter.Value
Array = Value.Array
Hash = Value.Hash
Entry = Hash.Entry


class Handler:
    def __init__(self, logger, channel, measure_coverage):
        self.adapter_core: AdapterCore | None = None # callback to adapter; register separately
        self.configuration = []

        # Initialize empty SUT connections
        self.sut: SeleniumInterface | None = None
        self.event_queue = []
        self.event_thread = None

        # Initialize logger
        self.logger = logger
        self.channel = channel
        self.measure_coverage = measure_coverage


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
    def send_response(self, label_name, parameters_type={}, parameters_value={}):
        self.logger.debug("Handler", "response received: {}".format(label_name))
        if self.adapter_core:
            self.adapter_core.send_response(self.response(label_name, parameters_type, parameters_value),
            None, time.time_ns())


    """
    SUT SPECIFIC

    Prepare the SUT to start testing.
    """
    def start(self):
        self.sut = SeleniumInterface(self.logger, self.event_queue, self.send_response, self.measure_coverage)
        self.sut.start()

        self.stop_event_thread = False
        self.event_thread = Thread(target=self.running_event, args=(lambda: self.stop_event_thread,))
        self.event_thread.start()


    """
    SUT SPECIFIC

    Prepare the SUT for the next test case.
    return [Dict, String] [response, exception_message]
    """
    def reset(self):
        self.logger.info("Handler", "Resetting the sut for new test cases")
        self.sut.reset()        


    """
    SUT SPECIFIC

    Stop the SUT from testing.
    """
    def stop(self):
        self.logger.info("Handler", "Stopping the plugin adapter from plugin handler")

        # Stop the event thread
        if self.event_thread:
            self.stop_event_thread = True
            self.event_thread.join()
            self.event_thread = None

        # Stop the SUT 
        if self.sut:
            self.sut.stop()
            self.sut = None
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
    def response(self, label_name, parameters_type, parameters_value=None):
        if parameters_value == None or parameters_value == {}:
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
                self.stimulus('click', {'selector': 'string'}),
                self.stimulus('fill_in', {'selector': 'string', 'value': 'string'}),
                self.stimulus('open_url', {'url': 'string'}),
                self.stimulus('refresh'),
                self.stimulus('accept_alert'),

                self.response('page_update', {'mutations': 'struct'}),
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
        self.event_queue.append(label)


    """
    A threadable function to allow for simultaneous stimuli and responses
    """
    def running_event(self, stop):
        while True:
            if stop():
                break

            if self.event_queue:
                label = self.event_queue[0]
                self.event_queue.pop(0)
                match label.label:
                    case 'click':
                        self.sut.click(label.parameters[0].value.string)
                    case 'open_url':
                        self.sut.open_url(label.parameters[0].value.string)
                    case 'refresh':
                        self.sut.refresh()
                    case 'fill_in':
                        self.sut.fill_in(label.parameters[0].value.string, label.parameters[1].value.string)
                    case 'accept_alert':
                        self.sut.accept_alert()
                    case _:
                        self.logger.warning("Handler", f"Unknown label: {label.label}")

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

            param = Parameter(name=param_name, value=pb_value)
            pb_params += [param]

        pb_label = Label(label=label_name,
                                   type=label_type,
                                   channel=self.channel,
                                   parameters=pb_params)

        pb_label.timestamp = time.time_ns()

        return pb_label


    """
    TODO ADD ARRAY AND HASH TYPES

    Generate a protobuf Label containing parameters with filled in values.
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

            pb_value = Value()

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
                pb_value.array.CopyFrom(self.encodeList(value))
            elif param_type == "struct":
                pb_value.struct.CopyFrom(self.encodeDict(value))
            else:
                self.logger.warning("Handler", "UNKNOWN TYPE FOR PARAM/STIMULUS in generate value: {}".format(param_type))

            param = Parameter(name=param_name, value=pb_value)
            pb_params += [param]

        pb_label = Label(label=label_name,
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
        pb_value = Value()
        value = None


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
        elif param_type == "array":
            value = []
        elif param_type == "struct":
            value = {}
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
                    self.broker_connection.close(reason=message)
                    return 0

        message = "Could not find param " + param_name + " in label " + label
        self.broker_connection.close(reason=message)


    def encodeList(self, source: list) -> Array:
        values = [self.encodeToValue(value) for value in source]
        pb_array = Array()
        pb_array.values.extend(values)
        return pb_array
    

    def encodeDictItem(self, key : str, value : any) -> Entry:
        pb_entry = Entry()
        pb_entry.key.string = key
        pb_entry.value.CopyFrom(self.encodeToValue(value))
        return pb_entry


    def encodeDict(self, source: dict) -> Hash:
        entries = [self.encodeDictItem(key, value) for key, value in source.items()]
        pb_hash = Hash()
        pb_hash.entries.extend(entries)
        return pb_hash


    def encodeToValue(self, var : any) -> Value:
        value = Value()
        match var:
            case str():
                value.string = var
            case int():
                value.integer = var
            case float():
                value.decimal = var
            case bool():
                value.boolean = var
            case date():
                value.date = var
            # case time():
                # value.time = var
            case list():
                value.array.CopyFrom(self.encodeList(var))
            case dict():
                value.struct.CopyFrom(self.encodeDict(var))
        return value
