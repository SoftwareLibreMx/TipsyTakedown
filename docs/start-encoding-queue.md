# Start Encoding queue

To start you need to run

With docker-compose
```sh
$ mkdir www/tmp
$ make start-encoding-docker
```
else
```sh
$ mkdir www/tmp
$ make start-encoding
```

## Possible errors

*`Out of storage`. This is because the encoding queue uses tmp files
*`Can use Minio`. You need to add your .env file

Its important to know that the decition to not make it a parallel encoder was based on system specs.
its more likely that you have enough space and CPU/GPU power to run 1 by 1 instead of Threating the process
