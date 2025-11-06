# Task Management System - Implementation Guide

## Table of Contents
1. [Platform Requirements](#platform-requirements)
2. [Installation & Configuration](#installation--configuration)
3. [Compilation Instructions](#compilation-instructions)
4. [Execution Instructions](#execution-instructions)
5. [Architecture Comparison](#architecture-comparison)
6. [Rationale for Architecture Selection](#rationale-for-architecture-selection)
7. [Changes from Project Proposal](#changes-from-project-proposal)
8. [Architecture Design Decisions](#architecture-design-decisions)
9. [Testing Instructions](#testing-instructions)
10. [Troubleshooting](#troubleshooting)

---

## Platform Requirements

### Operating System
- **macOS**: 10.15 (Catalina) or later
- **Windows**: Windows 10 or later
- **Linux**: Ubuntu 20.04 LTS or later, or any modern Linux distribution

### Required Software

#### 1. Python 3.11
- **Version**: Python 3.11.x (3.11.0 or later)
- **Download**: 
  - macOS/Linux: https://www.python.org/downloads/
  - Windows: https://www.python.org/downloads/windows/
- **Verification**: 
  ```bash
  python3 --version
  # Should output: Python 3.11.x
  ```

#### 2. pip (Python Package Manager)
- Usually comes with Python 3.11
- **Verification**:
  ```bash
  pip3 --version
  # Should output: pip 23.x.x or later
  ```

#### 3. Docker & Docker Compose (For Microservices Architecture Only)
- **Docker**: Version 24.0 or later
- **Docker Compose**: Version 2.20 or later (included with Docker Desktop)
- **Download**: 
  - macOS/Windows: https://www.docker.com/products/docker-desktop/
  - Linux: Follow instructions at https://docs.docker.com/engine/install/
- **Verification**:
  ```bash
  docker --version
  docker compose version
  ```

#### 4. Git (Optional, for version control)
- **Download**: https://git-scm.com/downloads
- **Verification**:
  ```bash
  git --version
  ```

#### 5. Code Editor (Recommended)
- **Visual Studio Code**: https://code.visualstudio.com/
- **PyCharm**: https://www.jetbrains.com/pycharm/
- Any text editor that supports Python

---

## Installation & Configuration

### Step 1: Install Python 3.11

#### macOS
1. Download Python 3.11 from https://www.python.org/downloads/
2. Run the installer package (.pkg file)
3. Check "Add Python to PATH" during installation
4. Verify installation:
   ```bash
   python3 --version
   ```

#### Windows
1. Download Python 3.11 Windows installer from https://www.python.org/downloads/windows/
2. Run the installer (.exe file)
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```bash
   python --version
   ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3.11 --version
```

### Step 2: Install Docker (For Microservices Only)

#### macOS/Windows
1. Download Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Install and launch Docker Desktop
3. Wait for Docker to start (whale icon in system tray)
4. Verify:
   ```bash
   docker --version
   docker compose version
   ```

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
# Log out and log back in for group changes to take effect
```

### Step 3: Clone/Download Project

If using Git:
```bash
git clone <repository-url>
cd CS5-7319-Final-Project-Group-1-Miller-Lomelin
```

Or download and extract the ZIP file to your desired location.

---

## Compilation Instructions

### Note on Python Compilation
Python is an interpreted language, so there is no traditional "compilation" step. However, we need to:
1. Install dependencies
2. Set up virtual environments
3. Initialize databases

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
- Install all dependencies in each container

#### Step 3: Verify Docker Images
```bash
docker images
```

You should see:
- `unselected-user-service`
- `unselected-task-service`
- `unselected-notification-service`

---

## Execution Instructions

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
- **URL**: http://localhost:5000
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
docker compose up
```

Or run in detached mode (background):
```bash
docker compose up -d
```

#### Step 3: Verify Services are Running
```bash
docker compose ps
```

You should see all three services with status "Up":
- user-service (port 5002)
- task-service (port 5000)
- notification-service (port 5001)

#### Step 4: Check Service Health
```bash
# User Service
curl http://localhost:5002/health

# Task Service
curl http://localhost:5000/health

# Notification Service
curl http://localhost:5001/health
```

All should return: `{"status":"healthy","service":"..."}`

#### Step 5: Access the Services
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

### Testing the Systems

#### Layered Monolith - Create a User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com"}'
```

#### Layered Monolith - Create a Task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"This is a test","priority":"high","created_by":1}'
```

#### Microservices - Create a User
```bash
curl -X POST http://localhost:5002/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com"}'
```

#### Microservices - Create a Task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"This is a test","priority":"high","created_by":1}'
```

---

## Architecture Comparison

### Layered Monolith (MVC) Architecture

#### Structure
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

#### Key Characteristics
- **Single Deployable Unit**: All code in one application
- **Four Layers**: Presentation → Business Logic → Data Access → Data
- **Repository Pattern**: Abstracts database operations
- **Shared Database**: Single SQLite database for all entities
- **Internal Communication**: Direct function calls
- **Technology Stack**: Python, Flask, SQLAlchemy, SQLite

#### Advantages
1. **Simplicity**: Easy to understand and develop
2. **Rapid Development**: Fast iteration cycles
3. **Easy Testing**: All components in one codebase
4. **Low Overhead**: No network latency between layers
5. **Transaction Management**: ACID transactions across all operations
6. **Single Deployment**: One application to deploy and monitor

#### Disadvantages
1. **Scalability**: Harder to scale individual components
2. **Technology Lock-in**: All components use same stack
3. **Fault Isolation**: One bug can affect entire system
4. **Team Coordination**: All developers work on same codebase

### Microservices Architecture

#### Structure
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
```

#### Key Characteristics
- **Three Independent Services**: User, Task, Notification
- **Separate Databases**: Each service has its own data store
- **HTTP Communication**: REST APIs for inter-service communication
- **Containerized**: Docker containers for each service
- **Service Discovery**: Services communicate via service names
- **Independent Deployment**: Each service can be deployed separately

#### Advantages
1. **Scalability**: Scale each service independently
2. **Fault Isolation**: Failure in one service doesn't crash others
3. **Technology Flexibility**: Each service can use different tech
4. **Team Autonomy**: Different teams can work on different services
5. **Modularity**: Clear separation of concerns
6. **Independent Scaling**: Scale high-demand services more

#### Disadvantages
1. **Complexity**: More moving parts to manage
2. **Network Latency**: HTTP calls add overhead
3. **Data Consistency**: Harder to maintain consistency
4. **Deployment Overhead**: Multiple services to deploy
5. **Testing Complexity**: Integration testing is more complex
6. **Debugging**: Distributed tracing needed

### Detailed Comparison Table

| Aspect | Layered Monolith | Microservices |
|--------|-----------------|---------------|
| **Deployment** | Single application | 3 separate services |
| **Database** | 1 SQLite database | 3 separate databases |
| **Communication** | Function calls | HTTP REST APIs |
| **Scalability** | Vertical scaling | Horizontal scaling per service |
| **Fault Tolerance** | Single point of failure | Isolated failures |
| **Development Speed** | Fast (single codebase) | Slower (coordination needed) |
| **Testing** | Simple (unit + integration) | Complex (service + integration) |
| **Technology Stack** | Fixed (Python/Flask) | Flexible per service |
| **Team Size** | Small teams (1-3) | Larger teams (3+) |
| **Network Calls** | None (internal) | Multiple HTTP calls |
| **Transaction Management** | ACID across all operations | Eventual consistency |
| **Monitoring** | Single application log | Multiple service logs |
| **Setup Complexity** | Low (pip install) | Medium (Docker required) |

---

## Rationale for Architecture Selection

### Selected Architecture: Layered Monolith (MVC)

After careful analysis of both architectural approaches, the **Layered Monolith (MVC) Architecture** was selected as the primary architecture for this project. The following factors influenced this decision:

#### 1. Project Scope and Requirements
- **Small to Medium Scale**: The task management system is designed for small teams (5-20 users)
- **Limited Features**: Core features (CRUD, assignments, notifications) don't require distributed architecture
- **Academic Context**: The project is for academic demonstration, not production at scale

#### 2. Development Team Size
- **Small Team**: Typically 1-3 developers working on this project
- **Limited Resources**: Microservices require more coordination and infrastructure knowledge
- **Rapid Development**: Monolith allows faster feature development and iteration

#### 3. Complexity vs. Benefit Analysis
- **Microservices Overhead**: The complexity of managing 3 services, Docker, networking, and inter-service communication outweighs the benefits for this project size
- **Monolith Simplicity**: Single codebase, single deployment, easier debugging and testing
- **YAGNI Principle**: "You Aren't Gonna Need It" - Don't add complexity until needed

#### 4. Performance Considerations
- **Network Latency**: Microservices add HTTP call overhead (even if minimal)
- **Transaction Management**: Monolith provides ACID transactions across all operations
- **Data Consistency**: Easier to maintain consistency in a single database

#### 5. Development and Maintenance
- **Faster Development**: No need to coordinate between services during development
- **Easier Testing**: All components testable in one environment
- **Simpler Debugging**: Single codebase, single log file
- **Lower Operational Overhead**: One application to monitor and maintain

#### 6. Future Scalability Path
- **Evolutionary Architecture**: Monolith can be refactored to microservices if needed
- **Proven Pattern**: Many successful companies start with monoliths and evolve
- **Migration Path**: Clear path to extract services when scale demands it

#### 7. Technology Stack Alignment
- **Python/Flask**: Well-suited for monolithic applications
- **SQLite**: Sufficient for small to medium scale
- **Simple Deployment**: No need for container orchestration

### When Microservices Would Be Preferred

Microservices architecture would be the better choice if:
- **Large Scale**: 100+ concurrent users, millions of tasks
- **Large Team**: 10+ developers needing independent work streams
- **Different Technologies**: Need for different languages/frameworks per service
- **Independent Scaling**: Very different load patterns per service
- **Fault Tolerance Critical**: System must continue operating if one component fails
- **Regulatory Requirements**: Need for strict service isolation

### Conclusion

For this project's scope, team size, and requirements, the Layered Monolith provides the optimal balance of:
- **Simplicity**: Easy to understand, develop, and maintain
- **Speed**: Rapid development and deployment
- **Reliability**: Single point of deployment reduces failure modes
- **Cost**: Lower infrastructure and operational costs
- **Maintainability**: Easier for small teams to manage

The microservices architecture demonstrates valuable concepts and patterns but introduces unnecessary complexity for the current project requirements.

---

## Changes from Project Proposal

### Original Proposal
The original project proposal outlined two candidate architectures:
1. **Layered Monolith (MVC)** - Selected
2. **Microservices** - Two services (Task Service + Notification Service)

### Changes Made

#### 1. Added Database Layer to Layered Monolith
**Change**: Introduced a Repository Pattern (Data Access Layer) between Business Logic and Data layers.

**Rationale**:
- **Better Separation of Concerns**: Business logic no longer directly accesses database
- **Testability**: Easier to mock database operations in tests
- **Maintainability**: Database changes isolated to repository layer
- **Flexibility**: Can swap database implementations without changing business logic

**Implementation**:
- Created `database/repositories.py` with:
  - `TaskRepository`: All task data access operations
  - `UserRepository`: All user data access operations
  - `ActivityLogRepository`: All activity log operations
- Updated services to use repositories instead of direct model access

#### 2. Separated User Service in Microservices Architecture
**Change**: Split User management into a separate service (User Service) instead of including it in Task Service.

**Original**: Task Service + Notification Service (2 services)
**Updated**: User Service + Task Service + Notification Service (3 services)

**Rationale**:
- **Single Responsibility Principle**: Each service has a focused, single responsibility
- **Better Scalability**: User management can scale independently
- **Modularity**: Clear separation of user management from task management
- **Future-Proofing**: Easier to add authentication/authorization features
- **Real-World Pattern**: Common pattern in microservices architectures

**Implementation**:
- Created `user-service/` with:
  - User CRUD operations
  - User validation endpoints
  - User lookup by username/email
- Updated Task Service to:
  - Remove User model
  - Communicate with User Service via HTTP
  - Validate user IDs before task operations
- Updated docker-compose.yml to include User Service

### Impact of Changes

#### Positive Impacts
1. **Better Architecture**: Both architectures now follow best practices
2. **More Realistic**: Microservices architecture more closely mirrors production systems
3. **Better Learning**: Demonstrates proper separation of concerns
4. **Improved Testability**: Repository pattern makes testing easier

#### Challenges Addressed
1. **Service Communication**: Task Service now properly validates users via User Service
2. **Data Consistency**: User Service is single source of truth for user data
3. **Service Dependencies**: Proper dependency management in docker-compose

### Documentation Updates
- Updated README files in both architectures
- Added User Service documentation
- Updated architecture diagrams (conceptual)
- Added service communication documentation

---

## Architecture Design Decisions

### Layered Monolith Design Decisions

#### 1. Four-Layer Architecture
**Decision**: Presentation → Business Logic → Data Access → Data

**Rationale**:
- **Clear Separation**: Each layer has distinct responsibilities
- **Testability**: Each layer can be tested independently
- **Maintainability**: Changes isolated to specific layers
- **Industry Standard**: Follows common MVC/MVP patterns

#### 2. Repository Pattern
**Decision**: Use repository pattern for data access

**Rationale**:
- **Abstraction**: Business logic doesn't depend on ORM details
- **Testability**: Easy to create mock repositories
- **Flexibility**: Can change data storage without affecting business logic
- **Single Responsibility**: Repositories only handle data access

#### 3. Service Layer
**Decision**: Business logic in service classes, not in controllers

**Rationale**:
- **Reusability**: Services can be used by multiple controllers
- **Testability**: Business logic testable without HTTP layer
- **Separation**: Controllers handle HTTP, services handle business rules

#### 4. SQLite Database
**Decision**: Use SQLite instead of PostgreSQL/MySQL

**Rationale**:
- **Simplicity**: No separate database server needed
- **Portability**: Database file included with application
- **Sufficient**: Handles expected load for this project
- **Easy Setup**: No additional installation required

#### 5. Flask Framework
**Decision**: Use Flask instead of Django

**Rationale**:
- **Lightweight**: Minimal overhead, only what's needed
- **Flexibility**: More control over application structure
- **Learning**: Better for understanding web framework concepts
- **Simplicity**: Easier to understand for academic purposes

### Microservices Design Decisions

#### 1. Three Services
**Decision**: User Service, Task Service, Notification Service

**Rationale**:
- **Single Responsibility**: Each service has one clear purpose
- **Independence**: Services can be developed/deployed independently
- **Scalability**: Each can scale based on demand
- **Real-World Pattern**: Common microservices pattern

#### 2. HTTP REST APIs
**Decision**: Synchronous HTTP communication instead of message queues

**Rationale**:
- **Simplicity**: Easier to understand and debug
- **No Additional Infrastructure**: No need for RabbitMQ/Kafka
- **Sufficient**: Meets requirements for this project
- **Learning**: Demonstrates basic service communication

**Note**: Production systems often use message queues for better reliability and async processing.

#### 3. Separate Databases
**Decision**: Each service has its own database

**Rationale**:
- **Data Ownership**: Each service owns its data
- **Independence**: Services don't share database connections
- **Scalability**: Can optimize each database independently
- **Fault Isolation**: Database issues isolated to one service

#### 4. Docker Containerization
**Decision**: Use Docker for all services

**Rationale**:
- **Consistency**: Same environment across development/production
- **Isolation**: Services isolated in containers
- **Portability**: Works on any Docker-supported platform
- **Orchestration**: Docker Compose simplifies multi-service setup

#### 5. Service Discovery via DNS
**Decision**: Use Docker service names for service discovery

**Rationale**:
- **Simplicity**: No need for service registry (Consul, etcd)
- **Docker Native**: Built into Docker networking
- **Sufficient**: Meets requirements for this project
- **Learning**: Demonstrates basic service discovery

#### 6. Stateless Notification Service
**Decision**: Notification Service stores notifications in memory

**Rationale**:
- **Simplicity**: No database needed for basic functionality
- **Stateless**: Easier to scale horizontally
- **Sufficient**: Meets project requirements

**Note**: Production systems would use a database for persistence.

### Cross-Architecture Decisions

#### 1. Python 3.11
**Decision**: Use Python 3.11 for both architectures

**Rationale**:
- **Modern Features**: Latest language features and improvements
- **Performance**: Better performance than older versions
- **Compatibility**: All required libraries support 3.11
- **Long-term Support**: Active development and support

#### 2. SQLAlchemy ORM
**Decision**: Use SQLAlchemy for database operations

**Rationale**:
- **Maturity**: Well-established, widely used ORM
- **Flexibility**: Works with multiple database backends
- **Features**: Rich feature set (migrations, relationships, etc.)
- **Documentation**: Excellent documentation and community support

#### 3. Flask Framework
**Decision**: Use Flask for both architectures

**Rationale**:
- **Consistency**: Same framework across architectures
- **Lightweight**: Minimal overhead
- **Flexibility**: Easy to structure as needed
- **REST Support**: Good support for REST APIs

#### 4. pytest for Testing
**Decision**: Use pytest for all testing

**Rationale**:
- **Simplicity**: Easy to write and run tests
- **Features**: Rich assertion library, fixtures, parametrization
- **Integration**: Works well with Flask-Testing
- **Industry Standard**: Widely used in Python community

---

## Testing Instructions

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

Or manually:
```bash
cd Unselected/user-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/
```

#### Test Task Service
```bash
cd Unselected/task-service
docker compose run --rm task-service pytest tests/
```

Or manually:
```bash
cd Unselected/task-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/
```

#### Test Notification Service
```bash
cd Unselected/notification-service
docker compose run --rm notification-service pytest tests/
```

Or manually:
```bash
cd Unselected/notification-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/
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

#### Issue: Import errors in tests
**Symptoms**: `ImportError: cannot import name 'X'`

**Solution**:
- Ensure you're running tests from project root
- Check `__init__.py` files exist in package directories
- Verify PYTHONPATH includes project directory
- Use: `python -m pytest tests/` instead of `pytest tests/`

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

4. **Common Commands**:
   ```bash
   # Check whats running
   ps aux | grep python  # macOS/Linux
   tasklist | findstr python  # Windows
   
   # Check ports
   lsof -i :5000  # macOS/Linux
   netstat -ano | findstr :5000  # Windows
   
   # Docker status
   docker compose ps
   docker compose logs
   ```

---

## Additional Information

### Project Structure Summary

#### Layered Monolith
- **4 Layers**: Presentation, Business Logic, Data Access, Data
- **1 Application**: Single Flask application
- **1 Database**: SQLite database
- **Repository Pattern**: Data access abstraction

#### Microservices
- **3 Services**: User, Task, Notification
- **3 Databases**: One per service
- **HTTP Communication**: REST APIs
- **Docker Orchestration**: docker-compose.yml

### Key Files to Review

#### Layered Monolith
- `Selected/app.py`: Application entry point
- `Selected/routes.py`: Route handlers (Controllers)
- `Selected/services/task_service.py`: Business logic
- `Selected/database/repositories.py`: Data access layer
- `Selected/models.py`: Database models

#### Microservices
- `Unselected/user-service/app.py`: User Service
- `Unselected/task-service/app.py`: Task Service
- `Unselected/notification-service/app.py`: Notification Service
- `Unselected/docker-compose.yml`: Service orchestration

### Performance Considerations

#### Layered Monolith
- **Database**: SQLite suitable for <100 concurrent users
- **Memory**: Low memory footprint (~50-100MB)
- **Startup**: Fast startup time (<1 second)
- **Scalability**: Vertical scaling (more CPU/RAM)

#### Microservices
- **Network**: HTTP calls add ~1-10ms latency per call
- **Memory**: Higher memory footprint (~200-300MB total)
- **Startup**: Slower startup (Docker + 3 services)
- **Scalability**: Horizontal scaling per service

### Security Considerations

#### Both Architectures
- **Input Validation**: Validate all user inputs
- **SQL Injection**: SQLAlchemy ORM prevents SQL injection
- **CORS**: Configured for development (adjust for production)
- **Secrets**: Use environment variables for sensitive data

#### Production Recommendations
- Use PostgreSQL/MySQL instead of SQLite
- Implement authentication/authorization
- Use HTTPS instead of HTTP
- Add rate limiting
- Implement proper logging and monitoring
- Use secrets management (AWS Secrets Manager, etc.)

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

## Conclusion

This implementation guide provides comprehensive instructions for:
- Setting up the development environment
- Compiling and running both architectures
- Understanding architectural differences
- Testing the systems
- Troubleshooting common issues

Both architectures are fully functional and demonstrate different approaches to building the same application. The Layered Monolith is selected as the primary architecture due to its simplicity and suitability for the project scope, while the Microservices architecture demonstrates distributed system patterns and scalability considerations.

For questions or issues, refer to the troubleshooting section or review the code comments and documentation in each architecture's directory.

---

**Last Updated**: 2024
**Project**: CS5-7319 Final Project - Group 1 (Miller & Lomelin)
**Architectures**: Layered Monolith (Selected) | Microservices (Unselected)

