# Константы
MAP_SIZE = 10
WALL = '#'
EMPTY = '.'
PLAYER = 'P'
ENEMY = 'E'
ITEM = 'I'

# Функции для работы с персонажами
def create_character(name, hp, mp, arm, dmg):
    return {
        'name': name,
        'hp': hp,
        'mp': mp,
        'arm': arm,
        'dmg': dmg
    }

def is_alive(character):
    return character['hp'] > 0

def attack(attacker, defender):
    damage = calculate_damage(attacker, defender)
    defender['hp'] -= damage
    print(f"{attacker['name']} нанес {damage} урона {defender['name']}. У {defender['name']} осталось {defender['hp']} HP.")

# Функция для рендеринга карты
def render_map(player_pos, enemy_pos, items):
    for y in range(MAP_SIZE + 2):  # +2 для границ
        for x in range(MAP_SIZE + 2):  # +2 для границ
            if x == 0 or x == MAP_SIZE + 1 or y == 0 or y == MAP_SIZE + 1:
                print(WALL, end=' ')  # Границы
            else:
                if (x - 1, y - 1) == player_pos:
                    print(PLAYER, end=' ')
                elif (x - 1, y - 1) == enemy_pos:
                    print(ENEMY, end=' ')
                elif (x - 1, y - 1) in items:
                    print(ITEM, end=' ')
                else:
                    print(EMPTY, end=' ')
        print()

# Функция для обработки движения
def move_player(player_pos, direction, enemy_pos):
    x, y = player_pos
    if direction == 'w' and y > 0:  # вверх
        y -= 1
    elif direction == 's' and y < MAP_SIZE - 1:  # вниз
        y += 1
    elif direction == 'a' and x > 0:  # влево
        x -= 1
    elif direction == 'd' and x < MAP_SIZE - 1:  # вправо
        x += 1

    # Проверка на столкновение с врагом
    if (x, y) == enemy_pos:
        return player_pos, True  # Возвращаем старую позицию и флаг столкновения
    return (x, y), False

# Функция для расчета урона
def calculate_damage(attacker, defender):
    damage = attacker['dmg'] - defender['arm']
    return max(damage, 0)

# Основная игра
def main():
    player = create_character("Player", 100, 50, 5, 10)
    enemy = create_character("Enemy", 50, 0, 2, 8)
    player_pos = (1, 1)
    enemy_pos = (8, 8)
    items = {(3, 3): "Health Potion", (5, 5): "Mana Potion"}
    inventory = []

    while is_alive(player) and is_alive(enemy):
        render_map(player_pos, enemy_pos, items)
        action = input("Введите действие (w/a/s/d для движения, 'e' для атаки, 'pick' для подбора предмета, 'q' для выхода): ")

        if action in ['w', 'a', 's', 'd']:
            new_pos, collision = move_player(player_pos, action, enemy_pos)
            if not collision:
                player_pos = new_pos
            else:
                print("Вы не можете пройти через врага!")
        elif action == 'e':  # Атака
            # Проверка, находится ли игрок рядом с врагом
            if (abs(player_pos[0] - enemy_pos[0]) <= 1 and abs(player_pos[1] - enemy_pos[1]) <= 1):
                attack(player, enemy)
                if is_alive(enemy):
                    attack(enemy, player)
            else:
                print("Враг слишком далеко!")
        elif action == 'pick':
            if player_pos in items:
                item = items.pop(player_pos)
                inventory.append(item)
                print(f"Вы подобрали {item}.")
            else:
                print("Здесь нет предметов.")
        elif action == 'q':  # Выход из игры
            print("Вы вышли из игры.")
            break
        else:
            print("Неверная команда. Пожалуйста, попробуйте снова.")

            # Проверка на атаку врага
        if is_alive(enemy) and player_pos == enemy_pos:
            attack(enemy, player)

    if is_alive(player):
        print("Вы победили врага!")
    else:
        print("Вы погибли...")

if __name__ == "__main__":
    main()
