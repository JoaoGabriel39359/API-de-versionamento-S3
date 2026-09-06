# S3 File Versioning & Audit API

A FastAPI service for managing versioned files in Amazon S3, with recovery, logical deletion, and automated change auditing. The development environment runs entirely with Docker and LocalStack, so the workflow can be tested without an AWS account.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=flat-square&logo=fastapi&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS-S3-FF9900?style=flat-square&logo=amazons3&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-LocalStack-2496ED?style=flat-square&logo=docker&logoColor=white)

## What it solves

Object storage is simple until a file is overwritten or deleted accidentally. This API exposes a clear REST interface for the S3 version lifecycle and adds audit information that helps operators understand how files changed over time.

## Capabilities

- Upload files with S3 versioning
- List the complete version history of an object
- Restore an earlier version without deleting history
- Use delete markers for recoverable logical deletion
- Compare the latest and previous versions
- Audit file size and time between changes
- Develop locally with a reproducible Docker environment
- Explore and test endpoints through OpenAPI / Swagger

## Architecture

```text
Client
  |
  v
FastAPI routes
  |
  +--> S3 service --> Amazon S3
  |
  +--> Audit service
          
Local development: Docker Compose + LocalStack
```

## Tech stack

| Area | Technologies |
|---|---|
| API | Python 3.12, FastAPI |
| Cloud integration | Boto3, Amazon S3 |
| Local cloud | LocalStack |
| Infrastructure | Docker, Docker Compose |
| Documentation | OpenAPI / Swagger |

## Repository structure

```text
.
├── routes/
│   └── routes.py       # REST endpoints
├── services/
│   ├── s3_service.py   # S3 operations
│   └── audit.py        # Version comparison and audit rules
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Run locally

### Prerequisites

- Docker
- Docker Compose

### Start the stack

```bash
git clone https://github.com/JoaoGabriel39359/API-de-versionamento-S3.git
cd API-de-versionamento-S3
docker compose up --build
```

The API is available at `http://localhost:8000`, and its interactive documentation at `http://localhost:8000/docs`.

## API workflow

1. Upload an object.
2. Update the same key to create another version.
3. List its version history.
4. Request an audit comparison.
5. Restore a previous version or create a recoverable delete marker.

## Engineering focus

- Service modules isolate AWS-specific operations from HTTP routes.
- S3 versioning preserves traceability and recovery options.
- LocalStack makes integration development deterministic and inexpensive.
- Docker Compose gives contributors a one-command environment.

## Author

**João Gabriel Vieira Barbosa**  
Full-Stack Developer focused on Python, FastAPI, APIs, cloud integrations, and business automation.

[GitHub profile](https://github.com/JoaoGabriel39359)
