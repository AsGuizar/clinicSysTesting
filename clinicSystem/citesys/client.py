import grpc
import clinic_pb2
import clinic_pb2_grpc

class ClinicClient:
    def __init__(self):

        self.channel = grpc.insecure_channel('192.168.1.23:50051')
        self.stub = clinic_pb2_grpc.ClinicServiceStub(self.channel)
    
    def clear_screen(self):
        print("\n" * 2)
    
    # === MENÚ PRINCIPAL ===
    def main_menu(self):
        while True:
            print("\n" + "="*50)
            print("🏥 SISTEMA DE CITAS MÉDICAS")
            print("="*50)
            print("1. 👤 Gestión de Pacientes")
            print("2. 👨‍⚕️ Gestión de Doctores")
            print("3. 📅 Gestión de Citas")
            print("4. 🚪 Salir")
            print("="*50)
            
            choice = input("Elige una opción: ").strip()
            
            if choice == '1':
                self.patient_menu()
            elif choice == '2':
                self.doctor_menu()
            elif choice == '3':
                self.appointment_menu()
            elif choice == '4':
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción inválida")
    
    # === MENÚ DE PACIENTES ===
    def patient_menu(self):
        while True:
            self.clear_screen()
            print("\n--- 👤 GESTIÓN DE PACIENTES ---")
            print("1. Crear paciente")
            print("2. Ver paciente")
            print("3. Listar pacientes")
            print("4. Actualizar paciente")
            print("5. Eliminar paciente")
            print("6. Volver")
            
            choice = input("Opción: ").strip()
            
            if choice == '1':
                self.create_patient()
            elif choice == '2':
                self.get_patient()
            elif choice == '3':
                self.list_patients()
            elif choice == '4':
                self.update_patient()
            elif choice == '5':
                self.delete_patient()
            elif choice == '6':
                break
            else:
                print("❌ Opción inválida")
    
    def create_patient(self):
        print("\n--- Crear Paciente ---")
        name = input("Nombre: ").strip()
        age = int(input("Edad: ").strip())
        contact = input("Contacto: ").strip()
        
        patient = clinic_pb2.Patient(name=name, age=age, contact=contact)
        response = self.stub.CreatePatient(patient)
        
        if response.success:
            print(f"✅ {response.message} (ID: {response.id})")
        else:
            print(f"❌ {response.message}")
        input("\nPresiona Enter para continuar...")
    
    def get_patient(self):
        print("\n--- Ver Paciente ---")
        patient_id = int(input("ID del paciente: ").strip())
        
        try:
            patient = self.stub.GetPatient(clinic_pb2.PatientId(id=patient_id))
            print(f"\n📋 ID: {patient.id}")
            print(f"   Nombre: {patient.name}")
            print(f"   Edad: {patient.age}")
            print(f"   Contacto: {patient.contact}")
        except grpc.RpcError as e:
            print(f"❌ {e.details()}")
        input("\nPresiona Enter para continuar...")
    
    def list_patients(self):
        print("\n--- Lista de Pacientes ---")
        response = self.stub.ListPatients(clinic_pb2.Empty())
        
        if not response.patients:
            print("⚠️ No hay pacientes registrados")
        else:
            for p in response.patients:
                print(f"ID: {p.id} | {p.name} | {p.age} años | {p.contact}")
        input("\nPresiona Enter para continuar...")
    
    def update_patient(self):
        print("\n--- Actualizar Paciente ---")
        patient_id = int(input("ID del paciente: ").strip())
        name = input("Nuevo nombre: ").strip()
        age = int(input("Nueva edad: ").strip())
        contact = input("Nuevo contacto: ").strip()
        
        patient = clinic_pb2.Patient(id=patient_id, name=name, age=age, contact=contact)
        response = self.stub.UpdatePatient(patient)
        
        if response.success:
            print(f"✅ {response.message}")
        else:
            print(f"❌ {response.message}")
        input("\nPresiona Enter para continuar...")
    
    def delete_patient(self):
        print("\n--- Eliminar Paciente ---")
        patient_id = int(input("ID del paciente: ").strip())
        
        response = self.stub.DeletePatient(clinic_pb2.PatientId(id=patient_id))
        
        if response.success:
            print(f"✅ {response.message}")
        else:
            print(f"❌ {response.message}")
        input("\nPresiona Enter para continuar...")
    
    # === MENÚ DE DOCTORES ===
    def doctor_menu(self):
        while True:
            self.clear_screen()
            print("\n--- 👨‍⚕️ GESTIÓN DE DOCTORES ---")
            print("1. Crear doctor")
            print("2. Ver doctor")
            print("3. Listar doctores")
            print("4. Actualizar doctor")
            print("5. Eliminar doctor")
            print("6. Volver")
            
            choice = input("Opción: ").strip()
            
            if choice == '1':
                self.create_doctor()
            elif choice == '2':
                self.get_doctor()
            elif choice == '3':
                self.list_doctors()
            elif choice == '4':
                self.update_doctor()
            elif choice == '5':
                self.delete_doctor()
            elif choice == '6':
                break
            else:
                print("❌ Opción inválida")
    
    def create_doctor(self):
        print("\n--- Crear Doctor ---")
        name = input("Nombre: ").strip()
        specialty = input("Especialidad: ").strip()
        
        doctor = clinic_pb2.Doctor(name=name, specialty=specialty)
        response = self.stub.CreateDoctor(doctor)
        
        if response.success:
            print(f"✅ {response.message} (ID: {response.id})")
        else:
            print(f"❌ {response.message}")
        input("\nPresiona Enter para continuar...")
    
    def get_doctor(self):
        print("\n--- Ver Doctor ---")
        doctor_id = int(input("ID del doctor: ").strip())
        
        try:
            doctor = self.stub.GetDoctor(clinic_pb2.DoctorId(id=doctor_id))
            print(f"\n📋 ID: {doctor.id}")
            print(f"   Nombre: {doctor.name}")
            print(f"   Especialidad: {doctor.specialty}")
        except grpc.RpcError as e:
            print(f"❌ {e.details()}")
        input("\nPresiona Enter para continuar...")
    
    def list_doctors(self):
        print("\n--- Lista de Doctores ---")
        response = self.stub.ListDoctors(clinic_pb2.Empty())
        
        if not response.doctors:
            print("⚠️ No hay doctores registrados")
        else:
            for d in response.doctors:
                print(f"ID: {d.id} | {d.name} | {d.specialty}")
        input("\nPresiona Enter para continuar...")
    
    def update_doctor(self):
        print("\n--- Actualizar Doctor ---")
        doctor_id = int(input("ID del doctor: ").strip())
        name = input("Nuevo nombre: ").strip()
        specialty = input("Nueva especialidad: ").strip()
        
        doctor = clinic_pb2.Doctor(id=doctor_id, name=name, specialty=specialty)
        response = self.stub.UpdateDoctor(doctor)
        
        if response.success:
            print(f"✅ {response.message}")
        else:
            print(f"❌ {response.message}")
        input("\nPresiona Enter para continuar...")
    
    def delete_doctor(self):
        print("\n--- Eliminar Doctor ---")
        doctor_id = int(input("ID del doctor: ").strip())
        
        response = self.stub.DeleteDoctor(clinic_pb2.DoctorId(id=doctor_id))
        
        if response.success:
            print(f"✅ {response.message}")
        else:
            print(f"❌ {response.message}")
        input("\nPresiona Enter para continuar...")
    
    # === MENÚ DE CITAS ===
    def appointment_menu(self):
        while True:
            self.clear_screen()
            print("\n--- 📅 GESTIÓN DE CITAS ---")
            print("1. Crear cita")
            print("2. Ver cita")
            print("3. Listar citas")
            print("4. Actualizar cita")
            print("5. Eliminar cita")
            print("6. Volver")
            
            choice = input("Opción: ").strip()
            
            if choice == '1':
                self.create_appointment()
            elif choice == '2':
                self.get_appointment()
            elif choice == '3':
                self.list_appointments()
            elif choice == '4':
                self.update_appointment()
            elif choice == '5':
                self.delete_appointment()
            elif choice == '6':
                break
            else:
                print("❌ Opción inválida")
    
    def create_appointment(self):
        print("\n--- Crear Cita ---")
        patient_id = int(input("ID del paciente: ").strip())
        doctor_id = int(input("ID del doctor: ").strip())
        date = input("Fecha (YYYY-MM-DD HH:MM): ").strip()
        reason = input("Motivo: ").strip()
        
        appointment = clinic_pb2.Appointment(
            patient_id=patient_id, doctor_id=doctor_id, date=date, reason=reason
        )
        response = self.stub.CreateAppointment(appointment)
        
        if response.success:
            print(f"✅ {response.message} (ID: {response.id})")
        else:
            print(f"❌ {response.message}")
        input("\nPresiona Enter para continuar...")
    
    def get_appointment(self):
        print("\n--- Ver Cita ---")
        appointment_id = int(input("ID de la cita: ").strip())
        
        try:
            appointment = self.stub.GetAppointment(clinic_pb2.AppointmentId(id=appointment_id))
            print(f"\n📋 ID: {appointment.id}")
            print(f"   Paciente ID: {appointment.patient_id}")
            print(f"   Doctor ID: {appointment.doctor_id}")
            print(f"   Fecha: {appointment.date}")
            print(f"   Motivo: {appointment.reason}")
        except grpc.RpcError as e:
            print(f"❌ {e.details()}")
        input("\nPresiona Enter para continuar...")
    
    def list_appointments(self):
        print("\n--- Lista de Citas ---")
        response = self.stub.ListAppointments(clinic_pb2.Empty())
        
        if not response.appointments:
            print("⚠️ No hay citas registradas")
        else:
            for a in response.appointments:
                print(f"ID: {a.id} | Paciente: {a.patient_id} | Doctor: {a.doctor_id} | {a.date} | {a.reason}")
        input("\nPresiona Enter para continuar...")
    
    def update_appointment(self):
        print("\n--- Actualizar Cita ---")
        appointment_id = int(input("ID de la cita: ").strip())
        patient_id = int(input("Nuevo ID del paciente: ").strip())
        doctor_id = int(input("Nuevo ID del doctor: ").strip())
        date = input("Nueva fecha (YYYY-MM-DD HH:MM): ").strip()
        reason = input("Nuevo motivo: ").strip()
        
        appointment = clinic_pb2.Appointment(
            id=appointment_id, patient_id=patient_id, doctor_id=doctor_id, date=date, reason=reason
        )
        response = self.stub.UpdateAppointment(appointment)
        
        if response.success:
            print(f"✅ {response.message}")
        else:
            print(f"❌ {response.message}")
        input("\nPresiona Enter para continuar...")
    
    def delete_appointment(self):
        print("\n--- Eliminar Cita ---")
        appointment_id = int(input("ID de la cita: ").strip())
        
        response = self.stub.DeleteAppointment(clinic_pb2.AppointmentId(id=appointment_id))
        
        if response.success:
            print(f"✅ {response.message}")
        else:
            print(f"❌ {response.message}")
        input("\nPresiona Enter para continuar...")


if __name__ == '__main__':
    client = ClinicClient()
    try:
        client.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")