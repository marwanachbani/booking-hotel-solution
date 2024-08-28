from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from uuid import UUID
from app.models.booking import Booking
from typing import List
import os

class BookingRepository:
    def __init__(self, cassandra_host: str = os.getenv("CASSANDRA_HOST", "localhost")):
        self.cluster = Cluster([cassandra_host])
        self.session = self.cluster.connect()
        self.KEYSPACE = "booking_service"
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.KEYSPACE}
            WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
        """)
        self.session.set_keyspace(self.KEYSPACE)
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id UUID PRIMARY KEY,
                hotel_id UUID,
                user_id UUID,
                room_number int,
                check_in_date date,
                check_out_date date
            )
        """)

    def add_booking(self, booking: Booking):
        query = """
        INSERT INTO bookings (booking_id, hotel_id, user_id, room_number, check_in_date, check_out_date) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.session.execute(query, (
            booking.booking_id, booking.hotel_id, booking.user_id,
            booking.room_number, booking.check_in_date, booking.check_out_date))

    def get_bookings_by_hotel(self, hotel_id: UUID) -> List[Booking]:
        query = "SELECT * FROM bookings WHERE hotel_id=%s"
        rows = self.session.execute(query, (hotel_id,))
        return [Booking(**row._asdict()) for row in rows]

    def get_bookings_by_user(self, user_id: UUID) -> List[Booking]:
        query = "SELECT * FROM bookings WHERE user_id=%s"
        rows = self.session.execute(query, (user_id,))
        return [Booking(**row._asdict()) for row in rows]
