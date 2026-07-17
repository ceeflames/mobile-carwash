from sqlalchemy.orm import Session


class BaseRepository:

    def __init__(self, db: Session):
        self.db = db

    def add(self, instance):
        self.db.add(instance)

    def delete(self, instance):
        self.db.delete(instance)

    def flush(self):
        self.db.flush()

    def refresh(self, instance):
        self.db.refresh(instance)

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def save(self, instance):
        self.db.add(instance)
        self.db.flush()
        self.db.refresh(instance)
        return instance