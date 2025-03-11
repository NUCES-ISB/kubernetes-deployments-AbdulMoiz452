# Replica Count Investigation

This document will contain the investigation of the minimum and maximum replicas count in the deployment.

## Current Deployment Configuration

In our current Flask application deployment, we have set:
- Default replicas: 2
- No explicit min/max replicas (as we're not using Horizontal Pod Autoscaler)

## Horizontal Pod Autoscaler (HPA)

To implement automatic scaling based on metrics, we would need to create a Horizontal Pod Autoscaler (HPA) resource. Here's an example of how it would be configured:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

## Min Replicas Investigation

The minimum number of replicas determines the baseline availability of the application. Setting this too low might affect availability during traffic spikes, while setting it too high might waste resources during low-traffic periods.

Factors to consider when setting minimum replicas:
1. Base level of traffic expected
2. Importance of high availability
3. Cold start time of the application
4. Resource constraints of the cluster

For our Flask application, a minimum of 1 replica would be sufficient for development/testing, but 2 replicas would be recommended for production to ensure high availability.

## Max Replicas Investigation

The maximum number of replicas limits how much the application can scale during high-traffic periods. Setting this too low might lead to performance degradation under heavy load, while setting it too high might risk overwhelming the cluster resources.

Factors to consider when setting maximum replicas:
1. Peak traffic expectations
2. Resource limits of the cluster
3. Performance characteristics of the application
4. Cost considerations

For our Flask application, a maximum of 5 replicas should be sufficient to handle moderate traffic spikes while preventing excessive resource consumption.

## Resource Utilization and Scaling

The decision to scale is typically based on resource utilization metrics such as CPU and memory usage. In our example HPA configuration, we would scale up when average CPU utilization exceeds 50%.

## Conclusion

Properly configuring minimum and maximum replica counts is essential for balancing application availability, performance, and resource efficiency. For our Flask application, we recommend:

- Minimum replicas: 2 (for high availability)
- Maximum replicas: 5 (for handling traffic spikes)
- Scaling metric: CPU utilization > 50%

These values should be adjusted based on actual traffic patterns and performance observations in a production environment.
