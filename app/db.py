from sqlalchemy import create_engine, Column, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./iasw.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class PendingRequest(Base):
    __tablename__ = "pending_requests"

    request_id = Column(String, primary_key=True)
    customer_id = Column(String)
    change_type = Column(String)

    old_value = Column(String)
    new_value = Column(String)

    extracted_old = Column(String)
    extracted_new = Column(String)

    confidence_score = Column(Float)
    status = Column(String)

    summary = Column(Text)
    file_path = Column(String)
    checker_decision = Column(String)