import csv
import os

def read_tree_from_csv(filename):
    edges = []
    nodes = set()
    root_id = None
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)
    
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)  # Используем csv.reader вместо DictReader
            
            for row_num, row in enumerate(reader, 1):
                if not row:  # Пропускаем пустые строки
                    continue
                    
                print(f"Строка {row_num}: {row}")  # Отладочный вывод
                
                # Парсим данные по позициям: [node_id, parent_id, root_id]
                node_id = int(row[0]) if row[0] else None
                parent_id = int(row[1]) if len(row) > 1 and row[1] else None
                root_id_val = int(row[2]) if len(row) > 2 and row[2] else None
                
                if node_id is None:
                    continue
                    
                if root_id is None and root_id_val is not None:
                    root_id = root_id_val
                
                nodes.add(node_id)
                if parent_id is not None:
                    edges.append((parent_id, node_id))
                    nodes.add(parent_id)
                        
        if not nodes:
            print("Файл пуст или не содержит корректных данных")
            return [], [], {}, None, 0
            
        node_list = sorted(nodes)
        node_to_idx = {node: idx for idx, node in enumerate(node_list)}
        n = len(node_list)
        
        return edges, node_list, node_to_idx, root_id, n
        
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return [], [], {}, None, 0

def create_matrix(n, default_value=0):
    """Создает матрицу n x n"""
    return [[default_value for _ in range(n)] for _ in range(n)]

def dfs_reachability(node, current, adj_list, reachability, node_to_idx):
    """Рекурсивный поиск всех достижимых узлов из текущего"""
    for neighbor in adj_list.get(current, []):
        if not reachability[node_to_idx[node]][node_to_idx[neighbor]]:
            reachability[node_to_idx[node]][node_to_idx[neighbor]] = 1
            dfs_reachability(node, neighbor, adj_list, reachability, node_to_idx)

def build_matrices(edges, node_to_idx, n):
    # 1. Матрица смежности (только прямые связи)
    adj_matrix = create_matrix(n, 0)
    
    # 2-5. Матрицы инцидентности
    R1 = create_matrix(n, 0)  # управления (прямого)
    R2 = create_matrix(n, 0)  # подчинения (транспонированная R1)
    R3 = create_matrix(n, 0)  # опосредованного управления
    R4 = create_matrix(n, 0)  # опосредованного подчинения
    R5 = create_matrix(n, 0)  # соподчинения
    
    # Создаем список смежности для дерева
    adj_list = {}
    for parent, child in edges:
        if parent not in adj_list:
            adj_list[parent] = []
        adj_list[parent].append(child)
    
    # Заполнение матриц смежности и прямых отношений
    for parent, child in edges:
        i, j = node_to_idx[parent], node_to_idx[child]
        adj_matrix[i][j] = 1  # Только прямое направление в дереве
        R1[i][j] = 1  # прямое управление
        R2[j][i] = 1  # прямое подчинение
    
    # Вычисление матрицы достижимости (опосредованные отношения) с помощью DFS
    reachability = create_matrix(n, 0)
    idx_to_node = {idx: node for node, idx in node_to_idx.items()}
    
    for node_idx in range(n):
        node = idx_to_node[node_idx]
        dfs_reachability(node, node, adj_list, reachability, node_to_idx)
    
    # Заполнение матриц опосредованных отношений
    for i in range(n):
        for j in range(n):
            if i != j and reachability[i][j]:
                R3[i][j] = 1  # опосредованное управление
                R4[j][i] = 1  # опосредованное подчинение
    
    # Заполнение матрицы соподчинения
    for i in range(n):
        children = []
        for j in range(n):
            if R1[i][j] == 1:
                children.append(j)
        
        # Все дети одного родителя соподчинены друг другу
        for idx1 in range(len(children)):
            for idx2 in range(len(children)):
                if idx1 != idx2:
                    R5[children[idx1]][children[idx2]] = 1
    
    return adj_matrix, R1, R2, R3, R4, R5

def print_matrix(matrix, node_list, title):
    """Красиво выводит матрицу"""
    print(f"\n{title}:")
    # Заголовок с номерами столбцов
    header = "    " + "  ".join(f"{node:2}" for node in node_list)
    print(header)
    print("   " + "-" * (len(header) - 3))
    
    for i, row in enumerate(matrix):
        print(f"{node_list[i]:2} |" + "  ".join(f"{val:2}" for val in row))

def main():
    filename = "input.csv"
    
    try:
        edges, node_list, node_to_idx, root_id, n = read_tree_from_csv(filename)
        
        if not node_list:
            print("Не удалось прочитать данные из файла")
            return
        
        print(f"\nУзлы дерева: {node_list}")
        print(f"Корень дерева: {root_id}")
        print(f"Рёбра дерева: {edges}")
        
        A, R1, R2, R3, R4, R5 = build_matrices(edges, node_to_idx, n)
        
        print_matrix(A, node_list, "1. Матрица смежности")
        print_matrix(R1, node_list, "2. Матрица прямого управления (R1)")
        print_matrix(R2, node_list, "3. Матрица прямого подчинения (R2 - транспонированная R1)")
        print_matrix(R3, node_list, "4. Матрица опосредованного управления (R3)")
        print_matrix(R4, node_list, "5. Матрица опосредованного подчинения (R4 - транспонированная R3)")
        print_matrix(R5, node_list, "6. Матрица соподчинения (R5)")
        
        result_tuple = (A, R1, R2, R3, R4, R5)
        return result_tuple
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()