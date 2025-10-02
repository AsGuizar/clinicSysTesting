import grpc
from concurrent import futures
import sqlite3
import clinic_pb2
import clinic_pb2_grpc

# ========== BASE DE DATOS ==========
class Database:
    def __init__(self, db_name="clinic.db"):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de pacientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                contact TEXT
            )
        ''')
        
        # Tabla de doctores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialty TEXT
            )
        ''')
        
        # Tabla de citas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                date TEXT,
                reason TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Base de datos inicializada")
    
    # === PACIENTES ===
    def add_patient(self, name, age, contact):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, contact) VALUES (?, ?, ?)", 
                      (name, age, contact))
        conn.commit()
        patient_id = cursor.lastrowid
        conn.close()
        return patient_id
    
    def get_patient(self, patient_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def list_patients(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def update_patient(self, patient_id, name, age, contact):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET name = ?, age = ?, contact = ? WHERE id = ?",
                      (name, age, contact, patient_id))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    def delete_patient(self, patient_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    # === DOCTORES ===
    def add_doctor(self, name, specialty):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctors (name, specialty) VALUES (?, ?)", 
                      (name, specialty))
        conn.commit()
        doctor_id = cursor.lastrowid
        conn.close()
        return doctor_id
    
    def get_doctor(self, doctor_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def list_doctors(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def update_doctor(self, doctor_id, name, specialty):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE doctors SET name = ?, specialty = ? WHERE id = ?",
                      (name, specialty, doctor_id))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    def delete_doctor(self, doctor_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    # === CITAS ===
    def add_appointment(self, patient_id, doctor_id, date, reason):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO appointments (patient_id, doctor_id, date, reason) VALUES (?, ?, ?, ?)",
                      (patient_id, doctor_id, date, reason))
        conn.commit()
        appointment_id = cursor.lastrowid
        conn.close()
        return appointment_id
    
    def get_appointment(self, appointment_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
        row = cursor.fetchone()
        conn.close()
        return row
    
    def list_appointments(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def update_appointment(self, appointment_id, patient_id, doctor_id, date, reason):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET patient_id = ?, doctor_id = ?, date = ?, reason = ? WHERE id = ?",
                      (patient_id, doctor_id, date, reason, appointment_id))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    def delete_appointment(self, appointment_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0


# ========== SERVIDOR gRPC ==========
class ClinicService(clinic_pb2_grpc.ClinicServiceServicer):
    def __init__(self):
        self.db = Database()
    
    # === PACIENTES ===
    def CreatePatient(self, request, context):
        try:
            patient_id = self.db.add_patient(request.name, request.age, request.contact)
            return clinic_pb2.Response(success=True, message="Paciente creado", id=patient_id)
        except Exception as e:
            return clinic_pb2.Response(success=False, message=f"Error: {str(e)}")
    
    def GetPatient(self, request, context):
        row = self.db.get_patient(request.id)
        if row:
            return clinic_pb2.Patient(id=row[0], name=row[1], age=row[2], contact=row[3])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Paciente no encontrado")
            return clinic_pb2.Patient()
    
    def ListPatients(self, request, context):
        rows = self.db.list_patients()
        patients = [clinic_pb2.Patient(id=r[0], name=r[1], age=r[2], contact=r[3]) for r in rows]
        return clinic_pb2.PatientList(patients=patients)
    
    def UpdatePatient(self, request, context):
        success = self.db.update_patient(request.id, request.name, request.age, request.contact)
        if success:
            return clinic_pb2.Response(success=True, message="Paciente actualizado")
        else:
            return clinic_pb2.Response(success=False, message="Paciente no encontrado")
    
    def DeletePatient(self, request, context):
        success = self.db.delete_patient(request.id)
        if success:
            return clinic_pb2.Response(success=True, message="Paciente eliminado")
        else:
            return clinic_pb2.Response(success=False, message="Paciente no encontrado")
    
    # === DOCTORES ===
    def CreateDoctor(self, request, context):
        try:
            doctor_id = self.db.add_doctor(request.name, request.specialty)
            return clinic_pb2.Response(success=True, message="Doctor creado", id=doctor_id)
        except Exception as e:
            return clinic_pb2.Response(success=False, message=f"Error: {str(e)}")
    
    def GetDoctor(self, request, context):
        row = self.db.get_doctor(request.id)
        if row:
            return clinic_pb2.Doctor(id=row[0], name=row[1], specialty=row[2])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Doctor no encontrado")
            return clinic_pb2.Doctor()
    
    def ListDoctors(self, request, context):
        rows = self.db.list_doctors()
        doctors = [clinic_pb2.Doctor(id=r[0], name=r[1], specialty=r[2]) for r in rows]
        return clinic_pb2.DoctorList(doctors=doctors)
    
    def UpdateDoctor(self, request, context):
        success = self.db.update_doctor(request.id, request.name, request.specialty)
        if success:
            return clinic_pb2.Response(success=True, message="Doctor actualizado")
        else:
            return clinic_pb2.Response(success=False, message="Doctor no encontrado")
    
    def DeleteDoctor(self, request, context):
        success = self.db.delete_doctor(request.id)
        if success:
            return clinic_pb2.Response(success=True, message="Doctor eliminado")
        else:
            return clinic_pb2.Response(success=False, message="Doctor no encontrado")
    
    # === CITAS ===
    def CreateAppointment(self, request, context):
        try:
            appointment_id = self.db.add_appointment(
                request.patient_id, request.doctor_id, request.date, request.reason
            )
            return clinic_pb2.Response(success=True, message="Cita creada", id=appointment_id)
        except Exception as e:
            return clinic_pb2.Response(success=False, message=f"Error: {str(e)}")
    
    def GetAppointment(self, request, context):
        row = self.db.get_appointment(request.id)
        if row:
            return clinic_pb2.Appointment(
                id=row[0], patient_id=row[1], doctor_id=row[2], date=row[3], reason=row[4]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Cita no encontrada")
            return clinic_pb2.Appointment()
    
    def ListAppointments(self, request, context):
        rows = self.db.list_appointments()
        appointments = [
            clinic_pb2.Appointment(id=r[0], patient_id=r[1], doctor_id=r[2], date=r[3], reason=r[4])
            for r in rows
        ]
        return clinic_pb2.AppointmentList(appointments=appointments)
    
    def UpdateAppointment(self, request, context):
        success = self.db.update_appointment(
            request.id, request.patient_id, request.doctor_id, request.date, request.reason
        )
        if success:
            return clinic_pb2.Response(success=True, message="Cita actualizada")
        else:
            return clinic_pb2.Response(success=False, message="Cita no encontrada")
    
    def DeleteAppointment(self, request, context):
        success = self.db.delete_appointment(request.id)
        if success:
            return clinic_pb2.Response(success=True, message="Cita eliminada")
        else:
            return clinic_pb2.Response(success=False, message="Cita no encontrada")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    clinic_pb2_grpc.add_ClinicServiceServicer_to_server(ClinicService(), server)
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    print("🏥 Servidor gRPC corriendo en puerto 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()