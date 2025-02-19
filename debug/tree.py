import pptree
from lib.game import GameMoveNode


def build_tree_dfs(node: GameMoveNode) -> pptree.Node:
    pptree_node = pptree.Node(str(node))
    for child in node.children.values():
        pptree_node.children.append(build_tree_dfs(child))
    return pptree_node


def pretty_print_tree(node: GameMoveNode) -> None:
    printable_tree = build_tree_dfs(node)
    pptree.print_tree(printable_tree, childattr="children")
