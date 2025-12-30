import json


def membership(x, points):
    """
    Значение функции принадлежности в точке x
    points = [[x1, y1], [x2, y2], ...]
    """
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]

        if x1 <= x <= x2:
            if x2 == x1:
                return max(y1, y2)
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    return 0.0


def main(temp_sets_json, control_sets_json, rules_json, temperature):
    temp_sets = json.loads(temp_sets_json)["температура"]
    control_sets = json.loads(control_sets_json)["температура"]
    rules = json.loads(rules_json)

    # фаззификация температуры
    temp_mu = {}
    for term in temp_sets:
        mu = membership(temperature, term["points"])
        temp_mu[term["id"]] = mu

    print("Фаззификация температуры:")
    for k, v in temp_mu.items():
        print(f"  {k}: {v:.4f}")

    # применение правил
    control_mu = {term["id"]: 0.0 for term in control_sets}

    print("\nПрименение правил:")
    for temp_term, control_term in rules:
        activation = temp_mu.get(temp_term, 0.0)
        control_mu[control_term] = max(control_mu[control_term], activation)
        print(f"  ЕСЛИ {temp_term} → {control_term}: {activation:.4f}")

    # дефаззификация (центр тяжести)
    xs = []
    mus = []

    # область определения управления
    x_min = min(p[0] for t in control_sets for p in t["points"])
    x_max = max(p[0] for t in control_sets for p in t["points"])

    step = 0.1
    x = x_min
    while x <= x_max:
        mu_x = 0.0
        for term in control_sets:
            mu_term = membership(x, term["points"])
            mu_x = max(mu_x, min(mu_term, control_mu[term["id"]]))
        xs.append(x)
        mus.append(mu_x)
        x += step

    numerator = sum(x * mu for x, mu in zip(xs, mus))
    denominator = sum(mus)

    result = numerator / denominator if denominator != 0 else 0.0

    print("\nДефаззификация:")
    print(f"  Числитель: {numerator:.4f}")
    print(f"  Знаменатель: {denominator:.4f}")
    print(f"  Управление: {result:.4f}")

    return result

temp_json = json.dumps({
    "температура": [
        {
            "id": "холодно",
            "points": [[0,1],[18,1],[22,0],[50,0]]
        },
        {
            "id": "комфортно",
            "points": [[18,0],[22,1],[24,1],[26,0]]
        },
        {
            "id": "жарко",
            "points": [[0,0],[24,0],[26,1],[50,1]]
        }
    ]
})

control_json = json.dumps({
    "температура": [
        {
            "id": "слабый",
            "points": [[0,0],[0,1],[5,1],[8,0]]
        },
        {
            "id": "умеренный",
            "points": [[5,0],[8,1],[13,1],[16,0]]
        },
        {
            "id": "интенсивный",
            "points": [[13,0],[18,1],[23,1],[26,0]]
        }
    ]
})

rules_json = json.dumps([
    ["холодно", "интенсивный"],
    ["комфортно", "умеренный"],
    ["жарко", "слабый"]
])

temperature_value = 20.0

result = main(
    temp_json,
    control_json,
    rules_json,
    temperature_value
)

print("Оптимальное управление:", result)
