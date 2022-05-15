#!/bin/bash

touch ~/.pgpass

host=$(echo $GREEKLYAPI_RDS_SECRET | jq -r '.host')
port=$(echo $GREEKLYAPI_RDS_SECRET | jq -r '.port')
dbname=$(echo $GREEKLYAPI_RDS_SECRET | jq -r '.dbname')
username=$(echo $GREEKLYAPI_RDS_SECRET | jq -r '.username')
password=$(echo $GREEKLYAPI_RDS_SECRET | jq -r '.password')

echo "$host:$port:$dbname:$username:$password" >> ~/.pgpass

chmod 600 ~/.pgpass

export PGPASSFILE=~/.pgpass

psql -h "$host" -U "$username" "$dbname"