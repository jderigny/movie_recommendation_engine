import neo4j


class Connect:
    def __init__(self, configuration):
        self.driver = neo4j.GraphDatabase.driver(configuration.uri,
                                                 auth=(configuration.user, configuration.password),
                                                 encrypted=False)

    def close(self):
        self.driver.close()
