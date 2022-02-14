# How to run the project 
## Steps 


1. Deploy Kafka 

```sh
kubectl apply -f deployment/kafka
```

2. Deploy Person Microservices 
```sh
kubectl apply -f deployment/person-service
```

3. Deploy Location Microservices 
```sh
kubectl apply -f deployment/location-service
```

4. Deploy Connection Microservices 
```sh
kubectl apply -f deployment/connection-service
```

5. DeploY Api Gateway 

_to deploy API gateway, we need to deploy first an open-source ingress-controller_ `ingress nginx` _that will route the traffic to destinated microservices following our_ `ingress` _rules_

* Ingress Controller
```sh 
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.1/deploy/static/provider/baremetal/deploy.yaml
```
* Patching Ingress Controller Nodeort 
```sh

kubectl -n ingress-nginx patch svc ingress-nginx-controller --patch '{"spec": {"ports": [{"name": "http","port": 80, "nodePort": 30000}]}}'
```
* Ingress Rules
```sh
kubectl apply -f deployment/api-gateway
```
6. Deploy frontend 
```sh
kubectl apply -f deployment/frontend/
```

7. Seed databases

_`Before testing APIs` it is `mandatory` to seed person and location databases in order to create DB tables and some dummy data_

* Seed location db
```sh
sh scripts/run_db_cmd_location.sh $(kubectl get pod -l service=location-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```

* Seed person db
```
sh scripts/run_db_cmd_person.sh $(kubectl get pod -l service=person-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```

Once the project is up and running, you should be able to see 3 deployments and 3 services in Kubernetes:
`kubectl get pods` and `kubectl get services`

These pages should also load on your web browser:
* `http://localhost:30000/api/` - Base path for API
* `http://localhost:30050/` - Frontend ReactJS Application


