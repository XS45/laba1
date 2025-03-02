# Характеристики
class Character:
    def __init__(self, name, hp, mp, armor, damage):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.armor = armor
        self.damage = damage

    def attack(self, target):
        # Новый расчет урона
        damage = int(self.damage * (1 - target.armor / (target.armor + 100)))
        damage = max(damage, 1)  # Убедимся, что урон не меньше 1
        target.hp -= damage
        print(f"{self.name} наносит {damage} урона {target.name}.")
        print(f"{target.name} осталось здоровья: {target.hp}")

    def is_alive(self):
        return self.hp > 0

# Карта
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [['#'] * (width + 2)]
        for _ in range(height):
            self.grid.append(['#'] + ['.'] * width + ['#'])
        self.grid.append(['#'] * (width + 2))

    def is_walkable(self, x, y, enemies):
        if 0 < x < self.width + 1 and 0 < y < self.height + 1 and self.grid[y][x] != '#':
            for enemy in enemies:
                if enemy.position == (x, y) and enemy.is_alive():
                    return False
            return True
        return False

    def render(self, player, enemies):
        for y in range(self.height + 2):
            for x in range(self.width + 2):
                if (x, y) == player.position:
                    print('P', end=' ')
                elif any(enemy.position == (x, y) for enemy in enemies if enemy.is_alive()):
                    print('A', end=' ')
                else:
                    print(self.grid[y][x], end=' ')
            print()

# Игрок
class Player(Character):
    def __init__(self, name, hp, mp, armor, damage):
        super().__init__(name, hp, mp, armor, damage)
        self.position = (3, 3)
        self.inventory = []

    def move(self, dx, dy, game_map, enemies):
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        if game_map.is_walkable(new_x, new_y, enemies):
            self.position = (new_x, new_y)
        else:
            print("Вы не можете пройти в этом направлении.")

    def pick_up(self, item):
        self.inventory.append(item)
        print(f"{self.name} подобрал {item}.")

# Враг
class Enemy(Character):
    def __init__(self, name, hp, mp, armor, damage, position):
        super().__init__(name, hp, mp, armor, damage)
        self.position = position

    def move(self, game_map, player):
        dx = 0
        dy = 0
        if player.position[0] < self.position[0]:
            dx = -1
        elif player.position[0] > self.position[0]:
            dx = 1
        if player.position[1] < self.position[1]:
            dy = -1
        elif player.position[1] > self.position[1]:
            dy = 1

        new_x = self.position[0] + dx
        new_y = self.position[1] + dy

        if game_map.is_walkable(new_x, new_y, []):
            self.position = (new_x, new_y)

# Игровой цикл
def game_loop(player, enemies, game_map):
    while True:
        game_map.render(player, enemies)
        print(f"HP: {player.hp} | MP: {player.mp} | Инвентарь: {', '.join(player.inventory)}")
        print("Управление: W (вверх), A (влево), S (вниз), D (вправо), Q (выход)")

        target = None
        for enemy in enemies:
            if enemy.position == player.position and enemy.is_alive():
                target = enemy
                break

        # Проверка на возможность атаки
        attack_available = False
        for enemy in enemies:
            if enemy.is_alive() and abs(player.position[0] - enemy.position[0]) <= 1 and abs(player.position[1] - enemy.position[1]) <= 1:
                attack_available = True
                break

        if attack_available:
            print("E (атака)")

        move = input("Введите команду: ").strip().lower()

        if move == 'w':
            player.move(0, -1, game_map, enemies)
        elif move == 's':
            player.move(0, 1, game_map, enemies)
        elif move == 'a':
            player.move(-1, 0, game_map, enemies)
        elif move == 'd':
            player.move(1, 0, game_map, enemies)
        elif move == 'q':
            break
        elif move == 'e' and target:
            player.attack(target)
            if not target.is_alive():
                enemies.remove(target)  # Удаляем врага из списка
                print(f"{target.name} повержен!")

        # Проверка на урон от врагов
        for enemy in enemies:
            if enemy.position == player.position and enemy.is_alive():
                enemy.attack(player)
                if not player.is_alive():
                    print("Вы проиграли!")
                    return

        if not player.is_alive():
            print("Вы проиграли!")
            return

# Главная функция
def main():
    game_map = Map(10, 10)  # Создаем карту размером 10x10
    player = Player("Игрок", 100, 50, 5, 20)  # Создаем игрока с характеристиками
    enemies = [
        Enemy("Враг 1", 30, 20, 3, 5, (2, 2)),  # Создаем первого врага
        Enemy("Враг 2", 50, 20, 3, 5, (7, 7))   # Создаем второго врага
    ]

    game_loop(player, enemies, game_map)  # Запускаем игровой цикл

if __name__ == "__main__":
    main()  # Запускаем главную функцию, если скрипт выполняется напрямую



