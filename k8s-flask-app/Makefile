.PHONY: start build deploy clean scale-up scale-down test

# Start Minikube
start:
	minikube start

# Build Flask application Docker image
build:
	cd app && minikube image build -t flask-app:latest .

# Deploy all components
deploy: deploy-postgres deploy-flask

# Deploy PostgreSQL
deploy-postgres:
	kubectl apply -f manifests/configmap/postgres-configmap.yaml
	kubectl apply -f manifests/secret/postgres-secret.yaml
	kubectl apply -f manifests/deployment/postgres-deployment.yaml
	kubectl apply -f manifests/service/postgres-service.yaml

# Deploy Flask application
deploy-flask:
	kubectl apply -f manifests/deployment/flask-deployment.yaml
	kubectl apply -f manifests/service/flask-service.yaml

# Access the Flask application
access:
	minikube service flask-app

# Scale up Flask application replicas
scale-up:
	kubectl scale deployment flask-app --replicas=3

# Scale down Flask application replicas
scale-down:
	kubectl scale deployment flask-app --replicas=1

# Get all resources
get-all:
	kubectl get all

# Clean up all resources
clean:
	kubectl delete -f manifests/service/flask-service.yaml
	kubectl delete -f manifests/deployment/flask-deployment.yaml
	kubectl delete -f manifests/service/postgres-service.yaml
	kubectl delete -f manifests/deployment/postgres-deployment.yaml
	kubectl delete -f manifests/secret/postgres-secret.yaml
	kubectl delete -f manifests/configmap/postgres-configmap.yaml

# Stop Minikube
stop:
	minikube stop

# Full deployment process
all: start build deploy

# Test the application
test: access
	@echo "Access the following endpoints to test the application:"
	@echo "- / : Welcome page"
	@echo "- /health : Health check"
	@echo "- /db-test : Test database connection"
	@echo "- /init-db : Initialize database with sample data"
	@echo "- /tasks : List all tasks (GET) or create a new task (POST)"
