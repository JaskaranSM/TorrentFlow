import os
from constants import Constants

class EnvironmentSettings(Constants):
    def __init__(self):
        super().__init__()
        self.handshake_client_version = ""
        self.user_agent = ""
        self.upload_rate_limit = 0
        self.connections_limit = 0
        self.handshake_client_version = ""
        self.listen_interfaces = ""
        self.dht_boostrap_nodes =""

        self.default_settings = {
            self.ENV_KEY_LT_LISTEN_INTERFACES: "0.0.0.0:16188",
            self.ENV_KEY_DHT_BOOTSTRAP_NODES: "dht.libtorrent.org:25401",
            self.ENV_KEY_HANDSHAKE_CLIENT_VERSION: "qBittorrent/4.3.8",
            self.ENV_KEY_PEER_ID: "-qB4380-",
            self.ENV_KEY_UPLOAD_RATE_LIMIT: 0,
            self.ENV_KEY_USER_AGENT: "qBittorrent/4.3.8",
            self.ENV_KEY_CONNECTIONS_LIMIT: 500
        }
        self.parse_env()

    def get_default_value(self, key):
        return self.default_settings[key]

    def get_env_var_else_default(self, key):
        return os.environ.get(key, self.get_default_value(key))

    def parse_env(self):
        self.handshake_client_version = self.get_env_var_else_default(self.ENV_KEY_HANDSHAKE_CLIENT_VERSION)
        self.user_agent = self.get_env_var_else_default(self.ENV_KEY_USER_AGENT)
        self.listen_interfaces = self.get_env_var_else_default(self.ENV_KEY_LT_LISTEN_INTERFACES)
        self.connections_limit = int(self.get_env_var_else_default(self.ENV_KEY_CONNECTIONS_LIMIT))
        self.dht_bootstrap_nodes = self.get_env_var_else_default(self.ENV_KEY_DHT_BOOTSTRAP_NODES)
        self.upload_rate_limit = int(self.get_env_var_else_default(self.ENV_KEY_UPLOAD_RATE_LIMIT))
        self.peer_id = self.get_env_var_else_default(self.ENV_KEY_PEER_ID)

    def get_lt_settings_dict(self):
        return {
            'connections_limit': self.connections_limit,
            'user_agent': self.user_agent,
            'listen_interfaces': self.listen_interfaces,
            'dht_bootstrap_nodes': self.dht_bootstrap_nodes,
            'peer_fingerprint': self.peer_id,
            'handshake_client_version': self.handshake_client_version,
            'upload_rate_limit': self.upload_rate_limit
        }