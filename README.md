This is the repository for the manager python interface. This repository contains different modules and will cover the manager interface, Worker interface, and contain a dockerfile
with the ability to spawn dockers running as workers. 

To execute the code in this repository the following infrastructure is needed: 

A couchDB instance 
A dedicated interpreter instance, where the manager can do API calls 
X number of manager instances, representing each test to deploy.
A set of workers to each manager.

