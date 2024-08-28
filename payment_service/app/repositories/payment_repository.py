from cassandra.cluster import Cluster
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import connection
from app.models.payment import Payment
from uuid import UUID
from typing import List

class PaymentModel(Model):
    __keyspace__ = 'payment_service'
    payment_id = columns.UUID(primary_key=True)
    booking_id = columns.UUID()
    amount = columns.Integer()
    currency = columns.Text()
    status = columns.Text()
    created_at = columns.DateTime()

class PaymentRepository:
    def __init__(self, cassandra_host: str = "localhost"):
        self.cluster = Cluster([cassandra_host])
        self.session = self.cluster.connect()
        
        # Set up the keyspace and connection
        self.KEYSPACE = "payment_service"
        
        # Check if keyspace exists; create if not
        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {self.KEYSPACE}
            WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
        """)
        
        # Set the keyspace for the session
        self.session.set_keyspace(self.KEYSPACE)
        
        # Set up the connection for cqlengine
        connection.setup([cassandra_host], self.KEYSPACE, protocol_version=3)
        
        # Synchronize the model with the Cassandra table
        sync_table(PaymentModel)

    def save_payment(self, payment: Payment):
        PaymentModel.create(
            payment_id=payment.payment_id,
            booking_id=payment.booking_id,
            amount=payment.amount,
            currency=payment.currency,
            status=payment.status,
            created_at=payment.created_at
        )

    def get_payment(self, payment_id: UUID) -> Payment:
        payment_model = PaymentModel.objects(payment_id=payment_id).first()
        if payment_model:
            return Payment(
                payment_id=payment_model.payment_id,
                booking_id=payment_model.booking_id,
                amount=payment_model.amount,
                currency=payment_model.currency,
                status=payment_model.status,
                created_at=payment_model.created_at
            )
        return None

    def get_payments_by_booking(self, booking_id: UUID) -> List[Payment]:
        payment_models = PaymentModel.objects(booking_id=booking_id).all()
        return [
            Payment(
                payment_id=payment_model.payment_id,
                booking_id=payment_model.booking_id,
                amount=payment_model.amount,
                currency=payment_model.currency,
                status=payment_model.status,
                created_at=payment_model.created_at
            )
            for payment_model in payment_models
        ]
