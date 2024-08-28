from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from uuid import UUID
from app.models.hotel import Hotel
from typing import List
import os

class HotelRepository:
    def __init__(self, cassandra_host: str = os.getenv("CASSANDRA_HOST", "localhost")):
        self.cluster = Cluster([cassandra_host])
        self.session = self.cluster.connect()
        self.KEYSPACE = "hotel_service"
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.KEYSPACE}
            WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
        """)
        self.session.set_keyspace(self.KEYSPACE)
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS hotels (
                hotel_id UUID PRIMARY KEY,
                name TEXT,
                address TEXT,
                rooms int
            )
        """)

    def add_hotel(self, hotel: Hotel):
        query = """
        INSERT INTO hotels (hotel_id, name, address, rooms) VALUES (%s, %s, %s, %s)
        """
        self.session.execute(query, (hotel.hotel_id, hotel.name, hotel.address, hotel.rooms))

    def get_hotels(self) -> List[Hotel]:
        rows = self.session.execute("SELECT * FROM hotels")
        return [Hotel(**row._asdict()) for row in rows]
