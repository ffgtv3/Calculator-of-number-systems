#!/usr/bin/env python3
"""
MIT License

Copyright (c) 2024 Calculator TUI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

DISCLAIMER: This code is protected by MIT License. You are NOT allowed to:
- Copy this code without proper attribution
- Sell this code or any derivative works
- Use this code for commercial purposes without permission
- Remove or modify the license notice

For any questions regarding usage, please contact the original author.
"""

import curses
import sys
import os
from typing import Optional, Tuple

class Colors:
    """Цветовые константы для TUI"""
    WHITE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4
    BLUE = 5
    MAGENTA = 6
    CYAN = 7

class TUICalculator:
    """TUI калькулятор с поддержкой различных систем счисления"""
    
    def __init__(self):
        self.screen = None
        self.current_menu = "main"
        self.input_buffer = ""
        self.cursor_pos = 0
        self.menu_items = {
            "main": ["Перевод чисел", "Арифметические операции", "О программе", "Выход"],
            "conversion": ["Назад"],
            "arithmetic": ["Назад"]
        }
        self.selected_item = 0
        self.result = ""
        self.error_message = ""
        
    def init_colors(self):
        """Инициализация цветов"""
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(Colors.WHITE, curses.COLOR_WHITE, -1)
        curses.init_pair(Colors.RED, curses.COLOR_RED, -1)
        curses.init_pair(Colors.GREEN, curses.COLOR_GREEN, -1)
        curses.init_pair(Colors.YELLOW, curses.COLOR_YELLOW, -1)
        curses.init_pair(Colors.BLUE, curses.COLOR_BLUE, -1)
        curses.init_pair(Colors.MAGENTA, curses.COLOR_MAGENTA, -1)
        curses.init_pair(Colors.CYAN, curses.COLOR_CYAN, -1)

    def show_disclaimer(self):
        """Показ дисклеймера MIT лицензии"""
        disclaimer_text = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║                        MIT LICENSE                           ║",
            "╠══════════════════════════════════════════════════════════════╣",
            "║                                                              ║",
            "║  Copyright (c) 2024 Calculator TUI                          ║",
            "║                                                              ║",
            "║  Permission is hereby granted, free of charge, to any       ║",
            "║  person obtaining a copy of this software and associated    ║",
            "║  documentation files (the \"Software\"), to deal in the       ║",
            "║  Software without restriction, including without limitation ║",
            "║  the rights to use, copy, modify, merge, publish,          ║",
            "║  distribute, sublicense, and/or sell copies of the Software.║",
            "║                                                              ║",
            "║  ⚠️  ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ:                                ║",
            "║     • НЕ копируйте этот код без указания авторства         ║",
            "║     • НЕ продавайте этот код или производные работы        ║",
            "║     • НЕ используйте код в коммерческих целях без разрешения║",
            "║     • НЕ удаляйте или изменяйте уведомление о лицензии      ║",
            "║                                                              ║",
            "║  Нажмите любую клавишу для продолжения...                   ║",
            "╚══════════════════════════════════════════════════════════════╝"
        ]
        
        height, width = self.screen.getmaxyx()
        start_y = max(0, (height - len(disclaimer_text)) // 2)
        
        for i, line in enumerate(disclaimer_text):
            y = start_y + i
            if y < height:
                x = max(0, (width - len(line)) // 2)
                if x + len(line) <= width:
                    self.screen.addstr(y, x, line, curses.color_pair(Colors.CYAN))
        
        self.screen.refresh()
        self.screen.getch()

    def is_valid_number(self, number: str, base: int) -> bool:
        """Проверка корректности числа для заданной системы счисления"""
        if not number:
            return False
        valid_digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:base]
        return all(char.upper() in valid_digits for char in number if char not in '.-')

    def convert_number(self, number: str, from_base: int, to_base: int = 10) -> str:
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

    def perform_operation(self, num1: str, num2: str, operation: str, base: int) -> str:
        """Выполнение арифметических операций"""
        try:
            if not self.is_valid_number(num1, base) or not self.is_valid_number(num2, base):
                return "Ошибка: некорректные числа"

            decimal_num1 = float(self.convert_number(num1, base, 10))
            decimal_num2 = float(self.convert_number(num2, base, 10))

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

            return self.convert_number(f"{result:.5f}", 10, base)
        except (ValueError, OverflowError):
            return "Ошибка вычисления"

    def draw_menu(self):
        """Отрисовка меню"""
        height, width = self.screen.getmaxyx()
        
        # Заголовок
        title = "🔢 КАЛЬКУЛЯТОР СИСТЕМ СЧИСЛЕНИЯ 🔢"
        title_x = max(0, (width - len(title)) // 2)
        self.screen.addstr(1, title_x, title, curses.color_pair(Colors.YELLOW) | curses.A_BOLD)
        
        # Меню
        menu_items = self.menu_items[self.current_menu]
        menu_start_y = 4
        
        for i, item in enumerate(menu_items):
            y = menu_start_y + i
            if y < height - 2:
                if i == self.selected_item:
                    self.screen.addstr(y, 2, f"▶ {item}", 
                                     curses.color_pair(Colors.GREEN) | curses.A_BOLD)
                else:
                    self.screen.addstr(y, 2, f"  {item}", curses.color_pair(Colors.WHITE))

    def draw_conversion_form(self):
        """Отрисовка формы конвертации"""
        height, width = self.screen.getmaxyx()
        
        # Заголовок
        title = "🔄 ПЕРЕВОД ЧИСЕЛ"
        title_x = max(0, (width - len(title)) // 2)
        self.screen.addstr(1, title_x, title, curses.color_pair(Colors.CYAN) | curses.A_BOLD)
        
        # Поля ввода
        self.screen.addstr(3, 2, "Число для перевода:", curses.color_pair(Colors.WHITE))
        self.screen.addstr(4, 2, "─" * 30, curses.color_pair(Colors.BLUE))
        
        self.screen.addstr(6, 2, "Из системы счисления (2-36):", curses.color_pair(Colors.WHITE))
        self.screen.addstr(7, 2, "─" * 30, curses.color_pair(Colors.BLUE))
        
        self.screen.addstr(9, 2, "В систему счисления (2-36):", curses.color_pair(Colors.WHITE))
        self.screen.addstr(10, 2, "─" * 30, curses.color_pair(Colors.BLUE))
        
        # Результат
        if self.result:
            self.screen.addstr(12, 2, f"Результат: {self.result}", 
                             curses.color_pair(Colors.GREEN))
        
        if self.error_message:
            self.screen.addstr(14, 2, f"Ошибка: {self.error_message}", 
                             curses.color_pair(Colors.RED))

    def draw_arithmetic_form(self):
        """Отрисовка формы арифметических операций"""
        height, width = self.screen.getmaxyx()
        
        # Заголовок
        title = "🧮 АРИФМЕТИЧЕСКИЕ ОПЕРАЦИИ"
        title_x = max(0, (width - len(title)) // 2)
        self.screen.addstr(1, title_x, title, curses.color_pair(Colors.MAGENTA) | curses.A_BOLD)
        
        # Поля ввода
        self.screen.addstr(3, 2, "Первое число:", curses.color_pair(Colors.WHITE))
        self.screen.addstr(4, 2, "─" * 30, curses.color_pair(Colors.BLUE))
        
        self.screen.addstr(6, 2, "Второе число:", curses.color_pair(Colors.WHITE))
        self.screen.addstr(7, 2, "─" * 30, curses.color_pair(Colors.BLUE))
        
        self.screen.addstr(9, 2, "Операция (+, -, *, /, **, %, &, |, ^):", curses.color_pair(Colors.WHITE))
        self.screen.addstr(10, 2, "─" * 30, curses.color_pair(Colors.BLUE))
        
        self.screen.addstr(12, 2, "Система счисления (2-36):", curses.color_pair(Colors.WHITE))
        self.screen.addstr(13, 2, "─" * 30, curses.color_pair(Colors.BLUE))
        
        # Результат
        if self.result:
            self.screen.addstr(15, 2, f"Результат: {self.result}", 
                             curses.color_pair(Colors.GREEN))
        
        if self.error_message:
            self.screen.addstr(17, 2, f"Ошибка: {self.error_message}", 
                             curses.color_pair(Colors.RED))

    def draw_about(self):
        """Отрисовка информации о программе"""
        height, width = self.screen.getmaxyx()
        
        about_text = [
            "📋 О ПРОГРАММЕ",
            "",
            "🔢 Калькулятор систем счисления с TUI интерфейсом",
            "",
            "✨ Возможности:",
            "   • Перевод чисел между системами счисления (2-36)",
            "   • Арифметические операции в любой системе счисления",
            "   • Поддержка дробных чисел",
            "   • Побитовые операции",
            "",
            "⚖️  Лицензия: MIT",
            "📝 Автор: Calculator TUI",
            "",
            "⚠️  ВАЖНО: Код защищен MIT лицензией!",
            "   Не копируйте и не продавайте без разрешения!",
            "",
            "Нажмите любую клавишу для возврата..."
        ]
        
        for i, line in enumerate(about_text):
            y = 2 + i
            if y < height - 2:
                x = max(0, (width - len(line)) // 2)
                if x + len(line) <= width:
                    color = Colors.YELLOW if "⚠️" in line else Colors.WHITE
                    self.screen.addstr(y, x, line, curses.color_pair(color))

    def get_input(self, prompt: str, y_pos: int) -> str:
        """Получение ввода от пользователя"""
        height, width = self.screen.getmaxyx()
        
        # Очистка строки
        self.screen.addstr(y_pos, 2, " " * (width - 4))
        self.screen.addstr(y_pos, 2, prompt, curses.color_pair(Colors.WHITE))
        
        curses.echo()
        curses.curs_set(1)
        
        try:
            user_input = self.screen.getstr(y_pos, len(prompt) + 3).decode('utf-8')
        except (UnicodeDecodeError, KeyboardInterrupt):
            user_input = ""
        
        curses.noecho()
        curses.curs_set(0)
        
        return user_input

    def handle_conversion(self):
        """Обработка конвертации чисел"""
        self.result = ""
        self.error_message = ""
        
        number = self.get_input("Число:", 4)
        if not number:
            return
        
        from_base_str = self.get_input("Из системы:", 7)
        if not from_base_str:
            return
        
        to_base_str = self.get_input("В систему:", 10)
        if not to_base_str:
            return
        
        try:
            from_base = int(from_base_str)
            to_base = int(to_base_str)
            
            if not (2 <= from_base <= 36) or not (2 <= to_base <= 36):
                self.error_message = "Система счисления должна быть от 2 до 36"
                return
            
            if not self.is_valid_number(number, from_base):
                self.error_message = "Некорректное число для выбранной системы"
                return
            
            self.result = self.convert_number(number, from_base, to_base)
            
        except ValueError:
            self.error_message = "Некорректный ввод системы счисления"

    def handle_arithmetic(self):
        """Обработка арифметических операций"""
        self.result = ""
        self.error_message = ""
        
        num1 = self.get_input("Первое число:", 4)
        if not num1:
            return
        
        num2 = self.get_input("Второе число:", 7)
        if not num2:
            return
        
        operation = self.get_input("Операция:", 10)
        if not operation:
            return
        
        base_str = self.get_input("Система счисления:", 13)
        if not base_str:
            return
        
        try:
            base = int(base_str)
            
            if not (2 <= base <= 36):
                self.error_message = "Система счисления должна быть от 2 до 36"
                return
            
            self.result = self.perform_operation(num1, num2, operation, base)
            
        except ValueError:
            self.error_message = "Некорректный ввод системы счисления"

    def run(self):
        """Основной цикл приложения"""
        try:
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            self.screen.keypad(True)
            
            self.init_colors()
            self.show_disclaimer()
            
            while True:
                self.screen.clear()
                height, width = self.screen.getmaxyx()
                
                # Рамка
                self.screen.border()
                
                # Отрисовка текущего экрана
                if self.current_menu == "main":
                    self.draw_menu()
                elif self.current_menu == "conversion":
                    self.draw_conversion_form()
                elif self.current_menu == "arithmetic":
                    self.draw_arithmetic_form()
                elif self.current_menu == "about":
                    self.draw_about()
                
                # Подсказки
                if self.current_menu == "main":
                    self.screen.addstr(height - 2, 2, 
                                     "↑↓ - навигация, Enter - выбор, q - выход", 
                                     curses.color_pair(Colors.YELLOW))
                elif self.current_menu in ["conversion", "arithmetic"]:
                    self.screen.addstr(height - 2, 2, 
                                     "Заполните поля и нажмите Enter, Esc - назад", 
                                     curses.color_pair(Colors.YELLOW))
                
                self.screen.refresh()
                
                # Обработка ввода
                key = self.screen.getch()
                
                if self.current_menu == "main":
                    if key == curses.KEY_UP:
                        self.selected_item = (self.selected_item - 1) % len(self.menu_items["main"])
                    elif key == curses.KEY_DOWN:
                        self.selected_item = (self.selected_item + 1) % len(self.menu_items["main"])
                    elif key == ord('\n'):
                        if self.selected_item == 0:  # Перевод чисел
                            self.current_menu = "conversion"
                        elif self.selected_item == 1:  # Арифметика
                            self.current_menu = "arithmetic"
                        elif self.selected_item == 2:  # О программе
                            self.current_menu = "about"
                        elif self.selected_item == 3:  # Выход
                            break
                    elif key == ord('q'):
                        break
                
                elif self.current_menu == "conversion":
                    if key == ord('\n'):
                        self.handle_conversion()
                    elif key == 27:  # ESC
                        self.current_menu = "main"
                        self.result = ""
                        self.error_message = ""
                
                elif self.current_menu == "arithmetic":
                    if key == ord('\n'):
                        self.handle_arithmetic()
                    elif key == 27:  # ESC
                        self.current_menu = "main"
                        self.result = ""
                        self.error_message = ""
                
                elif self.current_menu == "about":
                    self.current_menu = "main"
        
        except KeyboardInterrupt:
            pass
        finally:
            if self.screen:
                curses.nocbreak()
                self.screen.keypad(False)
                curses.echo()
                curses.endwin()

def main():
    """Главная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print("Calculator TUI v1.0")
        print("MIT License - Copyright (c) 2024")
        return
    
    try:
        calculator = TUICalculator()
        calculator.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()