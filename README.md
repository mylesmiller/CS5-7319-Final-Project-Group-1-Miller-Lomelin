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

### Detailed Implementation Differences

This section provides an in-depth analysis of the implementation differences between the Layered Monolith and Microservices architectures, covering source code structure, reusable components, communication mechanisms, and architectural patterns.

#### 1. Source Code Structure and Organization

##### Layered Monolith Architecture (`Selected/`)

**File Structure:**
```
Selected/
├── app.py                    # Application factory and entry point
├── config.py                 # Configuration management
├── models.py                 # SQLAlchemy models (User, Task, ActivityLog)
├── routes.py                 # Route handlers (Controller/Presentation layer)
├── database/
│   ├── __init__.py
│   └── repositories.py       # Repository pattern (Data Access layer)
├── services/
│   ├── __init__.py
│   ├── task_service.py       # Business logic for tasks
│   └── notification_service.py  # Business logic for notifications
├── templates/                # Jinja2 HTML templates
├── static/                   # CSS and JavaScript files
└── tests/                    # Unit and integration tests
```

**Key Implementation Characteristics:**

1. **Single Application Entry Point (`app.py`)**:
   - Uses Flask application factory pattern (`create_app()`)
   - Single database initialization (`db.init_app(app)`)
   - All routes registered in one place via `register_routes(app)`
   - Single Flask application instance handles all requests

2. **Unified Models (`models.py`)**:
   - All domain models (User, Task, ActivityLog) in one file
   - SQLAlchemy relationships defined directly (e.g., `Task.assigned_to` foreign key to `User.id`)
   - Direct object relationships: `task.assignee` provides direct access to User object
   - Single database session manages all entities

3. **Repository Pattern (`database/repositories.py`)**:
   - Three repository classes: `TaskRepository`, `UserRepository`, `ActivityLogRepository`
   - All repositories share the same database connection (`db.session`)
   - Static methods for all operations (no instance state)
   - Direct SQLAlchemy query access: `Task.query.get(id)`
   - Transactions managed at the repository level with `db.session.commit()`

4. **Service Layer (`services/`)**:
   - `TaskService`: Contains all business logic for task operations
   - `NotificationService`: Handles notification generation logic
   - Services call repositories directly (in-process function calls)
   - No network communication required
   - Business logic can orchestrate multiple repository calls atomically

5. **Route Handlers (`routes.py`)**:
   - All HTTP endpoints defined in single file
   - Routes call service layer methods directly
   - Direct access to models and repositories if needed
   - Single error handling context

##### Microservices Architecture (`Unselected/`)

**File Structure:**
```
Unselected/
├── docker-compose.yml        # Service orchestration
├── user-service/
│   ├── app.py               # User Service Flask application
│   ├── models.py            # User model only
│   ├── config.py            # Service-specific configuration
│   └── Dockerfile           # Container definition
├── task-service/
│   ├── app.py               # Task Service Flask application
│   ├── models.py            # Task and ActivityLog models
│   ├── config.py            # Service-specific configuration
│   └── Dockerfile
├── notification-service/
│   ├── app.py               # Notification Service Flask application
│   └── Dockerfile
└── frontend-service/
    ├── app.py               # Frontend aggregation service
    ├── templates/           # Jinja2 templates
    ├── static/              # CSS and JavaScript
    └── Dockerfile
```

**Key Implementation Characteristics:**

1. **Multiple Independent Applications**:
   - Each service has its own `app.py` with Flask application instance
   - Each service initializes its own database connection
   - Services run in separate processes/containers
   - Each service has its own port (5000, 5001, 5002, 5003)

2. **Distributed Models**:
   - **User Service**: Only `User` model
   - **Task Service**: `Task` and `ActivityLog` models (no User model)
   - **Notification Service**: No persistent models (in-memory storage)
   - Models cannot reference each other directly (no foreign keys across services)
   - User IDs stored as integers in Task Service, not as relationships

3. **No Repository Pattern**:
   - Direct SQLAlchemy queries in route handlers
   - Each service queries only its own database
   - No abstraction layer between routes and database
   - Simpler structure per service (fewer layers)

4. **Service-Specific Business Logic**:
   - Business logic embedded in route handlers
   - Each service handles only its domain logic
   - Cross-service operations require HTTP calls
   - No shared business logic between services

5. **Frontend Service as API Gateway**:
   - Aggregates data from multiple backend services
   - Makes HTTP requests to Task, User, and Notification services
   - Renders templates with aggregated data
   - Handles service failures gracefully

#### 2. Communication Mechanisms

##### Layered Monolith: In-Process Function Calls

**Implementation Pattern:**
```python
# routes.py (Controller)
@app.route('/api/tasks', methods=['POST'])
def create_task():
    # Direct function call to service layer
    task = TaskService.create_task(...)
    return jsonify(task.to_dict())

# services/task_service.py (Service)
@staticmethod
def create_task(...):
    # Direct function call to repository
    task = TaskRepository.create(...)
    # Direct function call to another repository
    ActivityLogRepository.create(...)
    return task

# database/repositories.py (Repository)
@staticmethod
def create(...):
    # Direct database access
    task = Task(...)
    db.session.add(task)
    db.session.commit()
    return task
```

**Characteristics:**
- **Zero Network Overhead**: All communication is in-process function calls
- **Synchronous Execution**: Operations execute sequentially in same thread
- **Exception Propagation**: Exceptions bubble up naturally through call stack
- **Transaction Management**: Single database transaction can span multiple operations
- **Type Safety**: Python type hints and IDE support work across layers
- **Performance**: Sub-millisecond latency between layers

##### Microservices: HTTP REST API Calls

**Implementation Pattern:**
```python
# frontend-service/app.py
def get_from_service(url, endpoint):
    response = requests.get(f'{url}{endpoint}', timeout=5)
    return response.json()

@app.route('/tasks')
def tasks():
    # HTTP GET request to Task Service
    tasks = get_from_service(TASK_SERVICE_URL, '/api/tasks')
    # HTTP GET request to User Service
    users = get_from_service(USER_SERVICE_URL, '/api/users')
    return render_template('tasks.html', tasks=tasks, users=users)

# task-service/app.py
@app.route('/api/tasks/<int:task_id>/assign', methods=['POST'])
def assign_task(task_id):
    # HTTP GET request to User Service to validate user
    user = get_user_from_service(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Local database operation
    task.assigned_to = user_id
    db.session.commit()
    # HTTP POST request to Notification Service
    notify_notification_service('task_assigned', {...})
    return jsonify(task.to_dict())
```

**Characteristics:**
- **Network Overhead**: Each service call requires HTTP request/response (1-10ms latency)
- **Asynchronous Potential**: Can use async HTTP libraries, but implemented synchronously
- **Error Handling**: Must handle network failures, timeouts, service unavailability
- **Serialization**: Data must be JSON-serialized for transmission
- **Service Discovery**: Uses Docker service names (e.g., `user-service:5002`)
- **Timeout Management**: Each HTTP call has timeout (2-5 seconds)
- **Retry Logic**: Can implement retry mechanisms for failed requests

**Service Communication Examples:**

1. **Task Service → User Service**:
   ```python
   # In task-service/app.py
   def get_user_from_service(user_id):
       user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
       response = requests.get(f'{user_service_url}/api/users/{user_id}', timeout=2)
       return response.json() if response.status_code == 200 else None
   ```

2. **Task Service → Notification Service**:
   ```python
   def notify_notification_service(event_type, payload):
       notification_service_url = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5001')
       requests.post(f'{notification_service_url}/api/events', json={
           'event_type': event_type,
           'payload': payload,
           'timestamp': datetime.utcnow().isoformat()
       }, timeout=2)
   ```

3. **Frontend Service → All Backend Services**:
   ```python
   # Aggregates data from multiple services
   tasks = get_from_service(TASK_SERVICE_URL, '/api/tasks')
   users = get_from_service(USER_SERVICE_URL, '/api/users')
   notifications = get_from_service(NOTIFICATION_SERVICE_URL, '/api/notifications')
   ```

#### 3. Data Access Patterns

##### Layered Monolith: Repository Pattern with Shared Database

**Implementation:**
```python
# database/repositories.py
class TaskRepository:
    @staticmethod
    def create(title, description, priority='medium', due_date=None, assigned_to=None, created_by=None):
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to,  # Foreign key to User.id
            created_by=created_by
        )
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def get_by_id_or_404(task_id):
        return Task.query.get_or_404(task_id)  # Can use relationships

# Usage in service layer
task = TaskRepository.get_by_id_or_404(task_id)
user = task.assignee  # Direct relationship access via SQLAlchemy
```

**Key Features:**
- **Foreign Key Relationships**: `Task.assigned_to` is a foreign key to `User.id`
- **ORM Relationships**: SQLAlchemy relationships enable `task.assignee` direct access
- **Join Queries**: Can perform joins across tables in single query
- **ACID Transactions**: All operations within single transaction
- **Single Database Connection**: All repositories share `db.session`
- **Data Consistency**: Database enforces referential integrity

##### Microservices: Direct Queries with Service Boundaries

**Implementation:**
```python
# task-service/app.py
@app.route('/api/tasks', methods=['POST'])
def create_task():
    # No foreign key - just store integer ID
    task = Task(
        title=data['title'],
        assigned_to=data.get('assigned_to'),  # Just an integer, not a foreign key
        created_by=data.get('created_by')
    )
    # Must validate user exists via HTTP call
    if data.get('assigned_to'):
        if not validate_user_id(data['assigned_to']):
            return jsonify({'error': 'Invalid assigned_to user ID'}), 400
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict())

# No direct relationship access
# Must make HTTP call to get user details
def get_user_from_service(user_id):
    response = requests.get(f'{user_service_url}/api/users/{user_id}')
    return response.json()
```

**Key Features:**
- **No Foreign Keys Across Services**: `assigned_to` is just an integer
- **No ORM Relationships**: Cannot use `task.assignee` - user data is in different service
- **Manual Validation**: Must validate user existence via HTTP call
- **Separate Database Connections**: Each service has its own `db.session`
- **No Cross-Service Joins**: Cannot join User and Task tables
- **Eventual Consistency**: User deletion in User Service doesn't automatically update Task Service

#### 4. Reusable Components and Connectors

##### Layered Monolith: Shared Code Modules

**Reusable Components:**

1. **Repository Classes** (`database/repositories.py`):
   - `TaskRepository`: Reusable across all task operations
   - `UserRepository`: Reusable across all user operations
   - `ActivityLogRepository`: Reusable for activity tracking
   - All services can use same repository instances
   - Shared database connection pool

2. **Service Classes** (`services/`):
   - `TaskService`: Reusable business logic
   - `NotificationService`: Reusable notification logic
   - Can be imported and used by routes, background jobs, CLI scripts
   - No serialization needed - works with Python objects

3. **Models** (`models.py`):
   - Shared across all layers
   - Can be used in repositories, services, and routes
   - Type checking and IDE autocomplete work seamlessly

4. **Configuration** (`config.py`):
   - Single configuration file
   - Shared by all components
   - Environment variables loaded once

**Code Reuse Example:**
```python
# Can use TaskService from anywhere in the application
from services.task_service import TaskService

# In routes
task = TaskService.create_task(...)

# In background job (hypothetical)
def process_daily_tasks():
    tasks = TaskService.get_upcoming_deadlines(7)
    # Process tasks...

# In CLI script (hypothetical)
if __name__ == '__main__':
    task = TaskService.create_task(...)
```

##### Microservices: HTTP Client Helpers and Service Connectors

**Reusable Components:**

1. **HTTP Client Helper Functions** (`frontend-service/app.py`):
   ```python
   def get_from_service(url, endpoint):
       """Reusable helper for GET requests"""
       try:
           response = requests.get(f'{url}{endpoint}', timeout=5)
           if response.status_code == 200:
               return response.json()
           return None
       except Exception as e:
           print(f"Error calling {url}{endpoint}: {e}")
           return None
   
   def post_to_service(url, endpoint, data):
       """Reusable helper for POST requests"""
       # Implementation...
   
   def put_to_service(url, endpoint, data):
       """Reusable helper for PUT requests"""
       # Implementation...
   ```

2. **Service-Specific Connectors** (`task-service/app.py`):
   ```python
   def get_user_from_service(user_id):
       """Connector to User Service"""
       user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
       response = requests.get(f'{user_service_url}/api/users/{user_id}', timeout=2)
       return response.json() if response.status_code == 200 else None
   
   def notify_notification_service(event_type, payload):
       """Connector to Notification Service"""
       notification_service_url = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5001')
       requests.post(f'{notification_service_url}/api/events', json={...}, timeout=2)
   ```

3. **Service URL Configuration**:
   - Environment variables for service URLs
   - Docker service names for service discovery
   - Configurable per environment (dev, staging, production)

**Limitations:**
- **No Shared Code**: Each service is independent - cannot import code from other services
- **Serialization Required**: All data must be JSON-serialized for transmission
- **Error Handling**: Each service call must handle failures independently
- **Code Duplication**: Similar HTTP client code may exist in multiple services

#### 5. Error Handling and Resilience

##### Layered Monolith: Exception Propagation

**Implementation:**
```python
# Exception flows naturally through layers
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = TaskService.get_task_by_id(task_id)  # May raise exception
        return jsonify(task.to_dict())
    except Exception as e:
        # Handle at route level
        return jsonify({'error': str(e)}), 500

# In service layer
@staticmethod
def get_task_by_id(task_id):
    return TaskRepository.get_by_id_or_404(task_id)  # Raises 404 if not found

# In repository layer
@staticmethod
def get_by_id_or_404(task_id):
    return Task.query.get_or_404(task_id)  # Flask-SQLAlchemy raises 404
```

**Characteristics:**
- **Unified Error Handling**: Exceptions propagate through call stack
- **Single Error Context**: All errors occur in same process
- **Database Rollback**: Failed transactions automatically rollback
- **Type-Safe Errors**: Python exceptions with full stack traces

##### Microservices: Distributed Error Handling

**Implementation:**
```python
# Must handle service unavailability
def get_user_from_service(user_id):
    user_service_url = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
    try:
        response = requests.get(f'{user_service_url}/api/users/{user_id}', timeout=2)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.Timeout:
        print(f"User Service timeout for user {user_id}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"User Service unavailable")
        return None
    except Exception as e:
        print(f"Failed to get user from User Service: {e}")
        return None

# In route handler
@app.route('/api/tasks/<int:task_id>/assign', methods=['POST'])
def assign_task(task_id):
    user = get_user_from_service(user_id)
    if not user:  # Must check for None
        return jsonify({'error': 'User not found or service unavailable'}), 503
    # Continue with assignment...
```

**Characteristics:**
- **Network Failure Handling**: Must handle timeouts, connection errors, service unavailability
- **Graceful Degradation**: Services may continue operating if other services fail
- **Partial Failures**: Some operations may succeed while others fail
- **Error Propagation**: Must manually propagate errors across service boundaries
- **Circuit Breaker Pattern**: Could implement circuit breakers (not implemented in this project)

#### 6. Configuration Management

##### Layered Monolith: Single Configuration File

**Implementation:**
```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///task_manager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# app.py
from config import Config
app.config.from_object(Config)
```

**Characteristics:**
- **Single Configuration Source**: One config file for entire application
- **Environment Variables**: Can override with environment variables
- **Shared Settings**: All components use same configuration
- **Simple Deployment**: One set of environment variables

##### Microservices: Per-Service Configuration

**Implementation:**
```python
# task-service/config.py
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'task-service-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///task_service.db')
    USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user-service:5002')
    NOTIFICATION_SERVICE_URL = os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5001')

# docker-compose.yml
services:
  task-service:
    environment:
      - DATABASE_URL=sqlite:///task_service.db
      - USER_SERVICE_URL=http://user-service:5002
      - NOTIFICATION_SERVICE_URL=http://notification-service:5001
```

**Characteristics:**
- **Service-Specific Configuration**: Each service has its own config
- **Service Discovery URLs**: Must configure URLs to other services
- **Docker Environment Variables**: Configuration via docker-compose.yml
- **Multiple Configuration Points**: Must manage configuration for each service
- **Network Configuration**: Must configure service URLs and ports

#### 7. Testing Approaches

##### Layered Monolith: Unified Testing

**Implementation:**
```python
# tests/test_services.py
def test_create_task():
    task = TaskService.create_task(
        title="Test Task",
        created_by=1
    )
    assert task.title == "Test Task"
    # Can test entire flow in one test
    # Can use same database for all tests
```

**Characteristics:**
- **Single Test Suite**: All tests in one test directory
- **Shared Test Database**: Can use same test database for all tests
- **Mock Repositories**: Easy to mock repository layer for service tests
- **Integration Tests**: Can test entire request flow end-to-end
- **Fast Execution**: No network calls in tests

##### Microservices: Distributed Testing

**Implementation:**
```python
# Each service has its own test suite
# task-service/tests/test_task_service.py
def test_create_task():
    # Must mock HTTP calls to User Service
    with patch('app.get_user_from_service') as mock_get_user:
        mock_get_user.return_value = {'id': 1, 'username': 'test'}
        # Test task creation...
```

**Characteristics:**
- **Per-Service Test Suites**: Each service has its own tests
- **Mock External Services**: Must mock HTTP calls to other services
- **Integration Testing Complexity**: Requires all services running
- **Service Isolation**: Can test services independently
- **Network Mocking**: Must use tools like `responses` or `httpretty` to mock HTTP

#### 8. Deployment and Infrastructure

##### Layered Monolith: Single Deployment Unit

**Deployment Process:**
1. Install Python dependencies: `pip install -r requirements.txt`
2. Run application: `python app.py`
3. Single process handles all requests
4. Single database file (SQLite) or connection (PostgreSQL)

**Infrastructure Requirements:**
- Python runtime environment
- Virtual environment (optional but recommended)
- Database (SQLite file or PostgreSQL server)
- Web server (Flask development server or Gunicorn/uWSGI)

##### Microservices: Containerized Multi-Service Deployment

**Deployment Process:**
1. Build Docker images for each service: `docker compose build`
2. Start all services: `docker compose up`
3. Docker Compose orchestrates service startup
4. Each service runs in separate container
5. Docker network enables service communication

**Infrastructure Requirements:**
- Docker and Docker Compose
- Container orchestration (Docker Compose)
- Docker networking for service communication
- Volume management for persistent databases
- Health checks for service monitoring

**Docker Compose Configuration:**
```yaml
services:
  task-service:
    build: ./task-service
    environment:
      - USER_SERVICE_URL=http://user-service:5002
    networks:
      - task-manager-network
    depends_on:
      - user-service
```

#### 9. Data Model Differences

##### Layered Monolith: Unified Data Model with Relationships

**Models:**
```python
class Task(db.Model):
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    # SQLAlchemy relationship
    # Can access: task.assignee.username

class User(db.Model):
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assigned_to', backref='assignee')
    # Can access: user.assigned_tasks
```

**Benefits:**
- **Referential Integrity**: Database enforces foreign key constraints
- **ORM Relationships**: Direct object access via relationships
- **Join Queries**: Efficient joins across related tables
- **Cascade Operations**: Can cascade deletes/updates

##### Microservices: Distributed Data Model with ID References

**Task Service Models:**
```python
class Task(db.Model):
    assigned_to = db.Column(db.Integer, nullable=True)  # Just an integer, no foreign key
    # Cannot access: task.assignee (user data is in different service)
    # Must make HTTP call to get user details
```

**User Service Models:**
```python
class User(db.Model):
    # No relationship to tasks (tasks are in different service)
    # Cannot access: user.assigned_tasks
```

**Implications:**
- **No Referential Integrity**: Database cannot enforce cross-service relationships
- **Manual Validation**: Must validate user existence via HTTP call
- **Data Duplication Risk**: May need to cache user data in Task Service
- **Consistency Challenges**: User deletion doesn't automatically update tasks

#### 10. Summary of Key Implementation Differences

| Aspect | Layered Monolith | Microservices |
|--------|-----------------|---------------|
| **Code Organization** | Single codebase with layers | Multiple independent codebases |
| **Communication** | In-process function calls | HTTP REST API calls |
| **Data Access** | Repository pattern with shared DB | Direct queries with service boundaries |
| **Models** | Unified models with relationships | Distributed models with ID references |
| **Reusable Components** | Shared Python modules | HTTP client helpers and connectors |
| **Error Handling** | Exception propagation | Distributed error handling |
| **Configuration** | Single config file | Per-service configuration |
| **Testing** | Unified test suite | Per-service test suites with mocking |
| **Deployment** | Single application | Containerized multi-service |
| **Transaction Management** | ACID transactions | Eventual consistency |
| **Type Safety** | Full Python type checking | JSON serialization required |
| **Performance** | Sub-millisecond latency | Network latency (1-10ms per call) |

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
