# Used Stuff Market - Django Version

## Prerequisites

- Python3.13
- make
- [uv](https://docs.astral.sh/uv/#getting-started) to manage Python dependencies
- Container runtime - may be [docker](https://docs.docker.com/engine/install/), [colima](https://github.com/abiosoft/colima), [podman](https://podman.io/docs/installation) or a compatible alternative

## Installation

### Build project image and download other required images

```bash
docker compose pull redis postgres unleash
docker compose build shell
```

### Local installation (optional)

This step is recommended for optimal development experience, but not strictly required.

You can use full power of your IDE this way. 

```bash
make init
```

## Working with the project

### With containers only

**Start the project**

```bash
docker compose up
```

The application will be running on [http://localhost:8000](http://localhost:8000)

**Run migrations once PostgreSQL is ready**

```bash
docker compose run -it shell make migrate
```

**Run tests**

```bash
docker compose run -it shell make test
```

**Run formatter**

```bash
docker compose run -it shell make fmt
```

**Run linters and type checker**

```bash
docker compose run -it shell make lint
```

### With local installation

**Run dependencies**

```bash
docker compose up redis postgres unleash
```

**Start the project**

```bash
make run
```

The application will be running on [http://localhost:8000](http://localhost:8000)

**Run migrations once PostgreSQL is ready**

```bash
make migrate
```

**Run tests**

```bash
make test
```

**Run formatter**

```bash
make fmt
```

**Run linters and type checker**

```bash
make lint
```
