from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ChannelSubscriber(Base):
    """ Информация о подписчиках канала """
    __tablename__ = 'subscribers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    username: Mapped[str]
    channel_id: Mapped[int]