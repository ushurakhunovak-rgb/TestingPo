#!/usr/bin/env python3
"""
Простая текстовая RPG-битва: Герой vs Монстр
Максимум 10 ходов. Идеально для тестирования.
"""

import random
import time

def print_status(hero_hp, monster_hp, turn):
    print("\n" + "=" * 40)
    print(f"  Ход: {turn}/10")
    print(f"  Герой HP: {hero_hp:>3}  ❤")
    print(f"  Монстр HP: {monster_hp:>3}  ☠")
    print("=" * 40)

def get_player_action():
    print("\nВыбери действие:")
    print("  1. Атака      (урон 15-25)")
    print("  2. Сильная атака (урон 30-40, шанс промаха 30%)")
    print("  3. Лечение    (+20-30 HP)")
    print("  4. Защита     (урон монстра уменьшен в 2 раза)")
    while True:
        choice = input("Твой выбор (1-4): ").strip()
        if choice in ("1", "2", "3", "4"):
            return int(choice)
        print("Введи число от 1 до 4!")

def main():
    print("=" * 45)
    print("     БИТВА ГЕРОЯ С МОНСТРОМ")
    print("     Максимум 10 ходов")
    print("=" * 45)
    print("Ты — герой. Перед тобой злой монстр!")
    print("Победи его за 10 ходов или умри пытаясь.\n")
    input("Нажми Enter, чтобы начать бой...")

    hero_hp = 100
    monster_hp = 120
    defending = False

    for turn in range(1, 11):
        print_status(hero_hp, monster_hp, turn)

        action = get_player_action()
        defending = False

        if action == 1:
            damage = random.randint(15, 25)
            monster_hp -= damage
            print(f"\n⚔ Ты нанёс {damage} урона монстру!")
        elif action == 2:
            if random.random() < 0.3:
                print("\n💨 Промах! Сильная атака не попала.")
            else:
                damage = random.randint(30, 40)
                monster_hp -= damage
                print(f"\n💥 Критический удар! Ты нанёс {damage} урона!")
        elif action == 3:
            heal = random.randint(20, 30)
            hero_hp = min(100, hero_hp + heal)
            print(f"\n💚 Ты восстановил {heal} HP. Теперь у тебя {hero_hp} HP.")
        elif action == 4:
            defending = True
            print("\n🛡 Ты встал в защитную стойку!")

        if monster_hp <= 0:
            print("\n" + "=" * 45)
            print("🎉 ПОБЕДА! Ты победил монстра!")
            print(f"Бой закончился на {turn} ходу.")
            print("=" * 45)
            break

        time.sleep(0.7)
        print("\nМонстр атакует...")
        time.sleep(0.5)

        monster_damage = random.randint(12, 22)
        if defending:
            monster_damage //= 2
            print(f"🛡 Защита сработала! Урон уменьшен.")
        
        if random.random() < 0.2:
            monster_damage = int(monster_damage * 1.5)
            print("🔥 Монстр использовал огненное дыхание!")

        hero_hp -= monster_damage
        print(f"☠ Монстр нанёс тебе {monster_damage} урона!")

        if hero_hp <= 0:
            print("\n" + "=" * 45)
            print("💀 ПОРАЖЕНИЕ... Монстр победил.")
            print(f"Бой закончился на {turn} ходу.")
            print("=" * 45)
            break
    else:
        print("\n" + "=" * 45)
        print("⏰ Время вышло! 10 ходов закончились.")
        if hero_hp > monster_hp:
            print("🏆 По очкам здоровья побеждает ГЕРОЙ!")
        elif monster_hp > hero_hp:
            print("🏆 По очкам здоровья побеждает МОНСТР!")
        else:
            print("🤝 Ничья по здоровью!")
        print("=" * 45)

    print("\nСпасибо за игру! Это тестовая программа.")
    print("Можно запускать много раз для проверки разных сценариев.")

if __name__ == "__main__":
    main()