import rethinkdb as r
import requests
import json

class ServerSelector(object):
    @staticmethod
    def get_deployment_candidates(rethinkdb_host, rethinkdb_port, rethinkdb_db, tags, count, current_deployments):

        servers_table = "servers"

        r.connect(rethinkdb_host, rethinkdb_port).repl()
        keys = r.db(rethinkdb_db).table(servers_table).run()
        db_servers = list(keys)

        matching_servers = []

        for server in db_servers:
            server_tags = server['servertags']
            tags_match = True
            for tag in tags:
                tag_name = tag['name']
                tag_value = tag['value']
                server_tag = [x for x in server_tags if x['name'] == tag_name and x['value'] == tag_value]
                if server_tag.__len__() == 1:
                    pass
                else:
                    tags_match = False
                    #Break out of loop, try next server
                    break

            if tags_match:
                matching_servers.append(server)

        matching_servers_count = matching_servers.__len__()
        server_removal_exhausted = False

        #Get current unique servers
        current_deplyment_servers = []
        for x in current_deployments:
            current_deployment_server = x['server']
            current_deplyment_servers.append(current_deployment_server)


        current_deployments_unique_servers = list(set(current_deplyment_servers))

        while True:
            matching_servers_count = matching_servers.__len__()
            if matching_servers_count > count:
                #remove a server
                removed_one = False
                for server in matching_servers:
                    matching_servers_contains_current = [x for x in current_deplyment_servers if x == server['name']]
                    if matching_servers_contains_current.__len__() > 0:
                        if removed_one == False:
                            matching_servers.remove(server)
                            removed_one = True
            if matching_servers_count <= count:
                # already have a good list
                break



        return matching_servers

    @staticmethod
    def get_free_port(server_name, root_url):
        url = root_url + "api/deployments/server/" + server_name
        result = requests.get(url)
        data = json.loads(result.content)

        test_port = 7000
        while True:
            port_free = [x for x in data if x['local_port'] == test_port]
            if port_free.__len__() == 0:
                return test_port
            else:
                test_port = test_port + 1