# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: person.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='person.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0cperson.proto\"X\n\rPersonMessage\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\x14\n\x0c\x63ompany_name\x18\x04 \x01(\t\"4\n\x11PersonListMessage\x12\x1f\n\x07persons\x18\x01 \x03(\x0b\x32\x0e.PersonMessage\"\x1d\n\x0fPersonIdMessage\x12\n\n\x02id\x18\x01 \x01(\x05\"\x0e\n\x0c\x45mptyMessage2\x8f\x01\n\rPersonService\x12(\n\x06\x43reate\x12\x0e.PersonMessage\x1a\x0e.PersonMessage\x12\'\n\x03Get\x12\x10.PersonIdMessage\x1a\x0e.PersonMessage\x12+\n\x06GetAll\x12\r.EmptyMessage\x1a\x12.PersonListMessageb\x06proto3'
)




_PERSONMESSAGE = _descriptor.Descriptor(
  name='PersonMessage',
  full_name='PersonMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='PersonMessage.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='first_name', full_name='PersonMessage.first_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_name', full_name='PersonMessage.last_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='company_name', full_name='PersonMessage.company_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=16,
  serialized_end=104,
)


_PERSONLISTMESSAGE = _descriptor.Descriptor(
  name='PersonListMessage',
  full_name='PersonListMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='persons', full_name='PersonListMessage.persons', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=106,
  serialized_end=158,
)


_PERSONIDMESSAGE = _descriptor.Descriptor(
  name='PersonIdMessage',
  full_name='PersonIdMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='PersonIdMessage.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=160,
  serialized_end=189,
)


_EMPTYMESSAGE = _descriptor.Descriptor(
  name='EmptyMessage',
  full_name='EmptyMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=191,
  serialized_end=205,
)

_PERSONLISTMESSAGE.fields_by_name['persons'].message_type = _PERSONMESSAGE
DESCRIPTOR.message_types_by_name['PersonMessage'] = _PERSONMESSAGE
DESCRIPTOR.message_types_by_name['PersonListMessage'] = _PERSONLISTMESSAGE
DESCRIPTOR.message_types_by_name['PersonIdMessage'] = _PERSONIDMESSAGE
DESCRIPTOR.message_types_by_name['EmptyMessage'] = _EMPTYMESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PersonMessage = _reflection.GeneratedProtocolMessageType('PersonMessage', (_message.Message,), {
  'DESCRIPTOR' : _PERSONMESSAGE,
  '__module__' : 'person_pb2'
  # @@protoc_insertion_point(class_scope:PersonMessage)
  })
_sym_db.RegisterMessage(PersonMessage)

PersonListMessage = _reflection.GeneratedProtocolMessageType('PersonListMessage', (_message.Message,), {
  'DESCRIPTOR' : _PERSONLISTMESSAGE,
  '__module__' : 'person_pb2'
  # @@protoc_insertion_point(class_scope:PersonListMessage)
  })
_sym_db.RegisterMessage(PersonListMessage)

PersonIdMessage = _reflection.GeneratedProtocolMessageType('PersonIdMessage', (_message.Message,), {
  'DESCRIPTOR' : _PERSONIDMESSAGE,
  '__module__' : 'person_pb2'
  # @@protoc_insertion_point(class_scope:PersonIdMessage)
  })
_sym_db.RegisterMessage(PersonIdMessage)

EmptyMessage = _reflection.GeneratedProtocolMessageType('EmptyMessage', (_message.Message,), {
  'DESCRIPTOR' : _EMPTYMESSAGE,
  '__module__' : 'person_pb2'
  # @@protoc_insertion_point(class_scope:EmptyMessage)
  })
_sym_db.RegisterMessage(EmptyMessage)



_PERSONSERVICE = _descriptor.ServiceDescriptor(
  name='PersonService',
  full_name='PersonService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=208,
  serialized_end=351,
  methods=[
  _descriptor.MethodDescriptor(
    name='Create',
    full_name='PersonService.Create',
    index=0,
    containing_service=None,
    input_type=_PERSONMESSAGE,
    output_type=_PERSONMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Get',
    full_name='PersonService.Get',
    index=1,
    containing_service=None,
    input_type=_PERSONIDMESSAGE,
    output_type=_PERSONMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetAll',
    full_name='PersonService.GetAll',
    index=2,
    containing_service=None,
    input_type=_EMPTYMESSAGE,
    output_type=_PERSONLISTMESSAGE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_PERSONSERVICE)

DESCRIPTOR.services_by_name['PersonService'] = _PERSONSERVICE

# @@protoc_insertion_point(module_scope)
