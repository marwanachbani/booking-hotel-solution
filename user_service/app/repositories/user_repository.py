from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection
from uuid import UUID
from typing import Optional
from app.models.user import User
import os

class UserModel(Model):
    __keyspace__ = 'user_service'
    user_id = columns.UUID(primary_key=True)
    email = columns.Text(index=True)
    hashed_password = columns.Text()
    full_name = columns.Text()
    role = columns.Text()
    created_at = columns.DateTime()

class UserRepository:
    def __init__(self, cassandra_host: str = os.getenv("CASSANDRA_HOST", "localhost")):
        cluster = Cluster([cassandra_host])
        session = cluster.connect()

        # Create the keyspace if it doesn't exist
        session.execute("""
        CREATE KEYSPACE IF NOT EXISTS user_service
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
        """)

        # Set the keyspace for the session
        session.set_keyspace('user_service')

        # Setup the connection for cqlengine
        connection.setup([cassandra_host], "user_service", protocol_version=3)

        # Sync the UserModel table with Cassandra
        sync_table(UserModel)

    def create_user(self, user: User):
        UserModel.create(
            user_id=user.user_id,
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            role=user.role,
            created_at=user.created_at
        )

    def get_user_by_email(self, email: str) -> Optional[User]:
        user_model = UserModel.objects(email=email).first()
        if user_model:
            return User(
                user_id=user_model.user_id,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                full_name=user_model.full_name,
                role=user_model.role,
                created_at=user_model.created_at
            )
        return None

    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        user_model = UserModel.objects(user_id=user_id).first()
        if user_model:
            return User(
                user_id=user_model.user_id,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                full_name=user_model.full_name,
                role=user_model.role,
                created_at=user_model.created_at
            )
        return None
