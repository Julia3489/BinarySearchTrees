from collections import deque
import random

class node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left_child = None
        self.right_child = None
        self.parent = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        new_node = node(key, data)
        walking_node = self.root
        if self.root is None:
            self.root = new_node
            new_node.parent = None
            return
        while (walking_node != None):
            if key > walking_node.key:
                if walking_node.right_child != None:
                    walking_node = walking_node.right_child
                else:
                    new_node.parent = walking_node
                    walking_node.right_child = new_node
                    break
            elif key < walking_node.key:
                if walking_node.left_child != None:
                    walking_node = walking_node.left_child
                else:
                    new_node.parent = walking_node
                    walking_node.left_child = new_node
                    break


    def search(self, key):
        walking_node = self.root
        while (walking_node != None):
            if key == walking_node.key:
                return walking_node.data
            elif key > walking_node.key:
                walking_node = walking_node.right_child
            elif key < walking_node.key:
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
        if walking_node.left_child is None and walking_node.right_child is None: #случай, когда у удаляемого листа нет потомков
            if walking_node.parent is not None:
                if walking_node.parent.left_child == walking_node:
                    walking_node.parent.left_child = None
                else:
                    walking_node.parent.right_child = None
            else:
                self.root = None
        elif walking_node.left_child is None or walking_node.right_child is None: #случай, когда у удаляемого листа есть один потомок
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
        else: #случай, когда у удаляемого узла есть оба потомка
            replace_node = walking_node.right_child
            while replace_node.left_child is not None:
                replace_node = replace_node.left_child
            walking_node.key = replace_node.key
            if replace_node.parent.left_child == replace_node:
                replace_node.parent.left_child = replace_node.right_child
            else:
                replace_node.parent.right_child = replace_node.right_child

            if replace_node.right_child is not None:
                replace_node.right_child.parent = replace_node.parent


    def preorderTraversal(self, node): #прямой обход в глубину (вершина, левое поддерево, правое поддерево)
        if node != None:
            print(node.key)
            self.preorderTraversal(node.left_child)
            self.preorderTraversal(node.right_child)

    def inorderTraversal(self, node): #симметричный обход в глубину (в отсортированном порядке)
        if node != None:
            self.inorderTraversal(node.left_child)
            print(node.key)
            self.inorderTraversal(node.right_child)

    def postorderTraversal(self, node): #обратный обход в глубину (левое поддерево, правое поддерево, вершина)
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


test_tree = BST()
test_tree.insert(60, "data")
test_tree.insert(50, "data")
test_tree.insert(70, "data")
test_tree.insert(40, "data")
test_tree.insert(55, "data")
test_tree.insert(80, "data")
test_tree.insert(53, "data")
test_tree.insert(58, "data")
test_tree.insert(75, "data")
test_tree.postorderTraversal(test_tree.root)



























