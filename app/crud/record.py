from sqlalchemy.orm import Session
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate

def get_records_by_zone(db: Session, hosted_zone_id: int):
    return db.query(Record).filter(Record.hosted_zone_id == hosted_zone_id).all()

def create_record(db: Session, record: RecordCreate, hosted_zone_id: int):
    db_record = Record(
        hosted_zone_id=hosted_zone_id,
        name=record.name,
        type=record.type,
        value=record.value,
        ttl=record.ttl
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_record(db: Session, record_id: int):
    return db.query(Record).filter(Record.id == record_id).first()

def update_record(db: Session, record_id: int, record: RecordUpdate):
    db_record = get_record(db, record_id)
    if db_record:
        for key, value in record.dict(exclude_unset=True).items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int):
    db_record = get_record(db, record_id)
    if db_record:
        db.delete(db_record)
        db.commit()
        return True
    return False