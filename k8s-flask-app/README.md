# Kubernetes Flask PostgreSQL Application

This repository contains a Flask-based web application with a PostgreSQL database deployed on a Kubernetes cluster.

## Project Structure

```
k8s-flask-app/
│── manifests/
│   │── deployment/
│   │   │── flask-deployment.yaml
│   │   │── postgres-deployment.yaml
│   │── service/
│   │   │── flask-service.yaml
│   │   │── postgres-service.yaml
│   │── configmap/
│   │   │── postgres-configmap.yaml
│   │── secret/
│   │   │── postgres-secret.yaml
│── app/
│   │── Dockerfile
│   │── requirements.txt
│   │── app.py
│── submission/
│   │── (screenshots and test results)
```

## Prerequisites

- Minikube installed and running
- kubectl configured to use Minikube
- Docker installed (for building the Flask application image)

## Deployment Steps

### 1. Start Minikube

```bash
minikube start
```

### 2. Build the Flask Application Docker Image

```bash
cd app
minikube image build -t flask-app:latest .
```

### 3. Deploy PostgreSQL

```bash
kubectl apply -f manifests/configmap/postgres-configmap.yaml
kubectl apply -f manifests/secret/postgres-secret.yaml
kubectl apply -f manifests/deployment/postgres-deployment.yaml
kubectl apply -f manifests/service/postgres-service.yaml
```

### 4. Deploy Flask Application

```bash
kubectl apply -f manifests/deployment/flask-deployment.yaml
kubectl apply -f manifests/service/flask-service.yaml
```

### 5. Access the Application

```bash
minikube service flask-app
```

## API Endpoints

- `/`: Welcome page
- `/health`: Health check endpoint
- `/db-test`: Test database connection
- `/init-db`: Initialize database with sample data
- `/tasks`: GET - List all tasks, POST - Create a new task

## Testing

### Database Connection Test

Access the `/db-test` endpoint to verify the connection to PostgreSQL.

### Initialize Database

Access the `/init-db` endpoint to create the tasks table and populate it with sample data.

### Scaling the Application

You can scale the Flask application deployment using:

```bash
kubectl scale deployment flask-app --replicas=3
```

## Cleanup

```bash
kubectl delete -f manifests/service/flask-service.yaml
kubectl delete -f manifests/deployment/flask-deployment.yaml
kubectl delete -f manifests/service/postgres-service.yaml
kubectl delete -f manifests/deployment/postgres-deployment.yaml
kubectl delete -f manifests/secret/postgres-secret.yaml
kubectl delete -f manifests/configmap/postgres-configmap.yaml
