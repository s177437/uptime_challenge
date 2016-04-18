This is the repository for the uptime challenge application. This repository contains different modules and will cover the manager interface, worker interface, and contain Dockerfile-templates needed to deploy workers. 


To execute the code in this repository the following infrastructure is needed: 

* A couchDB instance 
* A dedicated interpreter instance, where the manager can do API calls 
* X number of manager instances, representing each test to deploy.
* A set of workers to each manager.

