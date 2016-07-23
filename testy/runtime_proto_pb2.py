# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: runtime_proto.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='runtime_proto.proto',
  package='',
  syntax='proto3',
  serialized_pb=_b('\n\x13runtime_proto.proto\"\xea\x01\n\x0bRuntimeData\x12\'\n\x06sensor\x18\x02 \x03(\x0b\x32\x17.RuntimeData.SensorData\x12\'\n\x0brobot_state\x18\x01 \x01(\x0e\x32\x12.RuntimeData.State\x1a\x35\n\nSensorData\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02\x12\n\n\x02id\x18\x03 \x01(\t\"R\n\x05State\x12\x13\n\x0fSTUDENT_CRASHED\x10\x00\x12\x13\n\x0fSTUDENT_RUNNING\x10\x01\x12\x13\n\x0fSTUDENT_STOPPED\x10\x02\x12\n\n\x06TELEOP\x10\x03\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_RUNTIMEDATA_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='RuntimeData.State',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STUDENT_CRASHED', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STUDENT_RUNNING', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STUDENT_STOPPED', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TELEOP', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=176,
  serialized_end=258,
)
_sym_db.RegisterEnumDescriptor(_RUNTIMEDATA_STATE)


_RUNTIMEDATA_SENSORDATA = _descriptor.Descriptor(
  name='SensorData',
  full_name='RuntimeData.SensorData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='RuntimeData.SensorData.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='RuntimeData.SensorData.value', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='id', full_name='RuntimeData.SensorData.id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=121,
  serialized_end=174,
)

_RUNTIMEDATA = _descriptor.Descriptor(
  name='RuntimeData',
  full_name='RuntimeData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sensor', full_name='RuntimeData.sensor', index=0,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='robot_state', full_name='RuntimeData.robot_state', index=1,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_RUNTIMEDATA_SENSORDATA, ],
  enum_types=[
    _RUNTIMEDATA_STATE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=258,
)

_RUNTIMEDATA_SENSORDATA.containing_type = _RUNTIMEDATA
_RUNTIMEDATA.fields_by_name['sensor'].message_type = _RUNTIMEDATA_SENSORDATA
_RUNTIMEDATA.fields_by_name['robot_state'].enum_type = _RUNTIMEDATA_STATE
_RUNTIMEDATA_STATE.containing_type = _RUNTIMEDATA
DESCRIPTOR.message_types_by_name['RuntimeData'] = _RUNTIMEDATA

RuntimeData = _reflection.GeneratedProtocolMessageType('RuntimeData', (_message.Message,), dict(

  SensorData = _reflection.GeneratedProtocolMessageType('SensorData', (_message.Message,), dict(
    DESCRIPTOR = _RUNTIMEDATA_SENSORDATA,
    __module__ = 'runtime_proto_pb2'
    # @@protoc_insertion_point(class_scope:RuntimeData.SensorData)
    ))
  ,
  DESCRIPTOR = _RUNTIMEDATA,
  __module__ = 'runtime_proto_pb2'
  # @@protoc_insertion_point(class_scope:RuntimeData)
  ))
_sym_db.RegisterMessage(RuntimeData)
_sym_db.RegisterMessage(RuntimeData.SensorData)


# @@protoc_insertion_point(module_scope)