#!/usr/bin/env python3
"""
Простая текстовая RPG-битва: Герой vs Монстр
Максимум 10 ходов. Подходит для тестирования.
"""

import random
import time


# ====================== ЧИСТЫЕ ФУНКЦИИ (легко тестировать) ======================

def calculate_normal_attack_damage() -> int:
    """Обычная атака: урон от 15 до 25."""
    return random.randint(15, 25)


def calculate_strong_attack_damage() -> tuple[int, bool]:
    """
    Сильная атака: урон 30-40, шанс промаха 30%.
    Возвращает (урон, был_ли_промах).
    """
    if random.random() < 0.3:
        return 0, True   # промах
    damage = random.randint(30, 40)
    return damage, False


def calculate_heal_amount(current_hp: int, max_hp: int = 100) -> int:
    """Лечение: +20-30 HP, но не больше max_hp. Возвращает новое HP."""
    heal = random.randint(20, 30)
    return min(max_hp, current_hp + heal)


def calculate_monster_damage(defending: bool) -> int:
    """
    Урон монстра: 12-22.
    Если defending=True — урон уменьшается в 2 раза.
    С шансом 20% — огненное дыхание (x1.5).
    """
    damage = random.randint(12, 22)
    if defending:
        damage //= 2
    if random.random() < 0.2:
        damage = int(damage * 1.5)
    return damage


def is_valid_action(choice: str) -> bool:
    """Проверяет, является ли ввод корректным действием (1-4)."""
    return choice.strip() in ("1", "2", "3", "4")


def check_winner(hero_hp: int, monster_hp: int) -> str | None:
    """
    Проверяет состояние боя.
    Возвращает: 'hero', 'monster' или None (бой продолжается).
    """
    if monster_hp <= 0:
        return "hero"
    if hero_hp <= 0:
        return "monster"
    return None


def determine_timeout_winner(hero_hp: int, monster_hp: int) -> str:
    """Определяет победителя по очкам здоровья после 10 ходов."""
    if hero_hp > monster_hp:
        return "hero"
    if monster_hp > hero_hp:
        return "monster"
    return "draw"


# ====================== ФУНКЦИИ С ВВОДОМ/ВЫВОДОМ ======================

def print_status(hero_hp: int, monster_hp: int, turn: int) -> None:
    print("\n" + "=" * 40)
    print(f"  Ход: {turn}/10")
    print(f"  Герой HP: {hero_hp:>3}  ❤")
    print(f"  Монстр HP: {monster_hp:>3}  ☠")
    print("=" * 40)


def get_player_action() -> int:
    print("\nВыбери действие:")
    print("  1. Атака      (урон 15-25)")
    print("  2. Сильная атака (урон 30-40, шанс промаха 30%)")
    print("  3. Лечение    (+20-30 HP)")
    print("  4. Защита     (урон монстра уменьшен в 2 раза)")
    while True:
        choice = input("Твой выбор (1-4): ").strip()
        if is_valid_action(choice):
            return int(choice)
        print("Введи число от 1 до 4!")


def main() -> None:
    print("=" * 45)
    print("     БИТВА ГЕРОЯ С МОНСТРОМ")
    print("     Максимум 10 ходов")
    print("=" * 45)
    print("Ты — герой. Перед тобой злой монстр!")
    print("Победи его за 10 ходов или умри пытаясь.\n")
    input("Нажми Enter, чтобы начать бой...")

    hero_hp = 100
    monster_hp = 120

    for turn in range(1, 11):
        print_status(hero_hp, monster_hp, turn)

        action = get_player_action()
        defending = False

        if action == 1:  # Обычная атака
            damage = calculate_normal_attack_damage()
            monster_hp -= damage
            print(f"\n⚔ Ты нанёс {damage} урона монстру!")

        elif action == 2:  # Сильная атака
            damage, missed = calculate_strong_attack_damage()
            if missed:
                print("\n💨 Промах! Сильная атака не попала.")
            else:
                monster_hp -= damage
                print(f"\n💥 Критический удар! Ты нанёс {damage} урона!")

        elif action == 3:  # Лечение
            new_hp = calculate_heal_amount(hero_hp)
            heal = new_hp - hero_hp
            hero_hp = new_hp
            print(f"\n💚 Ты восстановил {heal} HP. Теперь у тебя {hero_hp} HP.")

        elif action == 4:  # Защита
            defending = True
            print("\n🛡 Ты встал в защитную стойку!")

        # Проверка победы после хода игрока
        winner = check_winner(hero_hp, monster_hp)
        if winner == "hero":
            print("\n" + "=" * 45)
            print("🎉 ПОБЕДА! Ты победил монстра!")
            print(f"Бой закончился на {turn} ходу.")
            print("=" * 45)
            break

        # Ход монстра
        time.sleep(0.7)
        print("\nМонстр атакует...")
        time.sleep(0.5)

        monster_damage = calculate_monster_damage(defending)
        if defending:
            print("🛡 Защита сработала! Урон уменьшен.")
        if monster_damage > 22:
            print("🔥 Монстр использовал огненное дыхание!")

        hero_hp -= monster_damage
        print(f"☠ Монстр нанёс тебе {monster_damage} урона!")

        winner = check_winner(hero_hp, monster_hp)
        if winner == "monster":
            print("\n" + "=" * 45)
            print("💀 ПОРАЖЕНИЕ... Монстр победил.")
            print(f"Бой закончился на {turn} ходу.")
            print("=" * 45)
            break
    else:
        print("\n" + "=" * 45)
        print("⏰ Время вышло! 10 ходов закончились.")
        result = determine_timeout_winner(hero_hp, monster_hp)
        if result == "hero":
            print("🏆 По очкам здоровья побеждает ГЕРОЙ!")
        elif result == "monster":
            print("🏆 По очкам здоровья побеждает МОНСТР!")
        else:
            print("🤝 Ничья по здоровью!")
        print("=" * 45)

    print("\nСпасибо за игру! Это тестовая программа.")
    print("Можно запускать много раз для проверки разных сценариев.")


if __name__ == "__main__":
    main()