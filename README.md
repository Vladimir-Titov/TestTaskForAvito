# TestTaskForAvito

This solution is for a test task: <https://github.com/avito-tech/mi-backend-trainee-assignment>
***

The application is started by the command `docker-compose up -d`

External storage in the `data` folder

The server start in <http://127.0.0.1:8080>
***
You have 3 way:

`/add?query=$1&region=$2`

This handler return id created record object

`/stat?id=$1&start=$2&end=$3`

This handler return list record with count and timestamp on between start-end

**start** and **end** need in format `%Y-%m-%d %H:%M`

`/top5?id=$1`

This handler return top 5 links for queryid in site avito