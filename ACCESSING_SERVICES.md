# How to Access the Services After Starting Docker

## Step 1: Start the Services

```bash
cd Unselected
docker compose up --build
```

Wait until you see messages like:
```
user-service    |  * Running on http://0.0.0.0:5002
task-service    |  * Running on http://0.0.0.0:5000
notification-service |  * Running on http://0.0.0.0:5001
```

## Step 2: Access the Services

### Option A: Using a Web Browser (Recommended)

The microservices architecture now includes a **Frontend Service** with a full web interface!

1. **Open your web browser** and navigate to:
   - **Frontend (Web UI)**: http://localhost:5003
   - **Dashboard**: http://localhost:5003/
   - **Tasks**: http://localhost:5003/tasks
   - **Calendar**: http://localhost:5003/calendar

2. **Health Check Endpoints** (for testing):
   - Frontend Service: http://localhost:5003/health
   - User Service: http://localhost:5002/health
   - Task Service: http://localhost:5000/health
   - Notification Service: http://localhost:5001/health

### Option B: Using curl (Command Line)

Open a **new terminal window** (keep Docker running in the first one) and try:

#### Check Service Health
```bash
# User Service
curl http://localhost:5002/health

# Task Service
curl http://localhost:5000/health

# Notification Service
curl http://localhost:5001/health
```

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

## Step 3: Alternative - Use the Layered Monolith

Both architectures now have web interfaces! You can also use the **Layered Monolith** (Selected/) which has a similar interface:

```bash
# In a new terminal
cd Selected
source venv/bin/activate  # or: venv\Scripts\activate on Windows
python app.py
```

Then open your browser to:
- **Dashboard**: http://localhost:5000
- **Tasks Page**: http://localhost:5000/tasks
- **Calendar**: http://localhost:5000/calendar

## Quick Reference: Service URLs

### Microservices (Unselected/)
- **Frontend (Web UI)**: http://localhost:5003
- **Dashboard**: http://localhost:5003/
- **Tasks**: http://localhost:5003/tasks
- **Calendar**: http://localhost:5003/calendar
- **User Service API**: http://localhost:5002
- **Task Service API**: http://localhost:5000
- **Notification Service API**: http://localhost:5001

### Layered Monolith (Selected/)
- **Web Interface**: http://localhost:5000
- **Dashboard**: http://localhost:5000/
- **Tasks**: http://localhost:5000/tasks
- **Calendar**: http://localhost:5000/calendar

## Troubleshooting

### Services Not Responding?
1. Check if services are running:
   ```bash
   docker compose ps
   ```
   All services should show "Up" status

2. Check service logs:
   ```bash
   docker compose logs task-service
   docker compose logs user-service
   docker compose logs notification-service
   ```

3. Verify ports are not in use:
   ```bash
   # macOS/Linux
   lsof -i :5000
   lsof -i :5001
   lsof -i :5002
   ```

### Can't Access localhost?
- Make sure Docker Desktop is running
- Try `127.0.0.1:5000` instead of `localhost:5000`
- Check firewall settings

## Example: Complete Workflow

```bash
# Terminal 1: Start Docker services
cd Unselected
docker compose up --build

# Terminal 2: Test the services
# Create a user
curl -X POST http://localhost:5002/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com"}'

# Create a task (using user ID 1)
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Complete project","description":"Finish the final project","priority":"high","created_by":1}'

# Get all tasks
curl http://localhost:5000/api/tasks
```

## Using Postman or Similar Tools

1. **Download Postman**: https://www.postman.com/downloads/
2. **Create a new request**:
   - Method: GET
   - URL: http://localhost:5000/api/tasks
   - Click "Send"
3. **Create a POST request**:
   - Method: POST
   - URL: http://localhost:5002/api/users
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
     ```json
     {
       "username": "testuser",
       "email": "test@example.com"
     }
     ```

