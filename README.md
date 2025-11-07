# Task Management System - Architecture Comparison Project

## 🚀 Quick Start

### Option 1: Layered Monolith (Recommended - Selected Architecture)

```bash
cd Selected
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Access the application**: http://localhost:5000

### Option 2: Microservices Architecture

**Prerequisites**: Docker Desktop must be installed and running.

```bash
cd Unselected
docker compose up --build
```

**Access the application**: http://localhost:5003

---

## 📋 Table of Contents

1. [Implementation Platform & Requirements](#implementation-platform--requirements)
2. [Platform Installation & Configuration](#platform-installation--configuration)
3. [How to Compile](#how-to-compile)
4. [How to Execute](#how-to-execute)
5. [Architecture Comparison](#architecture-comparison)
6. [Rationale for Architecture Selection](#rationale-for-architecture-selection)
7. [Project Overview](#project-overview)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)

---

## Implementation Platform & Requirements

### Primary Implementation Platform

**Platform**: Python 3.11 with Flask Framework  
**Version**: Python 3.11.x (3.11.0 or later)  
**Download**: https://www.python.org/downloads/

### Framework & Libraries

- **Flask**: 3.0.0 (Web Framework)
- **Flask-SQLAlchemy**: 3.1.1 (Database ORM Integration)
- **SQLAlchemy**: 2.0.23 (Object-Relational Mapping)
- **Werkzeug**: 3.0.1 (WSGI Utility Library)
- **pytest**: 7.4.3 (Testing Framework)
- **Flask-Testing**: 0.8.1 (Flask Testing Utilities)
- **requests**: 2.31.0 (HTTP Library for Microservices Communication)

### Operating System Support

- **macOS**: 10.15 (Catalina) or later
- **Windows**: Windows 10 or later  
- **Linux**: Ubuntu 20.04 LTS or later, or any modern Linux distribution

### Additional Requirements (Microservices Only)

- **Docker**: Version 24.0+ 
- **Docker Compose**: Version 2.20+ (included with Docker Desktop)
- **Download**: https://www.docker.com/products/docker-desktop/

---

## Platform Installation & Configuration

### Step 1: Install Python 3.11

#### Download Links

- **macOS/Linux**: https://www.python.org/downloads/
- **Windows**: https://www.python.org/downloads/windows/

#### Installation Instructions

**macOS**:
1. Download Python 3.11 from https://www.python.org/downloads/
2. Run the installer package (.pkg file)
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```bash
   python3 --version
   # Should output: Python 3.11.x
   ```

**Windows**:
1. Download Python 3.11 Windows installer from https://www.python.org/downloads/windows/
2. Run the installer (.exe file)
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```bash
   python --version
   # Should output: Python 3.11.x
   ```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3.11 --version
```

### Step 2: Install pip (Python Package Manager)

pip usually comes with Python 3.11. Verify installation:
```bash
pip3 --version
# Should output: pip 23.x.x or later
```

If pip is not installed:
```bash
# macOS/Linux
python3 -m ensurepip --upgrade

# Windows
python -m ensurepip --upgrade
```

### Step 3: Install Docker & Docker Compose (For Microservices Architecture Only)

**Download**: https://www.docker.com/products/docker-desktop/

**Installation Instructions**:

**macOS/Windows**:
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Install and launch Docker Desktop
3. Wait for Docker to start (whale icon in system tray/menu bar)
4. Verify installation:
   ```bash
   docker --version
   docker compose version
   ```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
# Log out and log back in for group changes to take effect
```

### Step 4: Configure Virtual Environment (Layered Monolith)

After installing Python 3.11, create a virtual environment to isolate project dependencies:

```bash
cd Selected
python3 -m venv venv
```

**Activate virtual environment**:
- **macOS/Linux**: `source venv/bin/activate`
- **Windows (Command Prompt)**: `venv\Scripts\activate`
- **Windows (PowerShell)**: `venv\Scripts\Activate.ps1`

You should see `(venv)` in your terminal prompt when activated.

**Note for Windows PowerShell**: If you encounter execution policy errors, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 5: Docker Configuration (Microservices)

No additional configuration needed if Docker Desktop is installed and running. Docker Compose will handle all service orchestration automatically.

---

## How to Compile

### Note on Python Compilation

Python is an interpreted language, so there is no traditional "compilation" step. However, we need to:
1. Install dependencies
2. Set up virtual environments
3. Initialize databases (automatic on first run)

### Layered Monolith Architecture

#### Step 1: Navigate to Selected Directory
```bash
cd Selected
```

#### Step 2: Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv

# Windows
python -m venv venv
```

#### Step 3: Activate Virtual Environment
```bash
# macOS/Linux
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

You should see `(venv)` in your terminal prompt.

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- SQLAlchemy==2.0.23
- Werkzeug==3.0.1
- pytest==7.4.3
- Flask-Testing==0.8.1
- requests==2.31.0

#### Step 5: Verify Installation
```bash
python -c "import flask; print(flask.__version__)"
# Should output: 3.0.0
```

#### Step 6: Database Initialization

The database will be automatically created on first run. No manual initialization required.

### Microservices Architecture

#### Step 1: Navigate to Unselected Directory
```bash
cd Unselected
```

#### Step 2: Build Docker Images
```bash
docker compose build
```

This will:
- Build User Service image
- Build Task Service image
- Build Notification Service image
- Build Frontend Service image
- Install all dependencies in each container

#### Step 3: Verify Docker Images
```bash
docker images
```

You should see:
- `unselected-user-service`
- `unselected-task-service`
- `unselected-notification-service`
- `unselected-frontend-service`

#### Step 4: Database Initialization

Databases are automatically initialized when services start. Each service has its own database:
- User Service: SQLite database in container
- Task Service: SQLite database in container
- Notification Service: In-memory storage (stateless)

---

## How to Execute

### Layered Monolith Architecture

#### Step 1: Activate Virtual Environment (if not already active)
```bash
cd Selected
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
```

#### Step 2: Run the Application
```bash
python app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

#### Step 3: Access the Application

Open your web browser and navigate to:
- **Dashboard**: http://localhost:5000/
- **Tasks**: http://localhost:5000/tasks
- **Calendar**: http://localhost:5000/calendar

#### Step 4: Stop the Application

Press `CTRL+C` in the terminal to stop the server.

### Microservices Architecture

#### Step 1: Navigate to Unselected Directory
```bash
cd Unselected
```

#### Step 2: Start All Services
```bash
docker compose up --build
```

Or run in detached mode (background):
```bash
docker compose up -d
```

#### Step 3: Verify Services are Running
```bash
docker compose ps
```

You should see all services with status "Up":
- user-service (port 5002)
- task-service (port 5000)
- notification-service (port 5001)
- frontend-service (port 5003)

#### Step 4: Check Service Health
```bash
# User Service
curl http://localhost:5002/health

# Task Service
curl http://localhost:5000/health

# Notification Service
curl http://localhost:5001/health

# Frontend Service
curl http://localhost:5003/health
```

All should return: `{"status":"healthy","service":"..."}`

#### Step 5: Access the Services

**Web Interface**:
- **Frontend (Web UI)**: http://localhost:5003
- **Dashboard**: http://localhost:5003/
- **Tasks**: http://localhost:5003/tasks
- **Calendar**: http://localhost:5003/calendar

**API Services** (backend):
- **User Service API**: http://localhost:5002
- **Task Service API**: http://localhost:5000
- **Notification Service API**: http://localhost:5001

#### Step 6: Stop All Services
```bash
docker compose down
```

To also remove volumes (clears databases):
```bash
docker compose down -v
```

---

## Architecture Comparison

This project implements a task management system using two different architectural approaches:

1. **Layered Monolith (MVC)** - Located in `Selected/` directory (Selected Architecture)
2. **Microservices Architecture** - Located in `Unselected/` directory (Alternative Architecture)

### Detailed Architecture Comparison

#### Layered Monolith (MVC) Architecture

**Structure**:
```
┌─────────────────────────────────────────┐
│     Presentation Layer (Routes)         │
│  - Flask route handlers                 │
│  - Jinja2 templates                     │
│  - Static files (CSS/JS)                │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     Business Logic Layer (Services)     │
│  - TaskService                          │
│  - NotificationService                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     Data Access Layer (Repositories)    │
│  - TaskRepository                       │
│  - UserRepository                       │
│  - ActivityLogRepository                │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│     Data Layer (Models)                 │
│  - SQLAlchemy ORM                       │
│  - SQLite Database                      │
└─────────────────────────────────────────┘
```

**Key Characteristics**:
- **Single Deployable Unit**: All code in one application
- **Four Layers**: Presentation → Business Logic → Data Access → Data
- **Repository Pattern**: Abstracts database operations
- **Shared Database**: Single SQLite database for all entities
- **Internal Communication**: Direct function calls
- **Technology Stack**: Python 3.11, Flask 3.0.0, SQLAlchemy 2.0.23, SQLite

**Advantages**:
1. **Simplicity**: Easy to understand and develop
2. **Rapid Development**: Fast iteration cycles
3. **Easy Testing**: All components in one codebase
4. **Low Overhead**: No network latency between layers
5. **Transaction Management**: ACID transactions across all operations
6. **Single Deployment**: One application to deploy and monitor
7. **Lower Complexity**: No need to manage service communication or orchestration
8. **Easier Debugging**: Single codebase, single log file
9. **Lower Resource Usage**: Single process, lower memory footprint (~50-100MB)
10. **Faster Startup**: Application starts in <1 second

**Disadvantages**:
1. **Scalability**: Harder to scale individual components
2. **Technology Lock-in**: All components use same stack
3. **Fault Isolation**: One bug can affect entire system
4. **Team Coordination**: All developers work on same codebase
5. **Vertical Scaling Only**: Must scale entire application together

#### Microservices Architecture

**Structure**:
```
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  User Service    │      │  Task Service    │      │ Notification     │
│  (Port 5002)     │◄─────┤  (Port 5000)     │─────►│ Service          │
│                  │      │                  │      │ (Port 5001)      │
│  - User CRUD     │      │  - Task CRUD     │      │  - Events        │
│  - Validation    │      │  - Assignments   │      │  - Notifications │
│                  │      │  - Activity Log  │      │  - Alerts        │
│  SQLite DB       │      │  SQLite DB       │      │  In-Memory       │
└──────────────────┘      └──────────────────┘      └──────────────────┘
         ▲                         │
         │                         │
         └─────────────────────────┘
              HTTP REST APIs
                    │
         ┌──────────▼──────────┐
         │  Frontend Service   │
         │  (Port 5003)        │
         │  - Web UI           │
         │  - Aggregates APIs  │
         └─────────────────────┘
```

**Key Characteristics**:
- **Four Independent Services**: User Service, Task Service, Notification Service, Frontend Service
- **Separate Databases**: Each service has its own data store (except Notification Service which is stateless)
- **HTTP Communication**: REST APIs for inter-service communication
- **Containerized**: Docker containers for each service
- **Service Discovery**: Services communicate via Docker service names
- **Independent Deployment**: Each service can be deployed separately
- **Frontend Service**: Separate web interface service (port 5003)

**Advantages**:
1. **Scalability**: Scale each service independently based on demand
2. **Fault Isolation**: Failure in one service doesn't crash others
3. **Technology Flexibility**: Each service can use different technologies
4. **Team Autonomy**: Different teams can work on different services independently
5. **Modularity**: Clear separation of concerns
6. **Independent Scaling**: Scale high-demand services more than others
7. **Horizontal Scaling**: Add more instances of specific services
8. **Service Independence**: Services can be updated/deployed without affecting others

**Disadvantages**:
1. **Complexity**: More moving parts to manage (4 services, networking, orchestration)
2. **Network Latency**: HTTP calls add overhead (1-10ms per call)
3. **Data Consistency**: Harder to maintain consistency across services
4. **Deployment Overhead**: Multiple services to deploy and monitor
5. **Testing Complexity**: Integration testing is more complex
6. **Debugging**: Distributed tracing needed across services
7. **Infrastructure Requirements**: Requires Docker and orchestration knowledge
8. **Higher Resource Usage**: Multiple processes, higher memory footprint (~200-300MB total)
9. **Slower Startup**: Docker + 4 services take longer to start
10. **Network Failure Points**: Services depend on network connectivity

### Detailed Comparison Table

| Aspect | Layered Monolith | Microservices |
|--------|-----------------|---------------|
| **Deployment** | Single application | 4 separate services |
| **Database** | 1 SQLite database | 3 separate databases (User, Task, Notification is stateless) |
| **Communication** | Function calls (in-process) | HTTP REST APIs (network) |
| **Scalability** | Vertical scaling (entire app) | Horizontal scaling per service |
| **Fault Tolerance** | Single point of failure | Isolated failures |
| **Development Speed** | Fast (single codebase) | Slower (coordination needed) |
| **Testing** | Simple (unit + integration) | Complex (service + integration) |
| **Technology Stack** | Fixed (Python/Flask) | Flexible per service |
| **Team Size** | Small teams (1-3) | Larger teams (3+) |
| **Network Calls** | None (internal) | Multiple HTTP calls |
| **Transaction Management** | ACID across all operations | Eventual consistency |
| **Monitoring** | Single application log | Multiple service logs |
| **Setup Complexity** | Low (pip install) | Medium (Docker required) |
| **Startup Time** | Fast (<1 second) | Slower (Docker + 4 services) |
| **Memory Footprint** | Low (~50-100MB) | Higher (~200-300MB total) |
| **Debugging** | Simple (single codebase) | Complex (distributed) |
| **Data Consistency** | Strong (ACID) | Eventual (requires coordination) |
| **Deployment Frequency** | Single deployment | Multiple deployments |
| **Learning Curve** | Low | Medium-High |

### Architecture Design Decisions

#### Layered Monolith Design Decisions

**1. Four-Layer Architecture**
- **Decision**: Presentation → Business Logic → Data Access → Data
- **Rationale**: 
  - Clear separation of concerns
  - Testability (each layer can be tested independently)
  - Maintainability (changes isolated to specific layers)
  - Follows industry-standard MVC/MVP patterns
  - Enables dependency inversion (business logic doesn't depend on database details)

**2. Repository Pattern**
- **Decision**: Use repository pattern for data access
- **Rationale**: 
  - Abstraction from ORM details
  - Easy to create mock repositories for testing
  - Flexibility to change data storage without affecting business logic
  - Single responsibility principle (repositories only handle data access)
  - Enables test-driven development

**3. Service Layer**
- **Decision**: Business logic in service classes, not in controllers
- **Rationale**: 
  - Reusability across controllers
  - Testability without HTTP layer
  - Clear separation of concerns (controllers handle HTTP, services handle business rules)
  - Business logic can be used by API endpoints and web pages

**4. SQLite Database**
- **Decision**: Use SQLite instead of PostgreSQL/MySQL
- **Rationale**: 
  - Simplicity (no separate server needed)
  - Portability (database file included with application)
  - Sufficient for project scale (small to medium teams)
  - Easy setup (no additional installation required)
  - Zero configuration

**5. Flask Framework**
- **Decision**: Use Flask instead of Django
- **Rationale**: 
  - Lightweight (minimal overhead)
  - Flexible structure (better for learning architecture)
  - Better for understanding web framework concepts
  - Simplicity for academic purposes
  - More control over application structure

#### Microservices Design Decisions

**1. Four Services**
- **Decision**: User Service, Task Service, Notification Service, Frontend Service
- **Rationale**: 
  - Single responsibility principle (each service has one clear purpose)
  - Independent development/deployment
  - Independent scalability (scale based on demand)
  - Real-world pattern (common microservices pattern)
  - Clear domain boundaries

**2. HTTP REST APIs**
- **Decision**: Synchronous HTTP communication instead of message queues
- **Rationale**: 
  - Simplicity (easier to understand and debug)
  - No additional infrastructure needed (no RabbitMQ/Kafka)
  - Sufficient for project requirements
  - Demonstrates basic service communication
  - Standard protocol (widely understood)

**Note**: Production systems often use message queues for better reliability and async processing.

**3. Separate Databases**
- **Decision**: Each service has its own database
- **Rationale**: 
  - Data ownership (each service owns its data)
  - Independence (services don't share database connections)
  - Independent optimization (can optimize each database independently)
  - Fault isolation (database issues isolated to one service)
  - Follows microservices best practices

**4. Docker Containerization**
- **Decision**: Use Docker for all services
- **Rationale**: 
  - Consistency across environments (development/production)
  - Service isolation (services isolated in containers)
  - Portability (works on any Docker-supported platform)
  - Docker Compose simplifies orchestration
  - Industry standard for microservices

**5. Service Discovery via DNS**
- **Decision**: Use Docker service names for service discovery
- **Rationale**: 
  - Simplicity (no need for service registry like Consul, etcd)
  - Docker-native (built into Docker networking)
  - Sufficient for project requirements
  - Demonstrates basic service discovery
  - No additional infrastructure needed

**6. Stateless Notification Service**
- **Decision**: Notification Service stores notifications in memory
- **Rationale**: 
  - Simplicity (no database needed for basic functionality)
  - Stateless (easier to scale horizontally)
  - Sufficient for project requirements
  - Demonstrates stateless service pattern

**Note**: Production systems would use a database for persistence.

---

## Rationale for Architecture Selection

### Selected Architecture: Layered Monolith (MVC)

After careful analysis of both architectural approaches, the **Layered Monolith (MVC) Architecture** was selected as the primary architecture for this project. The following factors influenced this decision:

#### 1. Project Scope and Requirements

- **Small to Medium Scale**: The task management system is designed for small teams (5-20 users)
- **Limited Features**: Core features (CRUD, assignments, notifications) don't require distributed architecture
- **Academic Context**: The project is for academic demonstration, not production at scale
- **Feature Set**: All required features can be efficiently implemented in a monolithic structure
- **User Base**: Expected concurrent users (<100) don't justify microservices complexity

#### 2. Development Team Size

- **Small Team**: Typically 1-3 developers working on this project
- **Limited Resources**: Microservices require more coordination and infrastructure knowledge
- **Rapid Development**: Monolith allows faster feature development and iteration
- **Learning Curve**: Easier for small teams to understand and maintain
- **Communication Overhead**: Microservices require more coordination between team members

#### 3. Complexity vs. Benefit Analysis

- **Microservices Overhead**: The complexity of managing 4 services, Docker, networking, and inter-service communication outweighs the benefits for this project size
- **Monolith Simplicity**: Single codebase, single deployment, easier debugging and testing
- **YAGNI Principle**: "You Aren't Gonna Need It" - Don't add complexity until needed
- **Cost-Benefit**: The operational overhead of microservices doesn't justify the benefits at this scale
- **Maintenance Burden**: Microservices require more ongoing maintenance and monitoring

#### 4. Performance Considerations

- **Network Latency**: Microservices add HTTP call overhead (even if minimal, 1-10ms per call)
- **Transaction Management**: Monolith provides ACID transactions across all operations
- **Data Consistency**: Easier to maintain consistency in a single database
- **Response Time**: Direct function calls are faster than HTTP requests
- **Resource Efficiency**: Single process uses less memory and CPU

#### 5. Development and Maintenance

- **Faster Development**: No need to coordinate between services during development
- **Easier Testing**: All components testable in one environment
- **Simpler Debugging**: Single codebase, single log file
- **Lower Operational Overhead**: One application to monitor and maintain
- **Easier Onboarding**: New developers can understand the entire system quickly
- **Faster Iteration**: Changes can be made and tested immediately

#### 6. Future Scalability Path

- **Evolutionary Architecture**: Monolith can be refactored to microservices if needed
- **Proven Pattern**: Many successful companies start with monoliths and evolve (e.g., Amazon, Netflix)
- **Migration Path**: Clear path to extract services when scale demands it
- **Premature Optimization**: Avoid over-engineering for hypothetical future needs
- **Refactoring Strategy**: Can extract services incrementally as needed

#### 7. Technology Stack Alignment

- **Python/Flask**: Well-suited for monolithic applications
- **SQLite**: Sufficient for small to medium scale
- **Simple Deployment**: No need for container orchestration
- **Resource Efficiency**: Lower memory and CPU requirements
- **Development Speed**: Faster to develop and deploy

#### 8. Academic and Learning Objectives

- **Architecture Understanding**: Demonstrates solid architectural principles without unnecessary complexity
- **Best Practices**: Shows proper layering, separation of concerns, and design patterns
- **Educational Value**: Easier for students to understand and learn from
- **Comparison Value**: Provides clear contrast with microservices for learning purposes

### When Microservices Would Be Preferred

Microservices architecture would be the better choice if:

- **Large Scale**: 100+ concurrent users, millions of tasks
- **Large Team**: 10+ developers needing independent work streams
- **Different Technologies**: Need for different languages/frameworks per service
- **Independent Scaling**: Very different load patterns per service (e.g., notifications need 10x more capacity)
- **Fault Tolerance Critical**: System must continue operating if one component fails
- **Regulatory Requirements**: Need for strict service isolation (e.g., healthcare, finance)
- **Geographic Distribution**: Services need to be deployed in different regions
- **Complex Business Logic**: Each service has distinct, complex business rules
- **Organizational Structure**: Different teams own different services
- **Technology Evolution**: Need to adopt new technologies incrementally

### Conclusion

For this project's scope, team size, and requirements, the Layered Monolith provides the optimal balance of:

- **Simplicity**: Easy to understand, develop, and maintain
- **Speed**: Rapid development and deployment
- **Reliability**: Single point of deployment reduces failure modes
- **Cost**: Lower infrastructure and operational costs
- **Maintainability**: Easier for small teams to manage
- **Learning Value**: Demonstrates solid architectural principles without unnecessary complexity
- **Performance**: Faster response times, lower latency
- **Resource Efficiency**: Lower memory and CPU usage

The microservices architecture demonstrates valuable concepts and patterns but introduces unnecessary complexity for the current project requirements. It serves as an excellent educational comparison to show when microservices are appropriate and when a simpler architecture is more suitable.

**Key Takeaway**: Start simple with a monolith, and evolve to microservices only when the benefits clearly outweigh the costs. For this project, the monolith is the right choice.

---

## Project Overview

This project implements a task management system using two different architectural approaches to demonstrate and compare architectural styles, analyzing their trade-offs, advantages, and suitability for different scenarios.

### Project Structure

```
.
├── Selected/              # Layered Monolith (MVC) Architecture
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   ├── templates/
│   ├── static/
│   ├── tests/
│   └── README.md
│
└── Unselected/            # Microservices Architecture
    ├── task-service/
    ├── user-service/
    ├── notification-service/
    ├── frontend-service/
    ├── docker-compose.yml
    └── README.md
```

### Features

Both architectures implement the same core features:

- ✅ Create, edit, and manage tasks
- ✅ Assign tasks to team members
- ✅ Track progress with status updates
- ✅ Dashboard with statistics
- ✅ Calendar view for deadlines
- ✅ In-app notifications for upcoming deadlines
- ✅ Activity log of all task updates
- ✅ CSV export functionality

### Technology Stack

**Common**:
- Python 3.11
- Flask 3.0.0
- pytest for testing

**Layered Monolith Specific**:
- Jinja2 templates
- Flask-SQLAlchemy 3.1.1
- SQLAlchemy 2.0.23
- SQLite

**Microservices Specific**:
- Flask-CORS 4.0.0
- Docker & Docker Compose
- HTTP REST APIs for inter-service communication

---

## Testing

### Layered Monolith Testing

#### Run All Tests
```bash
cd Selected
source venv/bin/activate  # Activate virtual environment
pytest tests/
```

#### Run Specific Test Files
```bash
# Test models only
pytest tests/test_models.py

# Test services only
pytest tests/test_services.py

# Test routes only
pytest tests/test_routes.py
```

#### Run with Verbose Output
```bash
pytest tests/ -v
```

#### Run with Coverage
```bash
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html
```

### Microservices Testing

#### Test User Service
```bash
cd Unselected/user-service
docker compose run --rm user-service pytest tests/
```

#### Test Task Service
```bash
cd Unselected/task-service
docker compose run --rm task-service pytest tests/
```

#### Test Notification Service
```bash
cd Unselected/notification-service
docker compose run --rm notification-service pytest tests/
```

### Integration Testing

#### Test Service Communication (Microservices)
1. Start all services:
   ```bash
   cd Unselected
   docker compose up -d
   ```

2. Create a user:
   ```bash
   curl -X POST http://localhost:5002/api/users \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","email":"test@example.com"}'
   ```

3. Create a task (should validate user):
   ```bash
   curl -X POST http://localhost:5000/api/tasks \
     -H "Content-Type: application/json" \
     -d '{"title":"Test Task","description":"Test","priority":"high","created_by":1}'
   ```

4. Check notification service received event:
   ```bash
   curl http://localhost:5001/api/notifications
   ```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Python version not 3.11
**Symptoms**: `python --version` shows 3.9 or 3.10

**Solution**:
- Install Python 3.11 from python.org
- Use `python3.11` explicitly: `python3.11 -m venv venv`
- Update PATH to prioritize Python 3.11

#### Issue: ModuleNotFoundError
**Symptoms**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
- Ensure virtual environment is activated (see `(venv)` in prompt)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check you're in the correct directory

#### Issue: Port already in use
**Symptoms**: `Address already in use` or `Port 5000 is already in use`

**Solution**:
- Find process using port:
  ```bash
  # macOS/Linux
  lsof -i :5000
  
  # Windows
  netstat -ano | findstr :5000
  ```
- Kill the process or use a different port
- For Flask, set port: `app.run(port=5001)`

#### Issue: Docker not starting
**Symptoms**: `Cannot connect to Docker daemon`

**Solution**:
- Ensure Docker Desktop is running (macOS/Windows)
- Check Docker service: `sudo systemctl status docker` (Linux)
- Restart Docker Desktop
- Check Docker is in PATH: `docker --version`

#### Issue: Database locked (SQLite)
**Symptoms**: `sqlite3.OperationalError: database is locked`

**Solution**:
- Close all connections to the database
- Restart the application
- Check for multiple instances running
- Delete database file and restart (data will be lost)

#### Issue: Services can't communicate (Microservices)
**Symptoms**: `Connection refused` or `Service unavailable`

**Solution**:
- Ensure all services are running: `docker compose ps`
- Check service names in docker-compose.yml match URLs
- Verify network: `docker network ls`
- Check service logs: `docker compose logs <service-name>`

#### Issue: Virtual environment not activating (Windows)
**Symptoms**: Script execution is disabled

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Issue: Docker build fails
**Symptoms**: Build errors during `docker compose build`

**Solution**:
- Check Dockerfile syntax
- Verify all files are in correct locations
- Check internet connection (for pip installs)
- Clear Docker cache: `docker system prune -a`

### Getting Help

1. **Check Logs**:
   - Layered Monolith: Check terminal output
   - Microservices: `docker compose logs`

2. **Verify Installation**:
   - Python: `python --version`
   - pip: `pip --version`
   - Docker: `docker --version`

3. **Check Documentation**:
   - README.md in each architecture directory
   - Python/Flask documentation
   - Docker documentation

---

## Accessing Services

### Layered Monolith (Selected/)

**Web Interface**: http://localhost:5000
- **Dashboard**: http://localhost:5000/
- **Tasks**: http://localhost:5000/tasks
- **Calendar**: http://localhost:5000/calendar

### Microservices (Unselected/)

**Web Interface**: http://localhost:5003
- **Dashboard**: http://localhost:5003/
- **Tasks**: http://localhost:5003/tasks
- **Calendar**: http://localhost:5003/calendar

**API Services** (backend):
- **User Service API**: http://localhost:5002
- **Task Service API**: http://localhost:5000
- **Notification Service API**: http://localhost:5001
- **Frontend Service**: http://localhost:5003

**Health Check Endpoints**:
- Frontend Service: http://localhost:5003/health
- User Service: http://localhost:5002/health
- Task Service: http://localhost:5000/health
- Notification Service: http://localhost:5001/health

### Testing APIs with curl

#### Create a User
```bash
curl -X POST http://localhost:5002/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com"}'
```

#### Get All Users
```bash
curl http://localhost:5002/api/users
```

#### Create a Task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"My First Task","description":"This is a test task","priority":"high","created_by":1}'
```

#### Get All Tasks
```bash
curl http://localhost:5000/api/tasks
```

---

## Development Environment

- **IDE**: Visual Studio Code (compatible with macOS, Windows, Linux)
- **Python**: 3.11
- **Package Management**: pip/venv
- **Testing**: pytest
- **Source Control**: GitHub

---

## Project Goals

1. **Implementation**: Implement both architectural styles with the same feature set
2. **Comparison**: Analyze and compare the two approaches
3. **Documentation**: Provide comprehensive documentation for both architectures
4. **Best Practices**: Demonstrate sound architectural principles suitable for academic and small-scale professional use

---

## Future Considerations

The Layered Monolith provides the best balance of maintainability, reliability, and feasibility for this project, with the potential to evolve into a microservice-based model in the future if needed.

### Future Enhancements

#### Layered Monolith
- Add authentication/authorization
- Implement caching (Redis)
- Add background job processing (Celery)
- Migrate to PostgreSQL for production
- Add API versioning

#### Microservices
- Implement message queue (RabbitMQ/Kafka)
- Add API Gateway
- Implement service mesh (Istio)
- Add distributed tracing (Jaeger)
- Implement circuit breakers
- Add service discovery (Consul)

---

## License

This project is created for academic purposes as part of CS5-7319 Final Project.

---

## Authors

Group 1 - Miller & Lomelin

---

**Last Updated**: 2024  
**Project**: CS5-7319 Final Project - Group 1 (Miller & Lomelin)  
**Architectures**: Layered Monolith (Selected) | Microservices (Unselected)
