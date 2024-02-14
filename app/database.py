from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
import random

# Initialize Cassandra cluster
class CassandraConnection:
    def __init__(self):
        self.cluster = None
        self.session = None

    def connect(self, hosts, username, password, keyspace):
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        load_balancing_policy = RoundRobinPolicy()
        self.cluster = Cluster(contact_points=hosts, auth_provider=auth_provider, load_balancing_policy=load_balancing_policy)
        self.session = self.cluster.connect(keyspace)

    def close(self):
        if self.cluster:
            self.cluster.shutdown()

    def execute_query(self, query, params=None):
        statement = SimpleStatement(query)
        return self.session.execute(statement, parameters=params)

# Area Coverage Function
def get_cabs_in_area(latitude, longitude, radius):
    """Retrieve cabs within a specified radius of a given location."""
    # Example: Perform a spatial query to find cabs within the specified radius
    # For demonstration purposes, we'll generate random cab locations
    cab_locations = [
        {'cab_id': 'cab1', 'latitude': random.uniform(latitude - 0.01, latitude + 0.01), 'longitude': random.uniform(longitude - 0.01, longitude + 0.01)},
        {'cab_id': 'cab2', 'latitude': random.uniform(latitude - 0.01, latitude + 0.01), 'longitude': random.uniform(longitude - 0.01, longitude + 0.01)},
        {'cab_id': 'cab3', 'latitude': random.uniform(latitude - 0.01, latitude + 0.01), 'longitude': random.uniform(longitude - 0.01, longitude + 0.01)},
    ]
    return cab_locations

# Dynamic Pool Management for connection pooling
class ConnectionPoolManager:
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.connections = []

    def acquire_connection(self):
        """Acquire a connection from the pool."""
        if len(self.connections) < self.max_connections:
            connection = CassandraConnection()
            connection.connect(['127.0.0.1'], 'username', 'password', 'cab_tracking')  # Replace with your Cassandra credentials
            self.connections.append(connection)
            return connection
        else:
            return random.choice(self.connections)  # Return a random connection from the pool

    def release_connection(self, connection):
        """Release a connection back to the pool."""
        # No need to release connections for Cassandra

# Create a global connection pool
connection_pool = ConnectionPoolManager()

def store_location_data(data):
    """Store location data in the Cassandra database."""
    connection = connection_pool.acquire_connection()
    try:
        query = "INSERT INTO locations (cab_id, latitude, longitude) VALUES (?, ?, ?)"
        connection.execute_query(query, params=(data['cab_id'], data['latitude'], data['longitude']))
    finally:
        connection_pool.release_connection(connection)

def get_cab_locations(page=1, per_page=10):
    """Retrieve paginated cab locations from the Cassandra database."""
    connection = connection_pool.acquire_connection()
    try:
        query = "SELECT * FROM locations LIMIT ?"
        rows = connection.execute_query(query, params=(per_page,))
        cab_locations = [{'cab_id': row.cab_id, 'latitude': row.latitude, 'longitude': row.longitude} for row in rows]
        return cab_locations
    finally:
        connection_pool.release_connection(connection)
