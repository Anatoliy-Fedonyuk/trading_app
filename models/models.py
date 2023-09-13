from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)

    def __repr__(self) -> str:
        return f"Role :{self.id}, {self.name}, {self.permissions}"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey('roles.id'))

    def __repr__(self) -> str:
        return f"""Role :{self.id}, {self.email}, {self.username}, {self.password},
                        {self.registered_at}, {self.role_id}"""



### НО ВЕСЬ ЭТОТ БЛОК НЕ НУЖЕН ТАК МЫ С ПМОЩЬЮ МИГРАЦИЙ СОЗДАЕМ МОДЕЛИ И Т.Д.
# Создаем соединение с базой данных
# engine = create_engine('postgresql://fedonyuk:fedonyuk@127.0.0.1/postgres03')

# Создаем таблицы в базе данных
# Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
# Session = sessionmaker(bind=engine)
# session = Session()
