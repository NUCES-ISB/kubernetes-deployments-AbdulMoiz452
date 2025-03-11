# Scaling Test Documentation

This document will contain the results of testing the effect of scaling up and down the replica set for the Flask application.

## Scaling Up Test

### Command:
```bash
kubectl scale deployment flask-app --replicas=3
```

### Expected Result:
The number of Flask application pods should increase from 2 to 3.

### Observation:
When scaling up, we expect to see a new pod being created and entering the Running state. This demonstrates Kubernetes' ability to horizontally scale applications based on demand.

## Scaling Down Test

### Command:
```bash
kubectl scale deployment flask-app --replicas=1
```

### Expected Result:
The number of Flask application pods should decrease from 3 to 1.

### Observation:
When scaling down, we expect to see two pods being terminated. This demonstrates Kubernetes' ability to reduce resource usage when demand decreases.

## Impact on Application

Scaling operations should not disrupt the application's availability. The Kubernetes Service continues to distribute traffic to available pods, ensuring that the application remains accessible during scaling operations.

## Load Balancing

The Kubernetes Service automatically load balances traffic across all available pods. As the number of pods increases, the load is distributed more evenly, potentially improving application performance under high load.

## Resource Utilization

Scaling affects resource utilization:
- Scaling up increases CPU and memory usage on the cluster
- Scaling down frees up resources for other applications

## Conclusion

Kubernetes provides a simple and effective way to scale applications horizontally. This capability is essential for applications that experience variable load, allowing them to adapt to changing demand while maintaining performance and availability.
