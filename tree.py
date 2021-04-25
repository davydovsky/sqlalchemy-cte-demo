import uuid
from typing import List

from sqlalchemy import literal, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased

from models import TreeNode


async def build_tree(
        session: AsyncSession,
        depth: int,
        node_num: int,
        parent_id: uuid.UUID = None,
        max_depth=5,
        children=5
) -> None:
    """
    Build tree with depth = {max_depth},
    where depth = 0 is the root of the tree.
    Each node nas {children} nodes.
    """
    if depth >= max_depth:
        return

    node = TreeNode(id=uuid.uuid4(), title=f'{depth}-{node_num}', parent_id=parent_id)
    session.add(node)

    start_num = node_num * children
    for num in range(start_num, start_num + children):
        await build_tree(session, depth + 1, num, node.id)


async def traverse_tree(
        session: AsyncSession,
        sort_fld: str = 'title',
        sort_dir: str = 'asc',
        depth: int = 1,
        start_node: str = None
) -> List[TreeNode]:
    """
    Traverse tree_node table with given
    start node (default - root) and given depth.
    """
    if not start_node:
        start_node = '0-0'

    tree = (select(TreeNode, literal(0).label('level'))
            .filter(TreeNode.title == start_node)
            .cte(name='tree', recursive=True))

    parent = aliased(tree, name='p')
    children = aliased(TreeNode, name='c')
    tree = tree.union_all(
        select(
            children, (parent.c.level + 1).label('level')
        ).filter(children.parent_id == parent.c.id, parent.c.level + 1 <= depth)
    )

    order_by_clause = desc(sort_fld) if sort_dir == 'desc' else sort_fld
    result_nodes = await session.execute(
        select(TreeNode).join(tree, TreeNode.id == tree.c.id).order_by(order_by_clause)
    )

    return [node._data[0] for node in result_nodes]
