# Guide to Running the openVPNManagement Project

## Introduction
The openVPNManagement project is designed to efficiently manage OpenVPN servers. It provides a user-friendly interface and tools to facilitate the management of multiple OpenVPN instances. This guide will help you install and run the project using Docker, ensuring a smooth setup process.

## System Requirements
Before you begin, ensure that you have the following software installed:
- **Docker**: Latest version.
- **Docker Compose**: Latest version.

## Project Structure
The project includes the following files and directories:
- `docker-compose.yml`: Configuration file for Docker Compose.
- `Dockerfile`: Configuration file to build the Docker image for the application.

## Installation and Running Guide

### Step 1: Download the Source Code
Clone or download the source code of the project to your local machine using the following command:

```bash
git clone https://github.com/hepham/openVPNManagement.git
cd openVPNManagement
```

### Step 2: Build and Run the Project
Open a terminal and navigate to the directory containing the `docker-compose.yml` file. Run the following command to build and start the services:

```bash
docker-compose up --build -d
```

- This command will build the Docker image and start the services in detached mode.

### Step 3: Check the Status
Once the services are up and running, you can check their status using the following command:

```bash
docker-compose ps
```

### Step 4: Check Logs
If you need to check logs to monitor the application's activity, you can use the following commands:

- To view logs for the web service:
  ```bash
  docker-compose logs web
  ```


### Step 5: Stop the Services
When you want to stop the services, you can use the following command:

```bash
docker-compose down
```
## Running the Application Directly

### Option 1: Running with Python
If you prefer to run the application directly using Python, you can do so with the following command:

```bash
python wsgi.py
```

- This will start the Flask application on the default port (usually 4000).

### Option 2: Running with Gunicorn
To run the application using Gunicorn, you can use the following command:

```bash
gunicorn --bind 0.0.0.0:4000 wsgi:app
```

- This will start the application on port 4000.
## Conclusion
The openVPNManagement project provides an easy way to set up and manage OpenVPN servers. Follow the steps above to get the project up and running. If you encounter any issues, check the logs or refer to the official documentation for Docker.