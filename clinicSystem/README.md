🏥 Clinic System - gRPC Service
This repository contains the core files for the Clinic System, implemented using gRPC (Google Remote Procedure Call) and backed by a local SQLite database (clinic.db).

The key to running this project is understanding the difference between the Server (the central data host) and the Client (the user interface).

📁 Project Structure (CRITICAL)
Ensure your files are arranged exactly like this. The citesys folder MUST be a direct child of the root project folder.

/clinicSystem
├── .venv/                      # Python virtual environment
├── citesys/                    # Python source package
│   ├── client.py               # gRPC client application
│   ├── clinic.proto            # Protocol buffer definition file
│   ├── server.py               # gRPC server implementation
│   ├── clinic_pb2.py           # (GENERATED STUB)
│   └── clinic_pb2_grpc.py      # (GENERATED STUB)
├── .gitignore                  # Specifies files/folders to ignore
└── requirements.txt            # List of required Python dependencies

🚀 Setup & Installation (Mandatory First Steps)
Both the Server Host and the Client User must follow these three steps from the root directory of the project (/clinicSystem).

1. Create and Activate the Virtual Environment
You MUST activate the virtual environment (.venv) for every step.

# Create the environment
python -m venv .venv

# Activate the environment (Use the command appropriate for MINGW64/Git Bash):
source .venv/Scripts/activate

(Your terminal prompt must show (.venv).)

2. Install Dependencies
Install the required Python packages (grpcio, protobuf, etc.):

(venv) pip install -r requirements.txt

3. Generate gRPC Code Stubs (Protobuf Compilation)
This step generates the Python files needed for the client and server to talk. This command MUST be run from the ROOT directory.

(venv) python -m grpc_tools.protoc -I citesys --python_out=citesys --pyi_out=citesys --grpc_python_out=citesys citesys/clinic.proto

(If successful, this command will run silently and create clinic_pb2.py and clinic_pb2_grpc.py inside citesys/.)

🎯 Role-Based Instructions
A. The Server Host (Your Machine)
The Server Host is the machine that runs the server process, listens for requests, and manages the central clinic.db file.

1. Configure the Firewall
You must create an inbound rule in your operating system's firewall (e.g., Windows Defender Firewall) to allow TCP traffic on port 50051. This allows other computers on the network to reach your server.

2. Start the Server
Run the server executable from the ROOT directory:

(venv) python citesys/server.py

The server is bound to 0.0.0.0:50051, meaning it listens on all available network interfaces, ensuring it runs even if your IP changes.

3. Share Your IP
While the server listens to 0.0.0.0, the client needs your machine's current local IP address (e.g., 192.168.1.55).

Find your current IP address (e.g., using ipconfig on Windows or ip a on Linux/Mac).

Share this IP address with the Client User.

B. The Client User (Collaborator's Machine)
The Client User runs the client application to send requests to the Server Host.

1. Update the Client IP
Before running, the client's connection string must be updated to the Server Host's current local IP address.

In citesys/client.py, change the IP address in the __init__ method:

# Inside citesys/client.py
class ClinicClient:
    def __init__(self):
        # REPLACE 'SERVER_HOST_IP' with the actual IP address provided by the Server Host
        self.channel = grpc.insecure_channel('SERVER_HOST_IP:50051') 
        self.stub = clinic_pb2_grpc.ClinicServiceStub(self.channel)

2. Run the Client
Run the client executable from the ROOT directory:

(venv) python citesys/client.py

If successful, the client will connect to the server, send RPC calls, and display the results.
