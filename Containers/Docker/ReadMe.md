## **Core Docker Concepts**
<img width="1536" height="1024" alt="jpeg" src="https://github.com/user-attachments/assets/b6ecd8f3-2cee-4237-afa3-347e76ca157a" />

### 1. **Docker Image**
- A **read-only template** used to create containers.
- Includes application code, libraries, dependencies, and configuration.
- Built using a `Dockerfile`.

### 2. **Docker Container**
- A **runtime instance** of a Docker image.
- Lightweight, isolated, and portable.
- Can be started, stopped, moved, and deleted.

### 3. **Dockerfile**
- A script containing instructions to build a Docker image.
- Uses commands like `FROM`, `RUN`, `COPY`, `CMD`, etc.

### 4. **Docker Engine**
- The core part of Docker that runs on the host machine.
- Includes the **Docker daemon**, **REST API**, and **CLI**.

### 5. **Docker Daemon (`dockerd`)**
- Background service that manages containers, images, volumes, and networks.
- Communicates with the Docker client via REST API.

### 6. **Docker Client (`docker`)**
- Command-line interface to interact with the Docker daemon.
- Sends commands like `docker build`, `docker run`, etc.

### 7. **Docker Hub / Registry**
- A **repository** for Docker images.
- Docker Hub is the default public registry.
- You can also use private registries (e.g., AWS ECR, GitHub Container Registry).

### 8. **Volumes**
- Used for **persistent storage**.
- Allows data to persist across container restarts.
- Mounted using `-v` or defined in Docker Compose.

### 9. **Networks**
- Enables communication between containers.
- Types: **bridge**, **host**, **overlay**, and **none**.
- Defined using `docker network` or in Docker Compose.

### 10. **Docker Compose**
- Tool for defining and running **multi-container applications**.
- Uses a `docker-compose.yml` file.
- Simplifies orchestration and configuration.

### 11. **Layers & Caching**
- Each instruction in a Dockerfile creates a **layer**.
- Docker caches layers to speed up builds.
- Efficient layering improves performance and reduces image size.

### 12. **Port Mapping**
- Maps container ports to host ports using `-p` (e.g., `-p 8080:80`).
- Allows access to containerized services from outside.

### 13. **Environment Variables**
- Set using `ENV` in Dockerfile or `-e` in `docker run`.
- Useful for configuration and secrets management.

### 14. **Health Checks**
- Use `HEALTHCHECK` in Dockerfile to monitor container health.
- Helps in automated recovery and orchestration.

### 15. **Container Lifecycle**
- States: **created**, **running**, **paused**, **stopped**, **removed**.
- Managed using commands like `start`, `stop`, `restart`, `rm`.

## 🐳 **Docker CLI Commands Cheat Sheet**

### 📦 **Image Management**
| Command | Description |
|--------|-------------|
| `docker build -t <name> .` | Build an image from a Dockerfile |
| `docker images` | List all local images |
| `docker pull <image>` | Download image from Docker Hub |
| `docker push <image>` | Upload image to Docker Hub |
| `docker rmi <image>` | Remove an image |
| `docker tag <image> <new_name>` | Rename or tag an image |
| `docker save -o <file>.tar <image>` | Save image to a tar archive |
| `docker load -i <file>.tar` | Load image from a tar archive |

### 📦 **Container Management**
| Command | Description |
|--------|-------------|
| `docker run <image>` | Run a container from an image |
| `docker run -it <image> /bin/bash` | Run container interactively |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (including stopped) |
| `docker stop <container>` | Stop a running container |
| `docker start <container>` | Start a stopped container |
| `docker restart <container>` | Restart a container |
| `docker rm <container>` | Remove a container |
| `docker exec -it <container> <cmd>` | Run a command inside a running container |
| `docker logs <container>` | View container logs |
| `docker inspect <container>` | Detailed info about container/image |
| `docker top <container>` | Show running processes in a container |
| `docker kill <container>` | Forcefully stop a container |

### 🗃️ **Volumes & Storage**
| Command | Description |
|--------|-------------|
| `docker volume create <name>` | Create a volume |
| `docker volume ls` | List all volumes |
| `docker volume rm <name>` | Remove a volume |
| `docker volume inspect <name>` | View volume details |
| `docker run -v <host_path>:<container_path>` | Mount volume to container |

### 🌐 **Networking**
| Command | Description |
|--------|-------------|
| `docker network ls` | List all networks |
| `docker network create <name>` | Create a new network |
| `docker network inspect <name>` | View network details |
| `docker network rm <name>` | Remove a network |
| `docker run --network <name>` | Attach container to a network |
| `docker run -p <host>:<container>` | Map container port to host port |

### 🧹 **System Cleanup**
| Command | Description |
|--------|-------------|
| `docker system prune` | Remove unused data (containers, images, volumes) |
| `docker container prune` | Remove stopped containers |
| `docker image prune` | Remove unused images |
| `docker volume prune` | Remove unused volumes |
| `docker network prune` | Remove unused networks |

### 🧪 **Debugging & Monitoring**
| Command | Description |
|--------|-------------|
| `docker stats` | Show real-time resource usage of containers |
| `docker events` | Stream real-time Docker events |
| `docker diff <container>` | Show changes in container filesystem |

### 🧰 **Docker Compose**
| Command | Description |
|--------|-------------|
| `docker-compose up` | Start services defined in `docker-compose.yml` |
| `docker-compose down` | Stop and remove containers, networks, volumes |
| `docker-compose build` | Build images defined in the compose file |
| `docker-compose logs` | View logs from all services |
| `docker-compose ps` | List containers managed by Compose |

## 🐳 **Dockerfile Commands with Descriptions**

| **Command** | **Description** | **Common Options / Usage** |
|-------------|------------------|-----------------------------|
| `FROM` | Specifies the base image to use | `FROM python:3.10-slim` |
| `LABEL` | Adds metadata to the image | `LABEL maintainer="anurag@example.com"` |
| `ENV` | Sets environment variables | `ENV APP_ENV=production` |
| `ARG` | Defines build-time variables | `ARG VERSION=1.0` |
| `WORKDIR` | Sets the working directory inside the container | `WORKDIR /app` |
| `COPY` | Copies files from host to container | `COPY . /app` |
| `ADD` | Like `COPY`, but supports remote URLs and auto-extracts archives | `ADD https://example.com/file.tar.gz /data/` |
| `RUN` | Executes commands during image build | `RUN apt-get update && apt-get install -y curl` |
| `CMD` | Default command to run when container starts | `CMD ["python", "main.py"]` |
| `ENTRYPOINT` | Sets the main command; arguments passed via `CMD` or CLI | `ENTRYPOINT ["python"]` |
| `EXPOSE` | Documents the port the container listens on | `EXPOSE 8080` |
| `VOLUME` | Creates a mount point for persistent data | `VOLUME ["/data"]` |
| `USER` | Specifies the user to run the container | `USER appuser` |
| `HEALTHCHECK` | Defines a command to check container health | `HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1` |
| `SHELL` | Overrides the default shell used in `RUN` commands | `SHELL ["/bin/bash", "-c"]` |
| `ONBUILD` | Adds a trigger instruction for child images | `ONBUILD RUN pip install -r requirements.txt` |
| `STOPSIGNAL` | Sets the system call signal to stop the container | `STOPSIGNAL SIGTERM` |

### 🧠 **Tips for Using Dockerfile Commands**
- Use `RUN` commands efficiently by chaining them to reduce image layers.
- Prefer `COPY` over `ADD` unless you need archive extraction or remote URLs.
- Use `ENV` and `ARG` to make your Dockerfile configurable.
- Use `ENTRYPOINT` for fixed commands and `CMD` for default arguments.
