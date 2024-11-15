from datetime import datetime, date

from sqlalchemy import func, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


# association_table = Table(
#     "users_in_projects",
#     Base.metadata,
#     Column("user_id", ForeignKey("users.id"), primary_key=True),
#     Column("project_id", ForeignKey("projects.id"), primary_key=True),
# )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), server_default=func.now())

    # projects: Mapped[set['Project']] = relationship(
    #     secondary=association_table, back_populates="contributors"
    # )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]

    # contributors: Mapped[set[User]] = relationship(
    #     secondary=association_table, back_populates="projects"
    # )
    sprints: Mapped[set['Sprint']] = relationship(back_populates='project', uselist=True)


class Sprint(Base):
    __tablename__ = "sprints"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str]
    sprint_status: Mapped[str]

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete='CASCADE'))
    project: Mapped['Project'] = relationship(Project, uselist=False, back_populates='sprints')

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), server_default=func.now())
    started_at: Mapped[datetime]
    finished_at: Mapped[datetime]

    entities: Mapped[set['Entity']] = relationship(back_populates='sprint', uselist=True)


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    entity_id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)

    sprint_id: Mapped[int | None] = mapped_column(ForeignKey('sprints.id', ondelete='SET NULL'))
    sprint: Mapped[Sprint] = relationship(uselist=False, back_populates='entities')

    name: Mapped[str]
    area: Mapped[str]
    type: Mapped[str]
    status: Mapped[str]
    state: Mapped[str]
    priority: Mapped[str]
    ticket_number: Mapped[str]
    created_at: Mapped[datetime]
    # created_by:
    updated_at: Mapped[datetime]
    # updated_by: Mapped[]
    parent_ticket_id: Mapped[int | None]
    # assignee: Mapped[]
    # owner: Mapped[]
    due_date: Mapped[date | None]
    rank: Mapped[str]
    estimation: Mapped[int | None]
    workgroup: Mapped[str | None]
    resolution: Mapped[str | None]

    changes_history: Mapped[set['EntityChanging']] = relationship(back_populates='entity', uselist=True)


class EntityChanging(Base):
    __tablename__ = "entities_changing"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    entity_id: Mapped[int | None] = mapped_column(ForeignKey('entities.entity_id', ondelete='SET NULL'), nullable=True)
    entity: Mapped[Entity | None] = relationship(back_populates='changes_history', uselist=False)

    property_name: Mapped[str] = mapped_column(index=True)
    date: Mapped[datetime]
    version: Mapped[int]
    change_type: Mapped[str]
    changed_from: Mapped[str | None]
    changed_to: Mapped[str | None]










