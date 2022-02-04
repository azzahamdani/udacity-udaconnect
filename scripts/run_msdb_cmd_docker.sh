# Usage: pass in the DB container ID as the argument

# Set database configurations
export CT_DB_USERNAME=ct_admin
export CT_DB_NAME=geoconnections

DB=$1

cat ./db/${DB}_init-db.sql | docker exec -i $2 bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"
cat ./db/${DB}.sql | docker exec -i $2  bash -c "psql -U $CT_DB_USERNAME -d $CT_DB_NAME"

