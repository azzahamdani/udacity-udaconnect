# Deploy Application 

1. Apply kafka 
```sh
kubectl apply -f kafka
```

2. Apply Person Microservice

```sh
kubectl apply -f person-service
```

3. Apply Location Microservice
```sh
kubectl apply -f location-service
```

4. Apply Connection Microservice
```sh
kubectl apply -f connection-service
```

5. Apply API gateway
```sh
kubectl apply -f api-gateway
```

# Seed Databases

1. seed location database
```sh
sh scripts/run_db_cmd_location.sh $(kubectl get pod -l service=location-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```
2. seed person database
```sh
sh scripts/run_db_cmd_person.sh $(kubectl get pod -l service=person-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```

# Deploy Ingress

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.1/deploy/static/provider/baremetal/deploy.yaml

kubectl -n ingress-nginx patch svc ingress-nginx-controller --patch '{"spec": {"ports": [{"name": "http","port": 80, "nodePort": 30000}]}}'

## Clients To Verify Setup

* Kafka Client

```sh
kubectl run -it --rm --image=confluentinc/cp-kafka:latest --restart=Never --env=KAFKA_BROKER_ID=ignored --env=KAFKA_ZOOKEEPER_CONNECT=ignored  kafka-client -- bash
```

* Kafka Operations 
```sh
# list topics
kafka-topics --list --bootstrap-server uda-connect-kafka:9092

# create topic
kafka-topics --create --topic quickstart-events --bootstrap-server uda-connect-kafka:9092 --partitions 1 --replication-factor 1

# describe a topic 
kafka-topics --describe --topic quickstart-events --bootstrap-server uda-connect-kafka:9092
```

* Database clients

1. client for location database
```sh
kubectl run -it --rm --image=postgis/postgis:12-2.5-alpine --restart=Never postgres-client -- psql -h location-postgres -U ct_admin -d udaconnectlocation
```
2. client for person database
```sh
kubectl run -it --rm --image=postgis/postgis:12-2.5-alpine --restart=Never postgres-client -- psql -h person-postgres -U ct_admin -d udaconnectperson
```

* database operations 
```sh
# list databases
\l

# connect to a database
\c location

# list tables
\dt location

# view seeded data
SELECT * FROM table;

```
