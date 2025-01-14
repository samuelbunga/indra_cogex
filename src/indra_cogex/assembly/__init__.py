from collections import defaultdict
from typing import Dict, List, Optional

from indra_cogex.representation import Node


class NodeAssembler:
    def __init__(self, nodes: Optional[List[Node]] = None):
        self.nodes = nodes if nodes else []
        self.conflicts: List[Conflict] = []

    def add_nodes(self, nodes: List[Node]):
        self.nodes += nodes

    def assemble_nodes(self) -> List[Node]:
        nodes_by_id = defaultdict(list)
        for node in self.nodes:
            nodes_by_id[(node.db_ns, node.db_id)].append(node)

        assembled_nodes = [
            self.get_aggregate_node(db_ns, db_id, node_group)
            for (db_ns, db_id), node_group in nodes_by_id.items()
        ]
        return assembled_nodes

    def get_aggregate_node(self, db_ns: str, db_id: str, nodes: List[Node]) -> Node:
        labels = set()
        data: Dict[str, str] = {}
        for node in nodes:
            labels |= set(node.labels)
            for data_key, data_val in node.data.items():
                previous_val = data.get(data_key)
                if previous_val and previous_val != data_val:
                    self.conflicts.append(Conflict(data_key, previous_val, data_val))
                else:
                    data[data_key] = data_val
        return Node(db_ns, db_id, sorted(labels), data)


class Conflict:
    def __init__(self, key, val1, val2):
        self.key = key
        self.val1 = val1
        self.val2 = val2

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Conflict({self.key}, {self.val1}, {self.val2})"
