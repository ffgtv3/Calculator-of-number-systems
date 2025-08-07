#!/usr/bin/env python3
"""
Демонстрационный скрипт для TUI калькулятора
Показывает примеры использования без запуска полного TUI интерфейса
"""

def is_valid_number(number: str, base: int) -> bool:
    """Проверка корректности числа для заданной системы счисления"""
    if not number:
        return False
    valid_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:base]
    return all(char.upper() in valid_digits for char in number if char not in '.-')

def convert_number(number: str, from_base: int, to_base: int = 10) -> str:
    """Конвертация числа из одной системы счисления в другую"""
    try:
        is_negative = number.startswith('-')
        if is_negative:
            number = number[1:]

        if '.' in number:
            whole, frac = number.split('.')
            whole_decimal = int(whole, from_base)
            frac_decimal = sum(int(digit, from_base) * (from_base ** -i) 
                             for i, digit in enumerate(frac, 1))
            decimal_number = whole_decimal + frac_decimal
        else:
            decimal_number = int(number, from_base)

        if is_negative:
            decimal_number = -decimal_number

        if to_base == 10:
            return str(decimal_number)

        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        whole_number = abs(int(decimal_number))
        result = ""

        if whole_number == 0:
            result = '0'
        else:
            while whole_number > 0:
                result = digits[whole_number % to_base] + result
                whole_number //= to_base

        frac_part = abs(decimal_number) - abs(int(decimal_number))
        if frac_part > 0:
            result += '.'
            for _ in range(5):
                frac_part *= to_base
                result += digits[int(frac_part)]
                frac_part -= int(frac_part)

        if is_negative:
            result = '-' + result

        return result or '0'
    except (ValueError, OverflowError):
        return "Ошибка конвертации"

def perform_operation(num1: str, num2: str, operation: str, base: int) -> str:
    """Выполнение арифметических операций"""
    try:
        if not is_valid_number(num1, base) or not is_valid_number(num2, base):
            return "Ошибка: некорректные числа"

        decimal_num1 = float(convert_number(num1, base, 10))
        decimal_num2 = float(convert_number(num2, base, 10))

        if operation == '+':
            result = decimal_num1 + decimal_num2
        elif operation == '-':
            result = decimal_num1 - decimal_num2
        elif operation == '*':
            result = decimal_num1 * decimal_num2
        elif operation == '/':
            if decimal_num2 == 0:
                return "Ошибка: деление на ноль"
            result = decimal_num1 / decimal_num2
        elif operation == '**':
            result = decimal_num1 ** decimal_num2
        elif operation == '%':
            result = decimal_num1 % decimal_num2
        elif operation == '&':
            result = int(decimal_num1) & int(decimal_num2)
        elif operation == '|':
            result = int(decimal_num1) | int(decimal_num2)
        elif operation == '^':
            result = int(decimal_num1) ^ int(decimal_num2)
        else:
            return "Неверная операция"

        return convert_number(f"{result:.5f}", 10, base)
    except (ValueError, OverflowError):
        return "Ошибка вычисления"

def main():
    """Демонстрация возможностей калькулятора"""
    print("🔢 ДЕМОНСТРАЦИЯ TUI КАЛЬКУЛЯТОРА СИСТЕМ СЧИСЛЕНИЯ")
    print("=" * 60)
    print()
    
    # Примеры конвертации
    print("🔄 ПРИМЕРЫ КОНВЕРТАЦИИ ЧИСЕЛ:")
    print("-" * 40)
    
    examples = [
        ("FF", 16, 10, "Шестнадцатеричное в десятичное"),
        ("255", 10, 2, "Десятичное в двоичное"),
        ("1010", 2, 16, "Двоичное в шестнадцатеричное"),
        ("ABC", 16, 8, "Шестнадцатеричное в восьмеричное"),
        ("123", 10, 36, "Десятичное в 36-ричное")
    ]
    
    for number, from_base, to_base, description in examples:
        result = convert_number(number, from_base, to_base)
        print(f"{description}:")
        print(f"  {number} (основание {from_base}) → {result} (основание {to_base})")
        print()
    
    # Примеры арифметических операций
    print("🧮 ПРИМЕРЫ АРИФМЕТИЧЕСКИХ ОПЕРАЦИЙ:")
    print("-" * 40)
    
    arithmetic_examples = [
        ("1010", "1100", "+", 2, "Сложение в двоичной системе"),
        ("FF", "AA", "+", 16, "Сложение в шестнадцатеричной системе"),
        ("1010", "0011", "&", 2, "Побитовое AND в двоичной системе"),
        ("1010", "0011", "|", 2, "Побитовое OR в двоичной системе"),
        ("1010", "0011", "^", 2, "Побитовое XOR в двоичной системе")
    ]
    
    for num1, num2, op, base, description in arithmetic_examples:
        result = perform_operation(num1, num2, op, base)
        print(f"{description}:")
        print(f"  {num1} {op} {num2} (основание {base}) = {result}")
        print()
    
    print("🎯 ДЛЯ ЗАПУСКА ПОЛНОГО TUI ИНТЕРФЕЙСА ВЫПОЛНИТЕ:")
    print("   python3 tui_calculator.py")
    print()
    print("⚠️  НАПОМИНАНИЕ: Код защищен MIT лицензией!")
    print("   Не копируйте и не продавайте без разрешения!")

if __name__ == "__main__":
    main()