# Submission Folder

This folder will contain the following screenshots and test results once the deployment is run on a Minikube cluster:

1. **internal_deployment.png** - Snapshot of the internal deployment
2. **kubectl_get_all.png** - Snapshot of the output from 'kubectl get all' command
3. **scaling_test.md** - Documentation of testing the effect of scaling up and down the replica set
4. **replica_count_investigation.md** - Investigation of the min and max replicas count

## Steps to Generate These Files

1. Start Minikube:
   ```
   minikube start
   ```

2. Build the Flask application Docker image:
   ```
   cd app
   minikube image build -t flask-app:latest .
   ```

3. Deploy PostgreSQL:
   ```
   kubectl apply -f manifests/configmap/postgres-configmap.yaml
   kubectl apply -f manifests/secret/postgres-secret.yaml
   kubectl apply -f manifests/deployment/postgres-deployment.yaml
   kubectl apply -f manifests/service/postgres-service.yaml
   ```

4. Deploy Flask application:
   ```
   kubectl apply -f manifests/deployment/flask-deployment.yaml
   kubectl apply -f manifests/service/flask-service.yaml
   ```

5. Take a snapshot of the internal deployment:
   ```
   kubectl get deployments -o wide > submission/internal_deployment.txt
   ```

6. Take a snapshot of 'kubectl get all':
   ```
   kubectl get all > submission/kubectl_get_all.txt
   ```

7. Test scaling up and down the replica set:
   ```
   kubectl scale deployment flask-app --replicas=3
   kubectl get pods
   kubectl scale deployment flask-app --replicas=1
   kubectl get pods
   ```

8. Investigate min and max replicas count:
   ```
   kubectl describe deployment flask-app
   ```

Note: The actual screenshots and test results will be generated when the deployment is run on a Minikube cluster.
