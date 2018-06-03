#! usr/bin/python3
"""
Date Created: 02-06-2018
Project: BalanceIt
@author: Vijayasai.S
"""

import os
import etcd


class Configuration:

    def __init__(self, postgresdb_host, postgresdb_port, postgresdb_database,
                 postgresdb_username, postgresdb_password):

        self.postgresdb_host = postgresdb_host
        self.postgresdb_port = postgresdb_port
        self.postgresdb_database = postgresdb_database
        self.postgresdb_username = postgresdb_username
        self.postgresdb_password = postgresdb_password

    @staticmethod
    def get_conf():
        """
        Class method to initialize the variables
        :return: class instance
        """

        host = os.environ["CONF_HOSTS"].split(",")[0]
        etcd_client = etcd.Client(host=host, port=2379)

        cf = {}
        cf.update({
            "postgresdb_host": etcd_client.read("/bi_postgres_db/host").value,
            "postgresdb_port": int(etcd_client.read("bi_postgres_db/port").value),
            "postgresdb_username": etcd_client.read("/bi_postgres_db/username").value,
            "postgresdb_password": etcd_client.read("/bi_postgres_db/password").value,
            "postgresdb_database": etcd_client.read("/bi_postgres_db/database").value
        })
        return Configuration(
            cf.get("postgresdb_host", None),
            cf.get("postgresdb_port", None),
            cf.get("postgresdb_database", None),
            cf.get("postgresdb_username", None),
            cf.get("postgresdb_password", None)
        )
