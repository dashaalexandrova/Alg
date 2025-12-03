import random
import math
import matplotlib.pyplot as plt
from AVL import AVLNode
from BRT import RBNode

def get_tree_height(node):
    if node is None:
        return 0
    return 1 + max(get_tree_height(node.left_child), get_tree_height(node.right_child))

# Параметры
min_keys = 25
max_keys = 10000
step = 100
num_trials = 20

key_counts = list(range(min_keys, max_keys + 1, step))
avl_heights = []
avl_upper_bound = []
avl_lower_bound = []

brt_heights = []
brt_upper_bound = []
brt_lower_bound = []

for n in key_counts:
    print(n)

    avl_height_sum = 0
    brt_height_sum = 0  # Сумма высот для BRT

    for _ in range(num_trials):

        keys = random.sample(range(1, 1000000), n)

        # Создание AVL дерева
        avl_root = AVLNode(keys[0])
        for key in keys[1:]:
            avl_root = avl_root.insert(key)
        avl_height_sum += get_tree_height(avl_root)

        brt_root = RBNode(keys[0])
        for key in keys[1:]:
            brt_root.insert(key)
            brt_root = brt_root.get_root()
        brt_height_sum += get_tree_height(brt_root)



    avl_heights.append(avl_height_sum / num_trials)
    brt_heights.append(brt_height_sum / num_trials)

    # Теоретические оценки для AVL дерева
    avl_upper_bound.append(1.44 * math.log2(n + 1))
    avl_lower_bound.append(math.log2(n + 1))

    # Теоретические оценки для красно-черного дерева
    brt_upper_bound.append(2 * math.log2(n + 1))
    brt_lower_bound.append(math.log2(n + 1))
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)

plt.plot(key_counts, avl_upper_bound, 'r-',  linewidth=1.5)
plt.plot(key_counts, avl_lower_bound, 'g-', linewidth=1.5)
plt.plot(key_counts, avl_heights, 'b-', linewidth=1.5)

plt.xlabel('Кол-во ключей(n)')
plt.ylabel('Высота дерева')
plt.title('Зависимость высоты AVL-дерева от количества ключей')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)

plt.plot(key_counts, brt_upper_bound, 'r-', label='Теоретическая верхняя оценка', linewidth=1.5)
plt.plot(key_counts, brt_lower_bound, 'g-', label='Теоретическая нижняя оценка', linewidth=1.5)
plt.plot(key_counts, brt_heights, 'b-', label='Экспериментальная высота', linewidth=1.5)
plt.xlabel('Кол-во ключей(n)')
plt.ylabel('Высота дерева')
plt.title('Зависимость высоты красно-черного дерева от количества ключей')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()