# BST

class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left_child = None
        self.right_child = None

    def find(self, key):
        node = self
        while node is not None:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left_child
            else:
                node = node.right_child
        return None

    def insert(self, key):
        node = self
        while True:
            if key == node.key:
                return node
            elif key < node.key:
                if node.left_child is None:
                    new_node = Node(key)
                    new_node.parent = node
                    node.left_child = new_node
                    return new_node
                else:
                    node = node.left_child
            else:
                if node.right_child is None:
                    new_node = Node(key)
                    new_node.parent = node
                    node.right_child = new_node
                    return new_node
                else:
                    node = node.right_child

    def mini(self):
        current = self
        while current.left_child is not None:
            current = current.left_child
        return current

    def maxi(self):
        current = self
        while current.right_child is not None:
            current = current.right_child
        return current

    def delete(self, key):
        if key < self.key:
            if self.left_child:
                self.left_child = self.left_child.delete(key)
                if self.left_child:
                    self.left_child.parent = self
            return self
        elif key > self.key:
            if self.right_child:
                self.right_child = self.right_child.delete(key)
                if self.right_child:
                    self.right_child.parent = self
            return self
        else:
            if self.left_child is None:
                if self.right_child:
                    self.right_child.parent = self.parent
                return self.right_child
            elif self.right_child is None:
                if self.left_child:
                    self.left_child.parent = self.parent
                return self.left_child

            predecessor = self.left_child.maxi()
            self.key = predecessor.key
            self.left_child = self.left_child.delete(predecessor.key)
            if self.left_child:
                self.left_child.parent = self
            return self

    def in_order(self):
        result = []
        if self.left_child:
            result.extend(self.left_child.in_order())
        result.append(self.key)
        if self.right_child:
            result.extend(self.right_child.in_order())
        return result

    def pre_order(self):
        result = [self.key]
        if self.left_child:
            result.extend(self.left_child.pre_order())
        if self.right_child:
            result.extend(self.right_child.pre_order())
        return result

    def post_order(self):
        result = []
        if self.left_child:
            result.extend(self.left_child.post_order())
        if self.right_child:
            result.extend(self.right_child.post_order())
        result.append(self.key)
        return result

    def width_way(self):
        if not self:
            return
        queue = [self]
        level = 0

        while queue:
            print(f'{level}-ый уровень:')
            level_size = len(queue)

            for i in range(level_size):
                current = queue.pop(0)

                # Определяем положение относительно родителя
                position = "Root"
                if current.parent:
                    if current.parent.left_child == current:
                        position = "L"
                    elif current.parent.right_child == current:
                        position = "R"

                print(f' {current.key} - {position}')

                if current.left_child:
                    queue.append(current.left_child)
                if current.right_child:
                    queue.append(current.right_child)

            level += 1


    def print_tree(self, level=0, prefix="R:", is_root=True):
        #Компактный вывод дерева
        if is_root:
            print("  " * level + "Root:" + str(self.key))
        else:
            print("  " * level + prefix + str(self.key))

        if self.left_child:
            self.left_child.print_tree(level + 1, "L:", False)
        if self.right_child:
            self.right_child.print_tree(level + 1, "R:", False)

#пример
if __name__ == "__main__":
    root = Node(50)
    keys_to_insert = [30, 70, 20, 40, 60, 80, 10, 25, 35, 45]

    for key in keys_to_insert:
        root.insert(key)

    print("1. Дерево:")
    root.print_tree()

    #обходы
    print("2. Обходы")
    print("Центрированный:", root.in_order())
    print("Прямой:", root.pre_order())
    print("Обратный:", root.post_order())
    print("В ширину:")
    root.width_way()

    #поиск
    print("\n3. Поиск")
    test_keys = [40, 15]
    for key in test_keys:
        search_result = root.find(key)
        if search_result:
            print(f"Узел {key} найден")
        else:
            print(f"Узел {key} не найден")

    #мин и макс
    print("4. Минимум и максимум")

    min_node = root.mini()
    max_node = root.maxi()
    print(f"Минимум: {min_node.key}")
    print(f"Максимум: {max_node.key}")

    print("\n5. Дерево после вставки 10:")
    root.insert(10)
    root.print_tree()

    print("6. Дерево после удаления 30:")
    root.delete(30)
    root.print_tree()

