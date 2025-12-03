from BST import Node
import random
import matplotlib.pyplot as plt
import math


def build_bst(keys):
    """Построение BST из списка ключей"""
    if not keys:
        return None

    # Создаем корень
    root = Node(keys[0])

    # Вставляем остальные ключи
    for key in keys[1:]:
        root.insert(key)

    return root



def node_height(self):
    """Вычисляет высоту дерева"""
    left_height = self.left_child.height() if self.left_child else -1
    right_height = self.right_child.height() if self.right_child else -1
    return 1 + max(left_height, right_height)

Node.height = node_height

# Параметры
min_n = 100
max_n = 10000
step = 50
num_trials = 10

n_values = list(range(min_n, max_n + 1, step))
all_heights = []  # Список всех высот для всех экспериментов

for n in n_values:
    total_height = 0
    print(f"Обработка {n} ключей.")
    for _ in range(num_trials):
        keys = random.sample(range(1, 1000000), n)
        root = build_bst(keys)
        total_height += root.height()
    all_heights.append(total_height / num_trials)

# Отображаем результаты
plt.figure(figsize=(12, 8))
plt.plot(n_values, all_heights, 'b-', label='Эксперимент', linewidth=2)

plt.plot(n_values, [1.44 * math.log2(n) for n in n_values], 'r-', label='1.44 log₂(n)')

plt.xlabel('Количество ключей (n)')
plt.ylabel('Высота дерева')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()