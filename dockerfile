# 1. BASE IMAGE SELECTION
# Tells Docker to use Python 3.12 running on a lightweight Linux distribution ("slim").
# Think of this as pulling a clean, lightweight Linux laptop out of a box with Python already installed.
FROM python:3.13.5-slim

# 2. WORKSPACE CREATION
# Sets the internal working directory inside the container to '/app'.
# Any commands executed after this line will run inside this folder, creating it if it doesn't exist yet.
WORKDIR /app

# 3. DEPENDENCY FILE TRANSFER
# Copies 'requirements.txt' from your host computer (local machine) into the current container directory (/app).
# We copy this file separately first to leverage Docker layer caching (so rebuilds are faster when code changes).
COPY requirements.txt .

# 4. DEPENDENCY INSTALLATION
# Installs all Python libraries listed in 'requirements.txt'.
# '--no-cache-dir' tells pip to delete downloaded cache files after installation, keeping the final Docker image size small.
RUN pip install --no-cache-dir -r requirements.txt

# 5. APPLICATION CODE TRANSFER
# Copies 'app.py' from your local computer into the container's '/app' folder.
COPY app.py .

# 6. PORT DOCUMENTATION
# Informs Docker (and developers) that the application inside the container listens on network port 9900.
# NOTE: This acts as internal documentation; you still need to map ports when running the container (e.g., -p 9900:9900).
EXPOSE 9900

# 7. CONTAINER STARTUP COMMAND
# The default command that executes when the container finishes building and starts up.
# Executes Uvicorn server as a module: running 'app:app' listening on all network interfaces (0.0.0.0) at port 9900.
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9900"]