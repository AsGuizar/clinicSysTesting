# 🏥 Clinic System - gRPC Service

A clinic management system built with gRPC and Protocol Buffers, featuring patient, doctor, and appointment management with SQLite persistence.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
---

## 🎯 Overview

This clinic management system provides a robust client-server architecture for healthcare data management:

- **Fast RPC Communication**: Built on gRPC for efficient, low-latency operations
- **Type-Safe Protocol**: Protocol Buffers ensure consistent data structures
- **Centralized Data**: Single SQLite database for data integrity
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Network-Ready**: Designed for local network deployment

---

## 🏗 Architecture

| Component | Technology | Description |
|-----------|-----------|-------------|
| **Protocol Definition** | gRPC / Protocol Buffers | Service interfaces and data structures (`clinic.proto`) |
| **Server** | Python 3.x | Handles RPC requests, manages database operations |
| **Database** | SQLite | Persistent storage for all clinic data |
| **Client** | Python 3.x | User interface for executing CRUD operations |
| **Network** | TCP/IP | Communicates over port 50051 |

```
┌─────────────┐         gRPC/TCP          ┌─────────────┐
│   Client    │ ◄────────────────────────► │   Server    │
│  (Any IP)   │      Port 50051            │ (Host IP)   │
└─────────────┘                            └──────┬──────┘
                                                  │
                                           ┌──────▼──────┐
                                           │  clinic.db  │
                                           │   (SQLite)  │
                                           └─────────────┘
```

---

## ✅ Prerequisites

- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **Network Access**: Local network connectivity between client and server
- **Firewall**: Permission to open port 50051 (server only)

---

## 🚀 Installation

### Step 1: Verify Project Structure

Ensure your directory structure matches the following:

```
clinicSys/
├── .venv/                  # Virtual environment (created in Step 2)
├── citesys/
│   ├── __pycache__/       # Auto-generated
│   ├── client.py
│   ├── clinic.proto
│   ├── clinic_pb2.py      # Generated (Step 4)
│   ├── clinic_pb2.pyi     # Generated (Step 4)
│   ├── clinic_pb2_grpc.py # Generated (Step 4)
│   ├── clinic.db          # Created on first server run
│   └── server.py
├── Include/               # Virtual environment files
├── Lib/                   # Virtual environment files
├── Scripts/               # Virtual environment files
├── .gitignore
├── pyenv.cfg
└── requirements.txt
```

### Step 2: Create Virtual Environment

Navigate to the project root and create an isolated Python environment:

```bash
# From /clinicSys directory
python -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (Git Bash/MINGW64):**
```bash
source .venv/Scripts/activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` prefix in your terminal prompt.

### Step 4: Install Dependencies

```bash
(.venv) pip install -r requirements.txt
```

**Expected packages:**
- `grpcio` - gRPC runtime
- `grpcio-tools` - Protocol buffer compiler
- `protobuf` - Protocol buffer support

### Step 5: Generate Protocol Buffer Code

⚠️ **Critical Step**: This must be run from the project root directory.

```bash
(.venv) python -m grpc_tools.protoc -I citesys --python_out=citesys --pyi_out=citesys --grpc_python_out=citesys citesys/clinic.proto
```

**Generated files:**
- `clinic_pb2.py` - Message classes
- `clinic_pb2.pyi` - Type hints
- `clinic_pb2_grpc.py` - Service stubs

---

## ⚙️ Configuration

### For Server Host (Machine Running the Database)

#### 1. Configure Firewall

The server listens on `0.0.0.0:50051`, which means all network interfaces. You must allow incoming connections:

**Windows Firewall:**
```powershell
# Run PowerShell as Administrator
New-NetFirewallRule -DisplayName "Clinic gRPC Server" -Direction Inbound -Protocol TCP -LocalPort 50051 -Action Allow
```

**Linux (ufw):**
```bash
sudo ufw allow 50051/tcp
sudo ufw reload
```

**macOS:**
System Preferences → Security & Privacy → Firewall → Firewall Options → Add port 50051

#### 2. Find Your IP Address

Clients need your machine's local IP address to connect.

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" (e.g., `192.168.1.100`)

**macOS/Linux:**
```bash
ip addr show  # Linux
ifconfig      # macOS
```

**Share this IP with all client users.**

### For Client Users

#### Update Server Connection

Edit `citesys/client.py` and replace the placeholder IP:

```python
class ClinicClient:
    def __init__(self):
        # Replace with the actual server IP address
        # Example: self.channel = grpc.insecure_channel('192.168.1.100:50051')
        self.channel = grpc.insecure_channel('SERVER_HOST_IP:50051')
        self.stub = clinic_pb2_grpc.ClinicServiceStub(self.channel)
```

**Example configuration:**
```python
self.channel = grpc.insecure_channel('192.168.1.100:50051')
```

---

## 🎮 Usage

### Starting the Server

On the **server host machine**, from the project root:

```bash
(.venv) python citesys/server.py
```

**Expected output:**
```
Server started on port 50051
```

The server will:
- Create `citesys/clinic.db` if it doesn't exist
- Initialize database tables
- Begin listening for client connections

### Running the Client

On any **client machine**, from the project root:

```bash
(.venv) python citesys/client.py
```

The client will connect to the server and execute defined operations.

---
