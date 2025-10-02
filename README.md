🏥 Clinic System - gRPC ServiceA fast, language-agnostic Inter-Process Communication (IPC) system for managing patient, doctor, and appointment data, using gRPC (Protocol Buffers) and SQLite for persistence.📖 OverviewComponentTechnologyRoleProtocolgRPC / Protocol BuffersDefines service interfaces and data structures (clinic.proto).ServerPython (server.py)Listens on 0.0.0.0:50051, handles RPCs, and manages the central database.DatabaseSQLite (clinic.db)Single source of truth for all data, located on the Server Host machine.ClientPython (client.py)Connects to the Server Host's specific IP to execute CRUD operations.🚀 Setup & Installation (Mandatory Steps for All Users)These steps must be completed from the ROOT directory (/clinicSystem).1. Project StructureEnsure your file structure matches this diagram to avoid Python import errors:/clinicSystem
├── .venv/
├── citesys/
│   ├── client.py
│   ├── clinic.proto
│   └── server.py
└── requirements.txt

2. Virtual Environment & DependenciesActivate the environment before running any scripts.# Create the environment
python -m venv .venv

# Activate (Use 'source .venv/Scripts/activate' on MINGW64/Git Bash)
source .venv/Scripts/activate

Install all necessary packages:(venv) pip install -r requirements.txt

3. Generate gRPC Code StubsThis command compiles the service definition (clinic.proto) into the Python files required by the server and client. Must be run from the ROOT.(venv) python -m grpc_tools.protoc -I citesys --python_out=citesys --pyi_out=citesys --grpc_python_out=citesys citesys/clinic.proto

(Success will be silent. Two new files: clinic_pb2.py and clinic_pb2_grpc.py will appear in citesys/.)🎯 Role-Based InstructionsA. Server Host MachineThe Server Host must perform the following actions to make the central service available on the network.1. Network ConfigurationThe Server binds to the wildcard IP (0.0.0.0), but the operating system firewall must be configured:Action: Create an inbound rule to allow TCP traffic on port 50051.2. Start the ServerRun the server executable from the ROOT directory:(venv) python citesys/server.py

The server will start listening immediately.3. Share Host IPThe client needs the host's actual local IP address (e.g., 192.168.1.55). The server should be running before you check your IP.Action: Find and share your current IP address (using ipconfig or ip a).B. Client User MachineThe Client User runs the application that consumes the data and logic provided by the Server Host.1. Update Client IPBefore running, update the connection string in the client code (citesys/client.py) with the IP shared by the Server Host.# Inside citesys/client.py
class ClinicClient:
    def __init__(self):
        # REPLACE 'SERVER_HOST_IP' with the actual IP address provided by the Server Host
        self.channel = grpc.insecure_channel('SERVER_HOST_IP:50051') 
        self.stub = clinic_pb2_grpc.ClinicServiceStub(self.channel)

2. Run the ClientExecute the client application from the ROOT directory:(venv) python citesys/client.py

The client will connect, send RPCs, and display the results, which are all stored centrally on the Server Host's clinic.db file.
