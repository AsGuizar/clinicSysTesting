from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Patient(_message.Message):
    __slots__ = ("id", "name", "age", "contact")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    age: int
    contact: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., age: _Optional[int] = ..., contact: _Optional[str] = ...) -> None: ...

class Doctor(_message.Message):
    __slots__ = ("id", "name", "specialty")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SPECIALTY_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    specialty: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., specialty: _Optional[str] = ...) -> None: ...

class Appointment(_message.Message):
    __slots__ = ("id", "patient_id", "doctor_id", "date", "reason")
    ID_FIELD_NUMBER: _ClassVar[int]
    PATIENT_ID_FIELD_NUMBER: _ClassVar[int]
    DOCTOR_ID_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    id: int
    patient_id: int
    doctor_id: int
    date: str
    reason: str
    def __init__(self, id: _Optional[int] = ..., patient_id: _Optional[int] = ..., doctor_id: _Optional[int] = ..., date: _Optional[str] = ..., reason: _Optional[str] = ...) -> None: ...

class PatientId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class DoctorId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class AppointmentId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class PatientList(_message.Message):
    __slots__ = ("patients",)
    PATIENTS_FIELD_NUMBER: _ClassVar[int]
    patients: _containers.RepeatedCompositeFieldContainer[Patient]
    def __init__(self, patients: _Optional[_Iterable[_Union[Patient, _Mapping]]] = ...) -> None: ...

class DoctorList(_message.Message):
    __slots__ = ("doctors",)
    DOCTORS_FIELD_NUMBER: _ClassVar[int]
    doctors: _containers.RepeatedCompositeFieldContainer[Doctor]
    def __init__(self, doctors: _Optional[_Iterable[_Union[Doctor, _Mapping]]] = ...) -> None: ...

class AppointmentList(_message.Message):
    __slots__ = ("appointments",)
    APPOINTMENTS_FIELD_NUMBER: _ClassVar[int]
    appointments: _containers.RepeatedCompositeFieldContainer[Appointment]
    def __init__(self, appointments: _Optional[_Iterable[_Union[Appointment, _Mapping]]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("success", "message", "id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    id: int
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...
