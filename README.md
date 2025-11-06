# Task Management System - Architecture Comparison Project

## Project Overview

This project implements a task management system using two different architectural approaches:

1. **Layered Monolith (MVC)** - Located in `Selected/` directory (Selected Architecture)
2. **Microservices Architecture** - Located in `Unselected/` directory (Alternative Architecture)

The purpose of this project is to demonstrate and compare two architectural styles for building the same application, analyzing their trade-offs, advantages, and suitability for different scenarios.

## 📖 Documentation

**For detailed implementation instructions, please see: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)**

The implementation guide includes:
- Complete platform setup instructions
- Step-by-step compilation and execution guides
- Detailed architecture comparison
- Rationale for architecture selection
- Testing instructions
- Troubleshooting guide

## Project Structure

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
    ├── notification-service/
    ├── docker-compose.yml
    └── README.md
```

## Architecture Descriptions

### Layered Monolith (MVC) - Selected Architecture

The **Layered Monolith** architecture serves as the primary design for this software system. It provides a simple, unified structure ideal for small development teams. This version integrates the user interface, application logic, and database into a single, organized framework with clear separation of concerns.

**Key Features:**
- Three-layer architecture: Presentation, Business Logic, Data
- Single deployable application
- Simplified development and testing
- All components share the same codebase and database

**Technology Stack:**
- Python 3.11
- Flask (web framework)
- Jinja2 (templates)
- SQLite (database)
- SQLAlchemy (ORM)

### Microservices Architecture - Unselected Architecture

The **Microservices** version separates the application into two independent but connected services:

1. **Task Service**: Manages all core functions (creating, updating, organizing tasks)
2. **Notification Service**: Focuses on sending alerts and reminders

These services communicate through lightweight HTTP APIs, allowing each to function and scale separately.

**Key Features:**
- Independent services with separate deployments
- Better fault isolation
- Scalable architecture
- Service-to-service communication via REST APIs

**Technology Stack:**
- Python 3.11
- Flask (REST APIs)
- SQLite (Task Service)
- Docker & Docker Compose
- HTTP for inter-service communication

## Rationale for Architecture Selection

After analyzing both architectural options, the **Layered Monolith (MVC Architecture)** is the most suitable choice for developing this project.

### Why Layered Monolith?

1. **Simplicity**: The monolithic design simplifies development, testing, and maintenance
2. **Small Team**: Ideal for small development teams with limited resources
3. **Rapid Development**: Enables faster iteration and easier debugging
4. **All-in-One**: Supports all required features without the overhead of managing multiple services
5. **Low Complexity**: No need to manage separate deployments, service communication, or additional configuration

### Why Not Microservices (for this project)?

While microservices offer better scalability and fault isolation, they introduce significant complexity:
- Managing separate deployments
- Inter-service communication overhead
- Additional configuration and orchestration
- More coordination required than a small team can reasonably support

Microservices are valuable for large, distributed systems requiring modularity and independent scaling, but this project's scope and resources align better with the simplicity and efficiency of a monolithic design.

## Quick Start

### Prerequisites
- Python 3.11 or later
- pip (Python package manager)
- Docker & Docker Compose (for Microservices only)

### Layered Monolith (Selected)

Quick start:
```bash
cd Selected
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Access at: http://localhost:5000

### Microservices (Unselected)

**Prerequisites**: Docker Desktop must be installed and running.

Quick start:
```bash
cd Unselected
docker compose up --build
```

**Note**: If you get "command not found", try:
- `docker-compose up --build` (older Docker versions)
- Or install Docker Desktop: https://www.docker.com/products/docker-desktop/
- See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed setup instructions

**Web Interface**: http://localhost:5003
- Dashboard: http://localhost:5003/
- Tasks: http://localhost:5003/tasks
- Calendar: http://localhost:5003/calendar

**API Services** (backend):
- User Service API: http://localhost:5002
- Task Service API: http://localhost:5000
- Notification Service API: http://localhost:5001
- Frontend Service: http://localhost:5003

**For detailed setup instructions, see [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)**

## Features

Both architectures implement the same core features:

- ✅ Create, edit, and manage tasks
- ✅ Assign tasks to team members
- ✅ Track progress with status updates
- ✅ Dashboard with statistics
- ✅ Calendar view for deadlines
- ✅ In-app notifications for upcoming deadlines
- ✅ Activity log of all task updates
- ✅ CSV export functionality

## Testing

Both architectures include comprehensive test suites:

**Layered Monolith:**
```bash
cd Selected
pytest tests/
```

**Microservices:**
```bash
cd Unselected/task-service
pytest tests/

cd Unselected/notification-service
pytest tests/
```

## Development Environment

- **IDE**: Visual Studio Code (compatible with macOS, Windows, Linux)
- **Python**: 3.11
- **Package Management**: pip/venv
- **Testing**: pytest
- **Source Control**: GitHub

## Project Goals

1. **Implementation**: Implement both architectural styles with the same feature set
2. **Comparison**: Analyze and compare the two approaches
3. **Documentation**: Provide comprehensive documentation for both architectures
4. **Best Practices**: Demonstrate sound architectural principles suitable for academic and small-scale professional use

## Future Considerations

The Layered Monolith provides the best balance of maintainability, reliability, and feasibility for this project, with the potential to evolve into a microservice-based model in the future if needed.

## License

This project is created for academic purposes as part of CS5-7319 Final Project.

## Authors

Group 1 - Miller & Lomelin

