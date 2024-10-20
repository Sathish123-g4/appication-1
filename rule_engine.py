import ast
import json
from typing import List

def create_rule(rule_string):
    """Creates an AST from a rule string."""
    ast_nodes = [create_rule(rule) for rule in rules]  # Added comma
    return build_ast(ast_node.body[0])

def build_ast(ast_node):
    """Recursively builds the AST."""
    if isinstance(ast_node, ast.Name):
        return Node("operand", value=ast_node.id)
    elif isinstance(ast_node, ast.Constant):
        return Node("operand", value=ast_node.value)
    elif isinstance(ast_node, ast.Compare):
        operator = ast_node.ops[0].__class__.__name__.lower()
        left = build_ast(ast_node.left)
        right = build_ast(ast_node.comparators[0])
        return Node("operator", value=operator, left=left, right=right)
    elif isinstance(ast_node, ast.BoolOp):
        operator = ast_node.op.__class__.__name__.lower()
        left = build_ast(ast_node.values[0])
        right = build_ast(ast_node.values[1])
        return Node("operator", value=operator, left=left, right=right)
    else:
        raise ValueError("Unsupported AST node type: {}".format(ast_node.__class__.__name__))

def combine_rules(rules):
    """Combines multiple rules into a single AST."""
    ast_nodes = [create_rule(rule) for rule in rules]
    return combine_ast(ast_nodes)

def combine_ast(ast_nodes):
    """Recursively combines AST nodes."""
    if len(ast_nodes) == 1:
        return ast_nodes[0]
    else:
        return Node("operator", value="and", left=combine_ast(ast_nodes[:len(ast_nodes) // 2]), right=combine_ast(ast_nodes[len(ast_nodes) // 2:]))

def evaluate_rule(ast_node, data):
    """Evaluates an AST against given data."""
    if ast_node.type == "operand":
        return data.get(ast_node.value)
    elif ast_node.type == "operator":
        left_value = evaluate_rule(ast_node.left, data)
        right_value = evaluate_rule(ast_node.right, data)
        if ast_node.value == "and":
            return left_value and right_value
        elif ast_node.value == "or":
            return left_value or right_value
        elif ast_node.value == "eq":
            return left_value == right_value
        elif ast_node.value == "ne":
            return left_value != right_value
        elif ast_node.value == "lt":
            return left_value < right_value
        elif ast_node.value == "le":
            return left_value <= right_value
        elif ast_node.value == "gt":
            return left_value > right_value
        elif ast_node.value == "ge":
            return left_value >= right_value
        else:
            raise ValueError("Unsupported operator: {}".format(ast_node.value))

class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right