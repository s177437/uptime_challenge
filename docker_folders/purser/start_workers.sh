#!/bin/bash
docker run -d -P --name purserworker1 purserworker
docker run -d -P --name purserworker2 purserworker
docker run -d -P --name purserworker3 purserworker
docker run -d -P --name purserworker4 purserworker
docker run -d -P --name purserworker5 purserworker
#docker run -d -P --name purserworker6 purserworker
#docker run -d -P --name purserworker7 purserworker
