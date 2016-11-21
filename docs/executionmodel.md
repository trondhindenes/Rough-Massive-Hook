# The "Rough Massive Hook" execution model

I'm starting to regred that name a bit. Oh well.

The idea behind this project is to try and use containers/microservices as a pattern for a "classic" asp.net execution model, 
without actually using any container service in the app layer.

## What does this mean? 
Here's a simple container-based infrastructure:
(pics/containers.png)

Containerized apps (aka microservice instances) run on one or several container hosts. Client traffic is automatically distributed
to the right container using a load balancer in front of the container cluster. Some setups use a load balancer which is running on each 
container host, but logically those are the same.

As containers are deployed and destroyed all the time, the load balancer typically has some knowledge about the services it's
providing access to, either thru communication with the container scheduler running on the container hosts, or thru service discovery 
system such as Consul or etcd.

Rough Massive Hook takes the same approach, with a few key differences:
Firstly, since containers are not used IIS web apps serve as microservices, running on one or multiple hosts:
(pics/iis.png)

In contrast to a "classic" IIS-based setup, there's no need for IT/Ops to know exactly which server hosts a specific app. 
Utilizing the same service discovery model as container-based setups use, it's possible to completely abstract away the task of manually deciding
"which app goes where".

Given the fact that an IIS app works similar to a container, it reports its service to a service discovery system (Rought Massive Hook uses Consul), 
by telling the Consul Agent running on the host OS about this. Different tcp ports allow for simple separation of running services.

The fact that Rough Massive Hooks takes a very abstract approach to application placement, none of the existing popular deployment systems (Octopus Deploy, etc) 
will fit. Rough Massive Hook implements its own service ("LoneJupiter"), which performs the following tasks:
- Artifact database: LoneJupiter has a rest service which the build process calls. This allows LoneJupiter to store information about produced artifacts, and its metadata. With some tweaking, a regular nuget server could probably perform the same task.
- "Application Maps": An Application Map is a service description (comparable but a single node in Docker Compose's service definition, tho very simplified). An application map tells the system how many instances of an app should run, and which artifact to deploy to create that instance.
- Deployments: Deployments keep track of state, such as instance cound. When an ApplicationMap "orders" the system to deploy 3 instances of an app, 3 "deployments" are made to respond to this order. A deployment stores information such as which server the deployment will happen on, which port the app will run on, and so forth.
- Front-end configs: Front-end configs wire up the routing for a given app. As Rough Massive Hook allows multiple versions or branches of the same app to run on the same server, front-end configs control settings such as the weight ratio for the various app instances. Front-end configs are processed and written to Consul's KV store which are again used as the rule engine for the load balancers providing access to the app.

All in all, this setup allows a very flexible setup where the number of hosts (IIS Servers) are dictated by the needed compute resources, and not app isolation.
App placement (the which app goes where) is abstracted away using tags and optionally weigthing.

##The example app allows:
- Canary Deployments: Send 5% of the traffic bound to /api/v1 to an app running a newer version.
- A/B testing: Send 20% of the traffic bound for /api/v1 to an app running a build from the "devel" branch of the app.
- Api versioning: requests for api/v1 should be sent to version 1.0.0 of the app, while requests for api/v2 should be sent to a newer version of the same app.
- Prod and test apps on the same server


#Deployment pipeline/process:
Given an ApplicationMap where instancecount is changed from 2 to 3, LoneJupiter attempts to find the most suitable node for the new instance.
This placement is done using tag matching, although other mechanisms can easily be implemented. LoneJupiter attempts to spread an app on as many IIS hosts as possible, but allows a single hosts to run multiple instances if it has to.
The result of the placement process is a new "deployment" with status "pending", meaning the actual app hasn't been deployed yet.
The server targeted in the deployment is then instructed to download the required artifact and instal it. Upon installation, the IIS hosts's Consul config folder is updated with the added instance
The Load Balancing system picks up the added service instance when Consul receives a "green" healthcheck from the service, and traffic starts flowing to the instance.





