class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def get_last(self):
        if self.tail:
            return self.tail.data
        return None

    def get_all(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

class TreeNode:
    def __init__(self, text, is_question=True, topic=None):
        self.text = text
        self.is_question = is_question
        self.left = None
        self.right = None
        self.topic = topic

class DiscussionTree:
    def __init__(self):
        self.root = None

    def set_root(self, node):
        self.root = node

    def search_topic(self, node, topic):
        if node is None:
            return False
        
        if node.topic and topic.lower() in node.topic.lower():
            return True
        
        return self.search_topic(node.left, topic) or self.search_topic(node.right, topic)
