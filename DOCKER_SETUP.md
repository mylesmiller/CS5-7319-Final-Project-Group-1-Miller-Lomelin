# Docker Setup Guide

## Issue: `docker-compose` or `docker compose` command not found

### Solution 1: Install Docker Desktop (Recommended)

1. **Download Docker Desktop for macOS**:
   - Visit: https://www.docker.com/products/docker-desktop/
   - Download the version for Apple Silicon (M1/M2/M3) or Intel, depending on your Mac
   - Open the downloaded `.dmg` file
   - Drag Docker to Applications folder

2. **Launch Docker Desktop**:
   - Open Docker from Applications
   - Wait for Docker to start (whale icon in menu bar)
   - You may need to enter your password to allow Docker to run

3. **Verify Installation**:
   ```bash
   docker --version
   docker compose version
   ```

### Solution 2: Use Legacy docker-compose (if Docker is installed but old version)

If you have Docker installed but it's an older version, you may need to install `docker-compose` separately:

```bash
# Install docker-compose via Homebrew
brew install docker-compose

# Or via pip
pip3 install docker-compose
```

Then use:
```bash
docker-compose up --build
```

### Solution 3: Check if Docker is in PATH

If Docker is installed but not found:

```bash
# Check if Docker is installed
which docker

# If not found, add Docker to PATH (if installed in Applications)
export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"

# Add to ~/.zshrc to make permanent
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Quick Test

After installation, test with:

```bash
# Test Docker
docker --version

# Test Docker Compose (new syntax)
docker compose version

# If that doesn't work, try old syntax
docker-compose --version
```

### Running the Microservices

Once Docker is working, use the appropriate command:

**For Docker Compose V2 (newer Docker Desktop):**
```bash
cd Unselected
docker compose up --build
```

**For Docker Compose V1 (older installations):**
```bash
cd Unselected
docker-compose up --build
```

### Troubleshooting

- **"Cannot connect to Docker daemon"**: Make sure Docker Desktop is running
- **Permission denied**: You may need to add your user to the docker group (Linux) or ensure Docker Desktop has proper permissions (macOS)
- **Port already in use**: Stop other services using ports 5000, 5001, or 5002

