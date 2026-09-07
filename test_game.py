"""
Автоматические тесты для игры «Битва героя с монстром»
Используется pytest.
"""

import pytest
from game import (
    calculate_normal_attack_damage,
    calculate_strong_attack_damage,
    calculate_heal_amount,
    calculate_monster_damage,
    is_valid_action,
    check_winner,
    determine_timeout_winner,
)


# ====================== ТЕСТЫ КОРРЕКТНОЙ РАБОТЫ ======================

def test_normal_attack_damage_range():
    """Обычная атака всегда возвращает урон от 15 до 25."""
    for _ in range(50):
        damage = calculate_normal_attack_damage()
        assert 15 <= damage <= 25


def test_strong_attack_damage_when_hit():
    """При попадании сильная атака даёт урон 30–40."""
    for _ in range(100):
        damage, missed = calculate_strong_attack_damage()
        if not missed:
            assert 30 <= damage <= 40
            return
    pytest.fail("Не удалось получить попадание за 100 попыток")


def test_strong_attack_can_miss():
    """Сильная атака иногда промахивается (урон = 0)."""
    for _ in range(100):
        damage, missed = calculate_strong_attack_damage()
        if missed:
            assert damage == 0
            return
    pytest.fail("Не удалось получить промах за 100 попыток")


def test_heal_increases_hp():
    """Лечение увеличивает HP, но не выше 100."""
    new_hp = calculate_heal_amount(50)
    assert 70 <= new_hp <= 80

    new_hp_max = calculate_heal_amount(95)
    assert new_hp_max <= 100
    assert new_hp_max >= 95


def test_heal_at_full_hp():
    """Если HP уже 100, лечение не меняет его."""
    new_hp = calculate_heal_amount(100)
    assert new_hp == 100


def test_monster_damage_without_defense():
    """Урон монстра без защиты в разумных пределах."""
    for _ in range(50):
        damage = calculate_monster_damage(defending=False)
        assert 12 <= damage <= 33


def test_monster_damage_with_defense_is_lower():
    """С защитой урон монстра в среднем меньше."""
    damages_no_def = [calculate_monster_damage(False) for _ in range(30)]
    damages_def = [calculate_monster_damage(True) for _ in range(30)]
    assert sum(damages_def) / len(damages_def) < sum(damages_no_def) / len(damages_no_def)


def test_check_winner_hero():
    """Герой побеждает, когда HP монстра <= 0."""
    assert check_winner(50, 0) == "hero"
    assert check_winner(10, -5) == "hero"


def test_check_winner_monster():
    """Монстр побеждает, когда HP героя <= 0."""
    assert check_winner(0, 50) == "monster"
    assert check_winner(-3, 20) == "monster"


def test_check_winner_continue():
    """Бой продолжается, пока оба живы."""
    assert check_winner(50, 50) is None
    assert check_winner(1, 1) is None


def test_timeout_winner():
    """Правильное определение победителя по окончании 10 ходов."""
    assert determine_timeout_winner(80, 40) == "hero"
    assert determine_timeout_winner(30, 90) == "monster"
    assert determine_timeout_winner(50, 50) == "draw"


# ====================== ТЕСТЫ НЕКОРРЕКТНЫХ ДАННЫХ ======================

def test_is_valid_action_correct():
    """Корректные действия 1–4 принимаются."""
    assert is_valid_action("1") is True
    assert is_valid_action("2") is True
    assert is_valid_action("3") is True
    assert is_valid_action("4") is True
    assert is_valid_action(" 3 ") is True


def test_is_valid_action_incorrect():
    """Некорректный ввод отклоняется."""
    assert is_valid_action("0") is False
    assert is_valid_action("5") is False
    assert is_valid_action("10") is False
    assert is_valid_action("") is False
    assert is_valid_action("abc") is False
    assert is_valid_action("1.5") is False
    assert is_valid_action("-1") is False


def test_heal_with_negative_hp():
    """Лечение отрицательного HP всё равно даёт корректный результат."""
    new_hp = calculate_heal_amount(-10)
    assert 10 <= new_hp <= 20