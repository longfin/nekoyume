from enum import Enum

class BehaviorTreeBuilder:
    def __init__(self):
        self.node = None
        self.parents = []
    
    def do(self, name, fn):
        try:
            if len(self.parents) == 0:
                raise Exception
        except Exception:
            print("Can't create an unnested ActionNode, it must be a leaf node")
        self.parents[-1].add_child(ActionNode(name, fn))
        return self
    
    def condition(self, name, fn):
        return self.do(name, lambda b: BehaviorTreeStatus.SUCCESS if fn(b) else BehaviorTreeStatus.FAILURE)

    def sequence(self, name):
        node = SequenceNode(name)
        if len(self.parents) > 0:
            self.parents[-1].add_child(node)
        self.parents.append(node)
        return self

    def selector(self, name):
        node = SelectorNode(name)
        if len(self.parents) > 0:
            self.parents[-1].add_child(node)
        self.parents.append(node)
        return self
    
    def end(self):
        self.node = self.parents.pop()
        return self

    def build(self):
        try:
            if not self.node:
                raise Exception
        except Exception:
            print('Zero node')
        return self.node


class BehaviorTreeStatus(Enum):
    SUCCESS = 1,
    FAILURE = 2,
    RUNNING = 3,


class Node:
    def __init__(self, name):
        self.name = name


class ActionNode(Node):
    def __init__(self, name, fn):
        super().__init__(name)
        self.fn = fn

    def tick(self, data):
        return self.fn(data)


class SequenceNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def tick(self, data):
        for child in self.children:
            status = child.tick(data)
            if status != BehaviorTreeStatus.SUCCESS:
                return status
        return BehaviorTreeStatus.SUCCESS

class SelectorNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def tick(self, data):
        for child in self.children:
            status = child.tick(data)
            if status != BehaviorTreeStatus.FAILURE:
                return status
        return BehaviorTreeStatus.FAILURE

