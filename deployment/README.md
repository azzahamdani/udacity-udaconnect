# Push Docker images
## Docker commands used to build the application 
docker build -t udaconnect-person-api -f ./Dockerfile .
docker tag udaconnect-person-api:latest zoeid/udaconnect-person-api:latest
docker push zoeid/udaconnect-person-api:latest



# Deploy Application 
1. Apply Person Microservice

kubectl apply -f person-service




# Seed Databases

1. seed location database
```sh
sh scripts/run_db_cmd_k8s_location.sh $(kubectl get pod -l app=location-ms-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```
2. seed person database
```sh
sh scripts/run_db_cmd_person.sh $(kubectl get pod -l app=person-postgres --no-headers -o jsonpath='{.items[0].metadata.name}{"\n"}')
```

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
kubectl run -it --rm --image=postgis/postgis:12-2.5-alpine --restart=Never postgres-client -- psql -h location-ms-postgres -U ct_admin -d location
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
