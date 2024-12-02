from collections import deque
import random


class node:
    def __init__(self, key, data, color='red'):
        self.key = key
        self.data = data
        self.color = color
        self.left_child = None
        self.right_child = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.LISTNULL = node(0, None, color='black')
        self.root = self.LISTNULL

    def insert(self, key, data):
        new_node = node(key, data)
        walking_node = self.root
        if self.root == self.LISTNULL:
            self.root = new_node
            new_node.parent = None
            new_node.left_child = self.LISTNULL
            new_node.right_child = self.LISTNULL
            new_node.color = 'black'
            return
        while walking_node != self.LISTNULL:
            if key > walking_node.key:
                if walking_node.right_child != self.LISTNULL:
                    walking_node = walking_node.right_child
                else:
                    new_node.parent = walking_node
                    walking_node.right_child = new_node
                    new_node.left_child = self.LISTNULL
                    new_node.right_child = self.LISTNULL
                    break
            elif key < walking_node.key:
                if walking_node.left_child != self.LISTNULL:
                    walking_node = walking_node.left_child
                else:
                    new_node.parent = walking_node
                    walking_node.left_child = new_node
                    new_node.left_child = self.LISTNULL
                    new_node.right_child = self.LISTNULL
                    break
        new_node.color = 'red'
        self.balance_insert(new_node)

    def balance_insert(self, node):
        while node != self.root and node.parent.color == 'red':
            if node.parent == node.parent.parent.left_child:
                uncle = node.parent.parent.right_child
                if uncle is not None and uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.right_child:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left_child
                if uncle is not None and uncle.color == 'red':
                    node.parent.color = 'black'
                    uncle.color = 'black'
                    node.parent.parent.color = 'red'
                    node = node.parent.parent
                else:
                    if node == node.parent.left_child:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = 'black'
                    node.parent.parent.color = 'red'
                    self.left_rotate(node.parent.parent)
        self.root.color = 'black'

    def left_rotate(self, node):
        node2 = node.right_child
        node.right_child = node2.left_child
        if node2.left_child != self.LISTNULL:
            node2.left_child.parent = node
        node2.parent = node.parent
        if node.parent is None:
            self.root = node2
        elif node == node.parent.left_child:
            node.parent.left_child = node2
        else:
            node.parent.right_child = node2
        node2.left_child = node
        node.parent = node2

    def right_rotate(self, node):
        node2 = node.left_child
        node.left_child = node2.right_child
        if node2.right_child != self.LISTNULL:
            node2.right_child.parent = node
        node2.parent = node.parent
        if node.parent is None:
            self.root = node2
        elif node == node.parent.right_child:
            node.parent.right_child = node2
        else:
            node.parent.left_child = node2
        node2.right_child = node
        node.parent = node2

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
        original_color = walking_node.color
        if walking_node.left_child is None and walking_node.right_child is None:
            if walking_node.parent is not None:
                if walking_node.parent.left_child == walking_node:
                    walking_node.parent.left_child = None
                else:
                    walking_node.parent.right_child = None
            else:
                self.root = None
        elif walking_node.left_child is None or walking_node.right_child is None:
            child = walking_node.left_child if walking_node.left_child else walking_node.right_child
            if walking_node.parent is not None:
                if walking_node.parent.left_child == walking_node:
                    walking_node.parent.left_child = child
                else:
                    walking_node.parent.right_child = child
            else:
                self.root = child
            if child is not None:
                child.parent = walking_node.parent
        else:
            replace_node = walking_node.right_child
            while replace_node.left_child is not None:
                replace_node = replace_node.left_child
            walking_node.key = replace_node.key
            original_color = replace_node.color
            if replace_node.parent.left_child == replace_node:
                replace_node.parent.left_child = replace_node.right_child
            else:
                replace_node.parent.right_child = replace_node.right_child

            if replace_node.right_child is not None:
                replace_node.right_child.parent = replace_node.parent
            walking_node = replace_node
        if original_color == 'black':
            self.balance_delete(walking_node)

    def balance_delete(self, node):
        while node != self.root and node.color == 'black':
            if node == node.parent.left_child:
                brother = node.parent.right_child
                if brother.color == 'red':
                    brother.color = 'black'
                    node.parent.color = 'red'
                    self.left_rotate(node.parent)
                    brother = node.parent.right_child
                if brother.left_child.color == 'black' and brother.right_child.color == 'black':
                    brother.color = 'red'
                    node = node.parent
                else:
                    if brother.right_child.color == 'black':
                        brother.left_child.color = 'black'
                        brother.color = 'red'
                        self.right_rotate(brother)
                        brother = node.parent.right_child
                    brother.color = node.parent.color
                    node.parent.color = 'black'
                    brother.right_child.color = 'black'
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                brother = node.parent.left_child
                if brother.color == 'red':
                    brother.color = 'black'
                    node.parent.color = 'red'
                    self.right_rotate(node.parent)
                    brother = node.parent.left_child
                if brother.right_child.color == 'black' and brother.left_child.color == 'black':
                    brother.color = 'red'
                    node = node.parent
                else:
                    if brother.left_child.color == 'black':  # Случай 3
                        brother.right_child.color = 'black'
                        brother.color = 'red'
                        self.left_rotate(brother)
                        brother = node.parent.left_child
                    brother.color = node.parent.color
                    node.parent.color = 'black'
                    brother.left_child.color = 'black'
                    self.right_rotate(node.parent)
                    node = self.root
        node.color = 'black'

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

    def height(self):
        if not self.root:
            return 0

        queue = deque([(self.root, 1)])  # Начинаем с корня и уровня 1
        max_height = 0

        while queue:
            node, level = queue.popleft()
            max_height = max(max_height, level)

            # Проверяем, что дочерние узлы не равны self.LISTNULL
            if node.left_child is not self.LISTNULL:
                queue.append((node.left_child, level + 1))
            if node.right_child is not self.LISTNULL:
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


RBT = RedBlackTree()
RBT.insert_monotonically_increasing_keys(1000, 1)
RBT.breadth_first_search()
print(RBT.height())