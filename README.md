# Task Management System - Architecture Comparison Project

## 🚀 Quick Start

### Layered Monolith (Selected Architecture)
```bash
cd Selected
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
**Access**: http://localhost:5000

### Microservices Architecture
```bash
cd Unselected
docker compose up --build
```
**Access**: http://localhost:5003 (requires Docker Desktop)

---

## 1. Implementation Platform & Requirements

### Platform
- **Language**: Python 3.11.x (3.11.0 or later)
- **Download**: https://www.python.org/downloads/
- **Framework**: Flask 3.0.0
- **OS Support**: Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)

### Key Dependencies
- Flask 3.0.0, Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.23
- pytest 7.4.3, Flask-Testing 0.8.1
- requests 2.31.0 (for microservices)

### Additional Requirements (Microservices Only)
- **Docker**: Version 24.0+ with Docker Compose 2.20+
- **Download**: https://www.docker.com/products/docker-desktop/

---

## 2. Platform Installation & Configuration

### Install Python 3.11

**All Platforms**: Download from https://www.python.org/downloads/
- **Windows**: Run installer, check "Add Python to PATH"
- **macOS**: Run .pkg installer, check "Add Python to PATH"
- **Linux**: `sudo apt install python3.11 python3.11-venv python3-pip`

**Verify**: `python3 --version` (should show Python 3.11.x)

### Install pip
pip comes with Python 3.11. Verify: `pip3 --version`. If missing: `python3 -m ensurepip --upgrade`

### Install Docker (Microservices Only)
- **macOS/Windows**: Download Docker Desktop, install and launch
- **Linux**: `sudo apt install docker.io docker-compose && sudo systemctl start docker`
- **Verify**: `docker --version && docker compose version`

### Configure Virtual Environment (Layered Monolith)
```bash
cd Selected
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
**Windows PowerShell Note**: If activation fails, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 3. How to Compile

Python is interpreted, so "compilation" means installing dependencies and setting up the environment.

### Layered Monolith
```bash
cd Selected
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Database initializes automatically on first run.

### Microservices
```bash
cd Unselected
docker compose build
```
This builds Docker images for all four services (user-service, task-service, notification-service, frontend-service). Databases initialize when services start.

---

## 4. How to Execute

### Layered Monolith
```bash
cd Selected
source venv/bin/activate  # Windows: venv\Scripts\activate
python app.py
```
Access at http://localhost:5000

### Microservices
```bash
cd Unselected
docker compose up --build
```
Access frontend at http://localhost:5003. Services run on:
- User Service: http://localhost:5002
- Task Service: http://localhost:5000
- Notification Service: http://localhost:5001
- Frontend Service: http://localhost:5003

**Stop services**: `docker compose down`

---

## 5. Architecture Comparison & Implementation Differences

### Architecture Overview

This project implements two architectural styles:

1. **Layered Monolith (MVC)** - `Selected/` directory (Selected Architecture)
2. **Microservices** - `Unselected/` directory (Alternative Architecture)

### Layered Monolith Architecture

**Structure**:
```
Presentation Layer (Routes/Templates)
    ↓
Business Logic Layer (Services)
    ↓
Data Access Layer (Repositories)
    ↓
Data Layer (Models/Database)
```

**Key Characteristics**:
- Single deployable application
- Four layers: Presentation → Business Logic → Data Access → Data
- Repository pattern for data abstraction
- Single SQLite database for all entities
- In-process function calls between layers
- ACID transactions across all operations

**File Structure**:
```
Selected/
├── app.py                    # Application entry point
├── config.py                 # Configuration
├── models.py                 # SQLAlchemy models (User, Task, ActivityLog)
├── routes.py                 # Route handlers (Controller)
├── database/repositories.py  # Repository pattern (Data Access)
├── services/                 # Business logic
│   ├── task_service.py
│   └── notification_service.py
├── templates/                # Jinja2 templates
└── static/                   # CSS/JS
```

**Communication**: Direct function calls (zero network overhead)
```python
# Route → Service → Repository → Database
@app.route('/api/tasks', methods=['POST'])
def create_task():
    task = TaskService.create_task(...)  # Direct call
    return jsonify(task.to_dict())
```

**Data Access**: Repository pattern with shared database
- Foreign key relationships: `Task.assigned_to` → `User.id`
- ORM relationships: `task.assignee` provides direct User access
- Join queries across tables
- Single database session

**Reusable Components**:
- Repository classes (TaskRepository, UserRepository, ActivityLogRepository)
- Service classes (TaskService, NotificationService)
- Shared models, configuration, and database connection

### Microservices Architecture

**Structure**:
```
User Service (Port 5002) ←→ Task Service (Port 5000) ←→ Notification Service (Port 5001)
                                    ↓
                            Frontend Service (Port 5003)
```

**Key Characteristics**:
- Four independent services (User, Task, Notification, Frontend)
- Separate databases per service (except Notification, which is stateless)
- HTTP REST APIs for inter-service communication
- Docker containerization
- Service discovery via Docker service names
- Independent deployment per service

**File Structure**:
```
Unselected/
├── docker-compose.yml
├── user-service/          # User CRUD, validation
├── task-service/          # Task CRUD, assignments, activity log
├── notification-service/  # Events, notifications (stateless)
└── frontend-service/      # Web UI, aggregates APIs
```

**Communication**: HTTP REST API calls
```python
# Frontend Service → Task Service (HTTP GET)
tasks = requests.get('http://task-service:5000/api/tasks').json()

# Task Service → User Service (HTTP GET for validation)
user = requests.get(f'http://user-service:5002/api/users/{user_id}').json()
```

**Data Access**: Direct queries with service boundaries
- No foreign keys across services: `assigned_to` is just an integer
- No ORM relationships: cannot use `task.assignee`
- Manual validation via HTTP calls
- Separate database connections per service
- Eventual consistency (no cross-service transactions)

**Reusable Components**:
- HTTP client helper functions (`get_from_service`, `post_to_service`)
- Service-specific connectors (`get_user_from_service`, `notify_notification_service`)
- Service URL configuration via environment variables

### Detailed Implementation Differences

#### 1. Source Code Structure

**Layered Monolith**:
- Single codebase with clear layer separation
- Unified models file with all domain entities
- Repository pattern abstracts database operations
- Service layer contains business logic
- Routes call services directly

**Microservices**:
- Multiple independent codebases (one per service)
- Distributed models (User in user-service, Task in task-service)
- No repository pattern (direct SQLAlchemy queries in routes)
- Business logic embedded in route handlers
- Frontend service aggregates data from multiple backend services

#### 2. Communication Mechanisms

**Layered Monolith**:
- In-process function calls (sub-millisecond latency)
- Synchronous execution in same thread
- Exception propagation through call stack
- Single database transaction can span multiple operations
- Type-safe with Python type hints

**Microservices**:
- HTTP REST API calls (1-10ms latency per call)
- Network overhead for serialization/deserialization
- Must handle network failures, timeouts, service unavailability
- JSON serialization required for all data transmission
- Service discovery via Docker service names
- Manual error propagation across service boundaries

#### 3. Data Model Differences

**Layered Monolith**:
```python
class Task(db.Model):
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Can access: task.assignee.username (direct relationship)
```
- Referential integrity enforced by database
- ORM relationships enable direct object access
- Efficient join queries
- Cascade operations supported

**Microservices**:
```python
# Task Service
class Task(db.Model):
    assigned_to = db.Column(db.Integer)  # Just integer, no foreign key
    # Must make HTTP call to get user details

# User Service
class User(db.Model):
    # No relationship to tasks (different service)
```
- No referential integrity across services
- Manual validation via HTTP calls
- No cross-service joins
- Eventual consistency challenges

#### 4. Error Handling

**Layered Monolith**:
- Unified error handling with exception propagation
- Single error context in same process
- Automatic database rollback on failures
- Full Python stack traces

**Microservices**:
- Distributed error handling
- Must handle network failures, timeouts, service unavailability
- Graceful degradation (services may continue if others fail)
- Partial failures possible
- Manual error propagation across boundaries

#### 5. Configuration Management

**Layered Monolith**:
- Single configuration file (`config.py`)
- Shared by all components
- One set of environment variables

**Microservices**:
- Per-service configuration files
- Service discovery URLs must be configured
- Docker environment variables in `docker-compose.yml`
- Multiple configuration points to manage

#### 6. Testing Approaches

**Layered Monolith**:
- Single test suite in `tests/` directory
- Shared test database
- Easy to mock repository layer
- Fast execution (no network calls)
- Can test entire request flow end-to-end

**Microservices**:
- Per-service test suites
- Must mock HTTP calls to other services
- Integration testing requires all services running
- Network mocking needed (e.g., `responses` library)
- More complex setup

#### 7. Deployment

**Layered Monolith**:
- Single deployment: `pip install -r requirements.txt && python app.py`
- One process, one database
- Simple infrastructure (Python runtime + database)

**Microservices**:
- Containerized deployment: `docker compose up --build`
- Four services, multiple databases
- Requires Docker, orchestration, networking
- Health checks and service monitoring needed

### Comparison Table

| Aspect | Layered Monolith | Microservices |
|--------|-----------------|---------------|
| **Deployment** | Single application | 4 separate services |
| **Database** | 1 SQLite database | 3 separate databases |
| **Communication** | Function calls (in-process) | HTTP REST APIs (network) |
| **Scalability** | Vertical scaling (entire app) | Horizontal scaling per service |
| **Fault Tolerance** | Single point of failure | Isolated failures |
| **Development Speed** | Fast (single codebase) | Slower (coordination needed) |
| **Testing** | Simple (unified suite) | Complex (per-service + mocking) |
| **Transaction Management** | ACID across all operations | Eventual consistency |
| **Network Calls** | None (internal) | Multiple HTTP calls |
| **Setup Complexity** | Low (pip install) | Medium (Docker required) |
| **Memory Footprint** | Low (~50-100MB) | Higher (~200-300MB total) |
| **Startup Time** | Fast (<1 second) | Slower (Docker + 4 services) |

---

## 6. Architecture Design Decisions & Rationale

### Selected Architecture: Layered Monolith (MVC)

After analyzing both approaches, the **Layered Monolith** was selected as the primary architecture.

### Rationale for Selection

#### 1. Project Scope & Requirements
- Small to medium scale (5-20 users, <100 concurrent)
- Limited feature set (CRUD, assignments, notifications)
- Academic context (demonstration, not production at scale)
- All features efficiently implementable in monolithic structure

#### 2. Development Team Size
- Small team (1-3 developers)
- Limited resources and infrastructure knowledge
- Rapid development and iteration needed
- Easier for small teams to understand and maintain

#### 3. Complexity vs. Benefit Analysis
- Microservices overhead (4 services, Docker, networking) outweighs benefits at this scale
- Monolith simplicity: single codebase, single deployment, easier debugging
- YAGNI principle: avoid premature complexity
- Lower operational overhead and maintenance burden

#### 4. Performance Considerations
- Network latency: microservices add HTTP overhead (1-10ms per call)
- Transaction management: monolith provides ACID transactions
- Data consistency: easier in single database
- Response time: direct function calls faster than HTTP requests
- Resource efficiency: single process uses less memory/CPU

#### 5. Development & Maintenance
- Faster development (no service coordination)
- Easier testing (all components in one environment)
- Simpler debugging (single codebase, single log)
- Lower operational overhead (one application to monitor)
- Easier onboarding for new developers

#### 6. Future Scalability Path
- Evolutionary architecture: can refactor to microservices if needed
- Proven pattern: many companies start with monoliths (Amazon, Netflix)
- Clear migration path to extract services when scale demands
- Avoid premature optimization

#### 7. Technology Stack Alignment
- Python/Flask well-suited for monolithic applications
- SQLite sufficient for small to medium scale
- Simple deployment (no container orchestration)
- Resource efficient

#### 8. Academic & Learning Objectives
- Demonstrates solid architectural principles without unnecessary complexity
- Shows proper layering, separation of concerns, design patterns
- Educational value: easier for students to understand
- Provides clear contrast with microservices for learning

### When Microservices Would Be Preferred

Microservices would be better if:
- Large scale (100+ concurrent users, millions of tasks)
- Large team (10+ developers needing independent work streams)
- Different technologies needed per service
- Independent scaling required (very different load patterns)
- Fault tolerance critical (system must continue if one component fails)
- Regulatory requirements (strict service isolation)
- Geographic distribution needed
- Complex business logic per service
- Different teams own different services

### Conclusion

For this project's scope, team size, and requirements, the Layered Monolith provides optimal balance of:
- **Simplicity**: Easy to understand, develop, and maintain
- **Speed**: Rapid development and deployment
- **Reliability**: Single point of deployment reduces failure modes
- **Cost**: Lower infrastructure and operational costs
- **Performance**: Faster response times, lower latency
- **Resource Efficiency**: Lower memory and CPU usage

**Key Takeaway**: Start simple with a monolith, evolve to microservices only when benefits clearly outweigh costs.

### Architecture Design Decisions

#### Layered Monolith Design Decisions

**1. Four-Layer Architecture** (Presentation → Business Logic → Data Access → Data)
- Clear separation of concerns
- Testability (each layer independently testable)
- Maintainability (changes isolated to specific layers)
- Follows industry-standard MVC/MVP patterns
- Enables dependency inversion

**2. Repository Pattern**
- Abstraction from ORM details
- Easy to create mock repositories for testing
- Flexibility to change data storage without affecting business logic
- Single responsibility principle
- Enables test-driven development

**3. Service Layer**
- Business logic in service classes, not controllers
- Reusability across controllers
- Testability without HTTP layer
- Clear separation (controllers handle HTTP, services handle business rules)

**4. SQLite Database**
- Simplicity (no separate server needed)
- Portability (database file included with application)
- Sufficient for project scale
- Easy setup (zero configuration)

**5. Flask Framework**
- Lightweight (minimal overhead)
- Flexible structure (better for learning architecture)
- Simplicity for academic purposes
- More control over application structure

#### Microservices Design Decisions

**1. Four Services** (User, Task, Notification, Frontend)
- Single responsibility principle
- Independent development/deployment
- Independent scalability
- Clear domain boundaries

**2. HTTP REST APIs**
- Simplicity (easier to understand and debug)
- No additional infrastructure needed
- Standard protocol (widely understood)
- **Note**: Production systems often use message queues for better reliability

**3. Separate Databases**
- Data ownership (each service owns its data)
- Independence (services don't share database connections)
- Independent optimization
- Fault isolation
- Follows microservices best practices

**4. Docker Containerization**
- Consistency across environments
- Service isolation
- Portability
- Docker Compose simplifies orchestration
- Industry standard for microservices

**5. Service Discovery via DNS**
- Simplicity (no service registry like Consul needed)
- Docker-native (built into Docker networking)
- Sufficient for project requirements

**6. Stateless Notification Service**
- Simplicity (no database needed for basic functionality)
- Stateless (easier to scale horizontally)
- **Note**: Production systems would use a database for persistence

### Changes from Project Proposal

No significant changes were made to the candidate architectures from the project proposal. Both the Layered Monolith and Microservices architectures were implemented as originally planned. The selection of Layered Monolith as the primary architecture was based on the analysis above, which confirmed it as the most appropriate choice for the project's requirements and constraints.

---

## 7. Testing

### Layered Monolith
```bash
cd Selected
source venv/bin/activate
pytest tests/
```

### Microservices
```bash
cd Unselected
docker compose run --rm task-service pytest tests/
docker compose run --rm user-service pytest tests/
docker compose run --rm notification-service pytest tests/
```

---

## 8. Troubleshooting

### Common Issues

**Python version not 3.11**: Install Python 3.11 from python.org, use `python3.11` explicitly

**ModuleNotFoundError**: Ensure virtual environment is activated, reinstall: `pip install -r requirements.txt`

**Port already in use**: Find process: `lsof -i :5000` (macOS/Linux) or `netstat -ano | findstr :5000` (Windows), kill process or use different port

**Docker not starting**: Ensure Docker Desktop is running, restart Docker Desktop, verify: `docker --version`

**Database locked (SQLite)**: Close all connections, restart application, check for multiple instances

**Services can't communicate (Microservices)**: Verify all services running: `docker compose ps`, check service names match URLs, check logs: `docker compose logs <service-name>`

**Virtual environment not activating (Windows PowerShell)**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## Project Overview

This project implements a task management system using two architectural approaches to demonstrate and compare architectural styles, analyzing trade-offs, advantages, and suitability for different scenarios.

### Features

Both architectures implement:
- Create, edit, and manage tasks
- Assign tasks to team members
- Track progress with status updates
- Dashboard with statistics
- Calendar view for deadlines
- In-app notifications for upcoming deadlines
- Activity log of all task updates
- CSV export functionality

### Project Structure

```
.
├── Selected/              # Layered Monolith (MVC) Architecture
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   ├── database/
│   ├── templates/
│   └── tests/
│
└── Unselected/            # Microservices Architecture
    ├── task-service/
    ├── user-service/
    ├── notification-service/
    ├── frontend-service/
    └── docker-compose.yml
```

---

## Accessing Services

### Layered Monolith
- **Web Interface**: http://localhost:5000
- Dashboard: http://localhost:5000/
- Tasks: http://localhost:5000/tasks
- Calendar: http://localhost:5000/calendar

### Microservices
- **Web Interface**: http://localhost:5003
- **API Services**: 
  - User Service: http://localhost:5002
  - Task Service: http://localhost:5000
  - Notification Service: http://localhost:5001
- **Health Checks**: `/health` endpoint on each service

---

**Project**: CS5-7319 Final Project - Group 1 (Miller & Lomelin)  
**Architectures**: Layered Monolith (Selected) | Microservices (Unselected)  
**Last Updated**: 2024
