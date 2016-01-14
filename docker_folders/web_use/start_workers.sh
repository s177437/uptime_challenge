#!/bin/bash
docker run -d -P --name webuseworker1 webuseworker
docker run -d -P --name webuseworker2 webuseworker
docker run -d -P --name webuseworker3 webuseworker
docker run -d -P --name webuseworker4 webuseworker
docker run -d -P --name webuseworker5 webuseworker
#docker run -d -P --name webuseworker6 webuseworker
#docker run -d -P --name webuseworker7 webuseworker
