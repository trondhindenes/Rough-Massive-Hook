# Rough-Massive-Hook
Proof of concept for n-tier app using modern tooling

### That name tho??
Found in in some project name generator. Thought it sounded kool.

### The why
Lots of orgs have huge codebases built around .Net "classic" and don't have an easy migration path to Containers. This project attempts to prove that it's possible to build a modern "microservice-like" application stack using modern tooling for service discovery, traffic routing and config/deploy.

### Components used
1. Consul: Consul serves multiple purposes:
* Service Discovery: Each application reports its currently running service(s) using Consul. The Consul service catalog wlil thereby serve as a "live view" of which applications and which versions are running where
* Routing/config: Consul's kv store is populated with info about routing and traffic weight. This setup allows the "Canary Deployment" pattern where a small subset of the traffic is directed to a different version of the service than the majority of users. This weighting is also configured in Consul KV.

2. Traefik: A modern web proxy/load balancer. Traefik gets its configuration from Consul (both service and kv), and is responsible for routing traffic to the right host/application. Traefik is used in two layers, where the first layer performs routing/weighting, and the second layer performs load balancing between available nodes

3. Windows Server 2016: Any windows server capable of running .Net/IIS will work. Each server has a number of IIS sites, where each site delivers one version of one app. In container pattern terms, each website functions as a container

4. DNS: internal DNS is used since much is based on wildcard dns queries

5. Ansible: Server configuration is done in using Ansible

6. LoneJupiter: A small rest service I threw togheter, which serves as an artifact database. Backed by a RethinkDB database.
