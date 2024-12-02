from collections import deque
import random


class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.height = 1
        self.left_child = None
        self.right_child = None
        self.parent = None

    def height_node(self):
        if self:
            return self.height
        else:
            return 0

    def balance_factor(self):
        if self.left_child:
            left_height = self.left_child.height_node()
        else:
            left_height = 0
        if self.right_child:
            right_height = self.right_child.height_node()
        else:
            right_height = 0
        return right_height - left_height

    def fix_height(self):
        if self.left_child:
            left_height = self.left_child.height_node()
        else:
            left_height = 0
        if self.right_child:
            right_height = self.right_child.height_node()
        else:
            right_height = 0
        self.height = max(left_height, right_height) + 1


class AVLTree:
    def __init__(self):
        self.root = None

    def balance(self, node):
        node.fix_height()
        balance = node.balance_factor()

        if balance > 1:
            if node.right_child.balance_factor() >= 0:
                return self.left_rotate(node)
            else:
                node.right_child = self.right_rotate(node.right_child)
                return self.left_rotate(node)
        elif balance < -1:
            if node.left_child.balance_factor() <= 0:
                return self.right_rotate(node)
            else:
                node.left_child = self.left_rotate(node.left_child)
                return self.right_rotate(node)
        return node

    def left_rotate(self, node1):
        node2 = node1.right_child
        node1.right_child = node2.left_child
        if node2.left_child:
            node2.left_child.parent = node1
        node2.parent = node1.parent
        if node1.parent:
            if node1 == node1.parent.left_child:
                node1.parent.left_child = node2
            else:
                node1.parent.right_child = node2
        else:
            self.root = node2
        node2.left_child = node1
        node1.parent = node2
        node1.fix_height()
        node2.fix_height()
        return node2

    def right_rotate(self, node1):
        node2 = node1.left_child
        node1.left_child = node2.right_child
        if node2.right_child:
            node2.right_child.parent = node1
        node2.parent = node1.parent
        if node1.parent:
            if node1 == node1.parent.right_child:
                node1.parent.right_child = node2
            else:
                node1.parent.left_child = node2
        else:
            self.root = node2
        node2.right_child = node1
        node1.parent = node2
        node1.fix_height()
        node2.fix_height()
        return node2

    def insert(self, key, data):
        new_node = Node(key, data)
        if self.root is None:
            self.root = new_node
            return
        walking_node = self.root
        while True:
            if key > walking_node.key:
                if walking_node.right_child is None:
                    walking_node.right_child = new_node
                    new_node.parent = walking_node
                    break
                walking_node = walking_node.right_child
            else:
                if walking_node.left_child is None:
                    walking_node.left_child = new_node
                    new_node.parent = walking_node
                    break
                walking_node = walking_node.left_child
        current_node = new_node.parent
        while current_node is not None:
            current_node = self.balance(current_node)
            current_node = current_node.parent if current_node.parent else None

    def search(self, key):
        walking_node = self.root
        while walking_node is not None:
            if key == walking_node.key:
                return walking_node.data
            elif key > walking_node.key:
                walking_node = walking_node.right_child
            else:
                walking_node = walking_node.left_child
        return "Данные не найдены"

    def delete(self, key):
        walking_node = self.root
        while walking_node is not None:
            if key < walking_node.key:
                walking_node = walking_node.left_child
            elif key > walking_node.key:
                walking_node = walking_node.right_child
            else:
                break
        if walking_node is None:
            print("Узел для удаления не найден")
            return
        if walking_node.left_child is None and walking_node.right_child is None:
            if walking_node.parent:
                if walking_node.parent.left_child == walking_node:
                    walking_node.parent.left_child = None
                else:
                    walking_node.parent.right_child = None
            else:
                self.root = None
        elif walking_node.left_child is None or walking_node.right_child is None:
            child = walking_node.left_child if walking_node.left_child else walking_node.right_child
            if walking_node.parent:
                if walking_node.parent.left_child == walking_node:
                    walking_node.parent.left_child = child
                else:
                    walking_node.parent.right_child = child
            else:
                self.root = child
            if child:
                child.parent = walking_node.parent
        else:
            replace_node = walking_node.right_child
            while replace_node.left_child is not None:
                replace_node = replace_node.left_child
            walking_node.key = replace_node.key
            if replace_node.parent.left_child == replace_node:
                replace_node.parent.left_child = replace_node.right_child
            else:
                replace_node.parent.right_child = replace_node.right_child
            if replace_node.right_child:
                replace_node.right_child.parent = replace_node.parent

        current_node = walking_node.parent if walking_node.parent else self.root
        while current_node is not None:
            current_node = self.balance(current_node)
            current_node = current_node.parent if current_node.parent else None

    def preorderTraversal(self, node):  # прямой обход в глубину (вершина, левое поддерево, правое поддерево)
        if node != None:
            print(node.key)
            self.preorderTraversal(node.left_child)
            self.preorderTraversal(node.right_child)

    def inorderTraversal(self, node):  # симметричный обход в глубину (в отсортированном порядке)
        if node != None:
            self.inorderTraversal(node.left_child)
            print(node.key)
            self.inorderTraversal(node.right_child)

    def postorderTraversal(self, node):  # обратный обход в глубину (левое поддерево, правое поддерево, вершина)
        if node != None:
            self.postorderTraversal(node.left_child)
            self.postorderTraversal(node.right_child)
            print(node.key)

    def breadth_first_search(self):
        if self.root is None:
            print("Дерево пустое")
            return
        queue = deque([self.root])
        current_level_count = 1
        next_level_count = 0
        result = []
        while queue:
            level_nodes = []
            for _ in range(current_level_count):
                current_node = queue.popleft()
                level_nodes.append(current_node.key)
                if current_node.left_child is not None:
                    queue.append(current_node.left_child)
                    next_level_count += 1
                if current_node.right_child is not None:
                    queue.append(current_node.right_child)
                    next_level_count += 1
            result.append(level_nodes)
            current_level_count = next_level_count
            next_level_count = 0
        for level in result:
            print(" ".join(str(key) for key in level))

    def heightAVL(self):
        if not self.root:
            return 0
        queue = deque([(self.root, 1)])
        max_height = 0
        while queue:
            node, level = queue.popleft()
            max_height = max(max_height, level)
            if node.left_child is not None:
                queue.append((node.left_child, level + 1))
            if node.right_child is not None:
                queue.append((node.right_child, level + 1))
        return max_height

    def insert_uniform_random_keys(self, count, min_value, max_value):
        if count > (max_value - min_value):
            print("Количество запрашиваемых ключей больше диапазона уникальных значений.")
            return

        uniform_keys = random.sample(range(min_value, max_value), count)
        for key in uniform_keys:
            self.insert(key, f"Data for {key}")

    def insert_monotonically_increasing_keys(self, count, start_value):
        for i in range(count):
            key = start_value + i
            self.insert(key, f"Data for {key}")


avl_tree = AVLTree()
avl_tree.insert_monotonically_increasing_keys(10, 1)
avl_tree.breadth_first_search()
print(avl_tree.heightAVL())


