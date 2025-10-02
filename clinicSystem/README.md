🏥 Clinic System - gRPC Service
This repository contains the core files for the Clinic System, implemented using gRPC (Google Remote Procedure Call). The system includes a Python-based server and client that communicate using protocol buffers defined in clinic.proto.

📂 Project Structure
The core application logic and service definitions are located inside the citesys/ directory.

/clinicSystem
├── .venv/                      # Python virtual environment (ignored by Git)
├── citesys/
│   ├── client.py               # gRPC client application
│   ├── clinic.proto            # Protocol buffer definition file (Service definition)
│   └── server.py               # gRPC server implementation
├── .gitignore                  # Specifies files/folders to ignore (e.g., .venv)
└── requirements.txt            # List of required Python dependencies

🚀 Setup & Installation (Start Here!)
Follow these steps to set up the project environment on your local machine.

1. Clone the Repository
git clone [https://github.com/AsGuizar/clinicSystem.git](https://github.com/AsGuizar/clinicSystem.git)
cd clinicSystem

2. Create and Activate the Virtual Environment
It is crucial to work inside an isolated virtual environment (.venv).

# Create the environment
python -m venv .venv

# Activate the environment (choose based on your OS/Shell):
# Windows (PowerShell/CMD):
.venv\Scripts\activate
# macOS/Linux (Git Bash):
source .venv/bin/activate

(Your terminal prompt should now show (.venv) to indicate activation.)

3. Install Dependencies
Install the required Python packages (including grpcio and protobuf) using the requirements.txt file.

pip install -r requirements.txt

4. Generate gRPC Code
The Protocol Buffer definition (clinic.proto) must be compiled to generate the Python stub files (clinic_pb2.py and clinic_pb2_grpc.py).

Note: If you run this from the project root while the .venv is active, it should work immediately.

python -m grpc_tools.protoc -I. --python_out=citesys --pyi_out=citesys --grpc_python_out=citesys citesys/clinic.proto

▶️ Running the Application
1. Start the Server
Open a terminal, ensure the .venv is activated, and run the server.

(venv) python citesys/server.py

Expected Output: Server will start and wait for client connections.

2. Run the Client
Open a separate terminal, ensure the .venv is activated, and run the client.

(venv) python citesys/client.py
