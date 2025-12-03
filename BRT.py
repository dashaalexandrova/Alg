from BST import Node

class RBNode(Node):
    RED = 'RED'
    BLACK = 'BLACK'

    def __init__(self, key):
        super().__init__(key)
        self.color = RBNode.RED  # Новые узлы всегда красные

    def black_height(self):
        """Вычисление черной высоты дерева"""
        if self is None:
            return 1  # NIL-узлы считаются черными

        left_height = 0
        right_height = 0

        if self.left_child:
            left_height = self.left_child.black_height()
        else:
            left_height = 1  # NIL-лист черный

        if self.right_child:
            right_height = self.right_child.black_height()
        else:
            right_height = 1  # NIL-лист черный

        if left_height != right_height:
            #print("ВНИМАНИЕ: ОШИБКА БАЛАНСИРОВКИ - черные высоты не равны!")
            return max(left_height, right_height)

        return left_height + (1 if self.color == RBNode.BLACK else 0)

    def get_root(self):
        """Возвращает корень дерева"""
        current = self
        while current.parent is not None:
            current = current.parent
        return current

    def insert(self, key):
        """Вставка нового значения с балансировкой красно-черного дерева"""
        if key < self.key:
            if self.left_child is None:
                self.left_child = RBNode(key)
                self.left_child.parent = self
                self.left_child.balance_after_insert()
                # Находим и возвращаем корень
                root = self
                while root.parent is not None:
                    root = root.parent
                return root
            else:
                return self.left_child.insert(key)
        elif key > self.key:
            if self.right_child is None:
                self.right_child = RBNode(key)
                self.right_child.parent = self
                self.right_child.balance_after_insert()
                # Находим и возвращаем корень
                root = self
                while root.parent is not None:
                    root = root.parent
                return root
            else:
                return self.right_child.insert(key)
        else:
            # Ключ уже существует
            return None

    def balance_after_insert(self):
        """Балансировка после вставки"""
        node = self

        while node.parent is not None and node.parent.color == RBNode.RED:
            parent = node.parent
            grandparent = parent.parent

            if grandparent is None:
                break

            if parent == grandparent.left_child:
                uncle = grandparent.right_child
                if uncle is not None and uncle.color == RBNode.RED:
                    # Случай 1: Дядя красный
                    parent.color = RBNode.BLACK
                    uncle.color = RBNode.BLACK
                    grandparent.color = RBNode.RED
                    node = grandparent  # Переходим к дедушке
                else:
                    # Случай 2: Дядя черный
                    if node == parent.right_child:
                        # Случай 2a: Треугольник
                        node = parent
                        node.left_rotate()
                        # После поворота обновляем parent
                        parent = node.parent
                        grandparent = parent.parent if parent else None

                    # Случай 2b/3: Линия
                    parent.color = RBNode.BLACK
                    if grandparent:
                        grandparent.color = RBNode.RED
                        grandparent.right_rotate()
            else:
                uncle = grandparent.left_child
                if uncle is not None and uncle.color == RBNode.RED:
                    # Случай 1: Дядя красный
                    parent.color = RBNode.BLACK
                    uncle.color = RBNode.BLACK
                    grandparent.color = RBNode.RED
                    node = grandparent
                else:
                    # Случай 2: Дядя черный
                    if node == parent.left_child:
                        # Случай 2a: Треугольник
                        node = parent
                        node.right_rotate()
                        # После поворота обновляем parent
                        parent = node.parent
                        grandparent = parent.parent if parent else None

                    # Случай 2b/3: Линия
                    parent.color = RBNode.BLACK
                    if grandparent:
                        grandparent.color = RBNode.RED
                        grandparent.left_rotate()

        # Обеспечиваем, что корень всегда черный
        root = node
        while root.parent is not None:
            root = root.parent
        root.color = RBNode.BLACK

    def left_rotate(self):
        """Левый поворот"""
        node = self
        pivot = node.right_child

        if pivot is None:
            return

        pivot.parent = node.parent
        if node.parent is not None:
            if node == node.parent.left_child:
                node.parent.left_child = pivot
            else:
                node.parent.right_child = pivot

        node.right_child = pivot.left_child
        if pivot.left_child is not None:
            pivot.left_child.parent = node

        pivot.left_child = node
        node.parent = pivot

    def right_rotate(self):
        """Правый поворот"""
        node = self
        pivot = node.left_child

        if pivot is None:
            return

        pivot.parent = node.parent
        if node.parent is not None:
            if node == node.parent.left_child:
                node.parent.left_child = pivot
            else:
                node.parent.right_child = pivot

        node.left_child = pivot.right_child
        if pivot.right_child is not None:
            pivot.right_child.parent = node

        pivot.right_child = node
        node.parent = pivot

    def delete(self, key):
        """Удаление значения с балансировкой красно-черного дерева"""
        node_to_delete = self.find(key)
        if node_to_delete is None:
            root = self
            while root.parent is not None:
                root = root.parent
            return root

        root = self
        while root.parent is not None:
            root = root.parent

        if node_to_delete.left_child is not None and node_to_delete.right_child is not None:
            successor = node_to_delete.right_child
            while successor.left_child is not None:
                successor = successor.left_child
            node_to_delete.key = successor.key
            node_to_delete = successor

        child = node_to_delete.left_child if node_to_delete.left_child is not None else node_to_delete.right_child

        if node_to_delete.parent is None:
            if child is not None:
                child.parent = None
            return child
        else:
            if node_to_delete == node_to_delete.parent.left_child:
                node_to_delete.parent.left_child = child
            else:
                node_to_delete.parent.right_child = child

            if child is not None:
                child.parent = node_to_delete.parent

        if node_to_delete.color == RBNode.BLACK:
            if child is not None and child.color == RBNode.RED:
                child.color = RBNode.BLACK
            elif child is not None:
                child.balance_after_delete()

        return root

    def balance_after_delete(self):
        """Балансировка после удаления"""
        node = self

        while node != self and node.color == RBNode.BLACK:
            parent = node.parent

            if node == parent.left_child:
                brother = parent.right_child

                if brother.color == RBNode.RED:
                    brother.color = RBNode.BLACK
                    parent.color = RBNode.RED
                    parent.left_rotate()
                    brother = parent.right_child

                if (brother.left_child is None or brother.left_child.color == RBNode.BLACK) and \
                        (brother.right_child is None or brother.right_child.color == RBNode.BLACK):
                    brother.color = RBNode.RED
                    node = parent
                else:
                    if brother.right_child is None or brother.right_child.color == RBNode.BLACK:
                        if brother.left_child is not None:
                            brother.left_child.color = RBNode.BLACK
                        brother.color = RBNode.RED
                        brother.right_rotate()
                        brother = parent.right_child

                    brother.color = parent.color
                    parent.color = RBNode.BLACK
                    if brother.right_child is not None:
                        brother.right_child.color = RBNode.BLACK
                    parent.left_rotate()
                    node = self
            else:
                brother = parent.left_child

                if brother.color == RBNode.RED:
                    brother.color = RBNode.BLACK
                    parent.color = RBNode.RED
                    parent.right_rotate()
                    brother = parent.left_child

                if (brother.left_child is None or brother.left_child.color == RBNode.BLACK) and \
                        (brother.right_child is None or brother.right_child.color == RBNode.BLACK):
                    brother.color = RBNode.RED
                    node = parent
                else:
                    if brother.left_child is None or brother.left_child.color == RBNode.BLACK:
                        if brother.right_child is not None:
                            brother.right_child.color = RBNode.BLACK
                        brother.color = RBNode.RED
                        brother.left_rotate()
                        brother = parent.left_child

                    brother.color = parent.color
                    parent.color = RBNode.BLACK
                    if brother.left_child is not None:
                        brother.left_child.color = RBNode.BLACK
                    parent.right_rotate()
                    node = self

        node.color = RBNode.BLACK

    def print_tree(self, level=0, prefix="R:", is_root=True):
        """Вывод дерева с цветами и черной высотой"""
        if self is None:
            return

        color_symbol = "B" if self.color == RBNode.BLACK else "R"

        # Вычисляем черную высоту для текущего узла
        node_black_height = self.black_height()

        if is_root:
            print("  " * level + f"ROOT:{self.key}({color_symbol}) bh={node_black_height}")
        else:
            print("  " * level + prefix + f"{self.key}({color_symbol}) bh={node_black_height}")

        if self.left_child:
            self.left_child.print_tree(level + 1, "L:", False)
        if self.right_child:
            self.right_child.print_tree(level + 1, "R:", False)

if __name__ == "__main__":

    # 1. Создание
    root = RBNode(50)
    root.color = RBNode.BLACK

    keys_to_insert = [30, 70, 20, 40, 60, 80, 100, 25, 350]
    # Вставка
    for key in keys_to_insert:
        result = root.insert(key)
        if result:
            root = result

    # дерево
    bh = root.black_height()
    print("1. Красно-черное дерево", f"(черная высота дерева: {bh}):")
    root.print_tree()

    # обходы
    print("\n2. Обходы:")
    print("Центрированный:", root.in_order())
    print("Прямой:", root.pre_order())
    print("Обратный:", root.post_order())
    print("В ширину:")
    root.width_way()

    print("\n3. Поиск:")
    search_keys = [40, 15]
    for key in search_keys:
        node = root.find(key)
        if node:
            color = "B" if node.color == RBNode.BLACK else "R"
            print(f"Узел {key} найден ({color})")
        else:
            print(f"Узел {key} не найден")

    print("\n4. Минимум и максимум :")
    min_node = root.mini()
    max_node = root.maxi()
    print(f"Минимум: {min_node.key}")
    print(f"Максимум: {max_node.key}")

    # Вставка с балансировкой
    print("\n5. Дерево после вставки 10:")
    root = root.insert(10)
    root.print_tree()
    print("\n6. Дерево после удаления 30")
    root = root.delete(30)
    if root:
        root.print_tree()


