#include <iostream>
#include <string>
#include <cmath>

const std::string digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";

bool isValidNumber(const std::string& s, int base) {
    for (char c : s) {
        if (c == '-' || c == '.') continue;
        if (digits.find(std::toupper(c)) >= static_cast<size_t>(base)) return false;
    }
    return true;
}

double toDecimal(const std::string& s, int base) {
    std::string n = s;
    bool neg = n[0] == '-';
    if (neg) n = n.substr(1);
    size_t dot = n.find('.');
    std::string whole = dot == std::string::npos ? n : n.substr(0, dot);
    std::string frac = dot == std::string::npos ? "" : n.substr(dot + 1);

    long long wholeVal = 0;
    for (char c : whole) wholeVal = wholeVal * base + digits.find(std::toupper(c));

    double fracVal = 0.0;
    double p = 1.0 / base;
    for (char c : frac) {
        fracVal += digits.find(std::toupper(c)) * p;
        p /= base;
    }
    return neg ? -(wholeVal + fracVal) : wholeVal + fracVal;
}

std::string fromDecimal(double value, int base) {
    bool neg = value < 0;
    if (neg) value = -value;
    long long whole = static_cast<long long>(value);
    double frac = value - whole;
    std::string res;
    if (whole == 0) res = "0";
    while (whole > 0) {
        res.insert(res.begin(), digits[whole % base]);
        whole /= base;
    }
    if (frac > 0) {
        res.push_back('.');
        for (int i = 0; i < 5; ++i) {
            frac *= base;
            int d = static_cast<int>(frac);
            res.push_back(digits[d]);
            frac -= d;
        }
    }
    if (neg) res.insert(res.begin(), '-');
    return res;
}

std::string convertNumber(const std::string& number, int fromBase, int toBase) {
    return fromDecimal(toDecimal(number, fromBase), toBase);
}

std::string performOperation(const std::string& a, const std::string& b, const std::string& op, int base) {
    if (!isValidNumber(a, base) || !isValidNumber(b, base)) return "Ошибка";
    double x = toDecimal(a, base);
    double y = toDecimal(b, base);
    double r = 0;
    if (op == "+") r = x + y;
    else if (op == "-") r = x - y;
    else if (op == "*") r = x * y;
    else if (op == "/") { if (y == 0) return "Ошибка"; r = x / y; }
    else if (op == "**") r = std::pow(x, y);
    else if (op == "%") r = std::fmod(x, y);
    else if (op == "&") r = static_cast<long long>(x) & static_cast<long long>(y);
    else if (op == "|") r = static_cast<long long>(x) | static_cast<long long>(y);
    else if (op == "^") r = static_cast<long long>(x) ^ static_cast<long long>(y);
    else return "Ошибка";
    return fromDecimal(r, base);
}

int main() {
    std::cout << "1. Перевод\n2. Арифметика\n";
    int mode; std::cin >> mode;
    if (mode == 1) {
        std::string num; int fromBase, toBase;
        std::cin >> num >> fromBase >> toBase;
        std::cout << convertNumber(num, fromBase, toBase) << '\n';
    } else {
        std::string a, b, op; int base;
        std::cin >> a >> b >> op >> base;
        std::cout << performOperation(a, b, op, base) << '\n';
    }
    return 0;
}
