# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: announcement.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import configuration_pb2 as configuration__pb2
import label_pb2 as label__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='announcement.proto',
  package='PluginAdapter.Api',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x12\x61nnouncement.proto\x12\x11PluginAdapter.Api\x1a\x13\x63onfiguration.proto\x1a\x0blabel.proto\"\x7f\n\x0c\x41nnouncement\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x37\n\rconfiguration\x18\x02 \x01(\x0b\x32 .PluginAdapter.Api.Configuration\x12(\n\x06labels\x18\x03 \x03(\x0b\x32\x18.PluginAdapter.Api.Labelb\x06proto3')
  ,
  dependencies=[configuration__pb2.DESCRIPTOR,label__pb2.DESCRIPTOR,])




_ANNOUNCEMENT = _descriptor.Descriptor(
  name='Announcement',
  full_name='PluginAdapter.Api.Announcement',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='PluginAdapter.Api.Announcement.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='configuration', full_name='PluginAdapter.Api.Announcement.configuration', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='labels', full_name='PluginAdapter.Api.Announcement.labels', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=202,
)

_ANNOUNCEMENT.fields_by_name['configuration'].message_type = configuration__pb2._CONFIGURATION
_ANNOUNCEMENT.fields_by_name['labels'].message_type = label__pb2._LABEL
DESCRIPTOR.message_types_by_name['Announcement'] = _ANNOUNCEMENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Announcement = _reflection.GeneratedProtocolMessageType('Announcement', (_message.Message,), dict(
  DESCRIPTOR = _ANNOUNCEMENT,
  __module__ = 'announcement_pb2'
  # @@protoc_insertion_point(class_scope:PluginAdapter.Api.Announcement)
  ))
_sym_db.RegisterMessage(Announcement)


# @@protoc_insertion_point(module_scope)