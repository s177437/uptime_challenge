#!/bin/bash
docker run -d -P --name httperfworker1 httperfworker
docker run -d -P --name httperfworker2 httperfworker
docker run -d -P --name httperfworker3 httperfworker
docker run -d -P --name httperfworker4 httperfworker
docker run -d -P --name httperfworker5 httperfworker
#docker run -d -P --name httperfworker6 httperfworker
#docker run -d -P --name httperfworker7 httperfworker
