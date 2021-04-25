import datetime
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TreeNode(Base):
    __tablename__ = 'tree_node'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('tree_node.id'), index=True)
    title = Column(String(256), unique=True)
    registered_in = Column(DateTime, default=datetime.datetime.now)
    parent = relationship('TreeNode', remote_side=id, backref='sub_nodes')

    def __repr__(self):
        parent_title = self.parent.title if self.parent else '-'
        registered_in = self.registered_in.strftime('%Y-%m-%d %H:%M:%S')
        return f'Node {self.title}, parent {parent_title}, registered_in {registered_in}'
