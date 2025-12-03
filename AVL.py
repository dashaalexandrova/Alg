from BST import Node  # Импортируем ваш существующий класс

class AVLNode(Node):
    def __init__(self, key):
        super().__init__(key)
        self.height = 1  # Высота узла

    #дополнительные
    def recalc_height(self):
        #Пересчитать высоту текущего узла
        left_height = self.left_child.height if self.left_child else 0
        right_height = self.right_child.height if self.right_child else 0
        self.height = max(left_height, right_height) + 1

    def koef_balance(self):
        #Получить коэффициент баланса узла
        left_height = self.left_child.height if self.left_child else 0
        right_height = self.right_child.height if self.right_child else 0
        return left_height - right_height

    def rotate_right(self):
        #Правый поворот (малый)
        new_root = self.left_child
        temp = new_root.right_child

        # Выполняем поворот
        new_root.right_child = self
        new_root.parent = self.parent

        self.left_child = temp
        self.parent = new_root

        if temp:
            temp.parent = self

        # Пересчитываем высоты
        self.recalc_height()
        new_root.recalc_height()

        return new_root

    def rotate_left(self):
        #Левый поворот (малый)
        new_root = self.right_child
        temp = new_root.left_child

        # Выполняем поворот
        new_root.left_child = self
        new_root.parent = self.parent

        self.right_child = temp
        self.parent = new_root

        if temp:
            temp.parent = self

        # Пересчитываем высоты
        self.recalc_height()
        new_root.recalc_height()

        return new_root

    def rebalance(self):
        #Выполнить балансировку узла
        self.recalc_height()
        balance = self.koef_balance()

        # Случай 1: Левое поддерево слишком высокое
        if balance > 1:
            if self.left_child.koef_balance() >= 0:
                # одинарный правый поворот
                return self.rotate_right()
            else:
                # двойной лево-правый поворот
                self.left_child = self.left_child.rotate_left()
                if self.left_child:
                    self.left_child.parent = self
                return self.rotate_right()

        # Случай 2: Правое поддерево слишком высокое
        if balance < -1:
            if self.right_child.koef_balance() <= 0:
                # одинарный левый поворот
                return self.rotate_left()
            else:
                # двойной право-левый поворот
                self.right_child = self.right_child.rotate_right()
                if self.right_child:
                    self.right_child.parent = self
                return self.rotate_left()

        return self

    # ОСНОВНЫЕ ОПЕРАЦИИ
    def insert(self, key):
        #Вставить элемент с балансировкой
        if key < self.key:
            if self.left_child is None:
                new_node = AVLNode(key)
                new_node.parent = self
                self.left_child = new_node
            else:
                self.left_child = self.left_child.insert(key)
                if self.left_child:
                    self.left_child.parent = self
        elif key > self.key:
            if self.right_child is None:
                new_node = AVLNode(key)
                new_node.parent = self
                self.right_child = new_node
            else:
                self.right_child = self.right_child.insert(key)
                if self.right_child:
                    self.right_child.parent = self

        # Балансировка после вставки
        return self.rebalance()

    def delete(self, key):
        #Удалить элемент с балансировкой
        if key < self.key:
            if self.left_child:
                self.left_child = self.left_child.delete(key)
                if self.left_child:
                    self.left_child.parent = self
        elif key > self.key:
            if self.right_child:
                self.right_child = self.right_child.delete(key)
                if self.right_child:
                    self.right_child.parent = self
        else:
            # Узел найден, удаляем его
            if self.left_child is None:
                temp = self.right_child
                if temp:
                    temp.parent = self.parent
                return temp
            elif self.right_child is None:
                temp = self.left_child
                if temp:
                    temp.parent = self.parent
                return temp
            else:
                # Узел имеет двух детей
                successor = self.right_child.mini()
                self.key = successor.key
                self.right_child = self.right_child.delete(successor.key)
                if self.right_child:
                    self.right_child.parent = self
        # Балансировка после удаления
        return self.rebalance()


    def print_avl(self, level=0, prefix="R:", is_root=True):
        #Вывести дерево с информацией о высоте и балансе
        if is_root:
            print("  " * level + f"ROOT:{self.key}[h={self.height},b={self.koef_balance()}]")
        else:
            print("  " * level + f"{prefix}{self.key}[h={self.height},b={self.koef_balance()}]")

        if self.left_child:
            self.left_child.print_avl(level + 1, "L:", False)
        if self.right_child:
            self.right_child.print_avl(level + 1, "R:", False)



# Демонстрация работы
if __name__ == "__main__":

    # вставка
    tree = AVLNode(50)
    keys_to_insert = [30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    for key in keys_to_insert:
        tree.insert(key)

    print("1. Дерево:")
    tree.print_avl()

    print("\n2. Обходы:")
    print(f"Центрированный обход: {tree.in_order()}")
    print(f"Прямой обход: {tree.pre_order()}")
    print(f"Обратный обход: {tree.post_order()}")
    print("В ширину:")
    tree.width_way()
    # поиск
    print("\n3. Поиск")
    test_keys = [40, 15]
    for key in test_keys:
        search_result = tree.find(key)
        if search_result:
            print(f"Узел {key} найден")
        else:
            print(f"Узел {key} не найден")

    # Минимум и максимум
    print("4. Минимум и максимум")
    print(f"Минимум: {tree.mini().key}")
    print(f"Максимум: {tree.maxi().key}")

    # Вставка с балансировкой
    print("\n5. Дерево после вставки 10:")
    tree = tree.insert(10)
    tree.print_avl()

    # Удаление
    print("6. Дерево после удаления 30:")
    tree = tree.delete(30)
    tree.print_avl()


