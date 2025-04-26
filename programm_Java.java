import java.util.*;

public class Converter {
    private static final String DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    static boolean isValid(String s, int base) {
        for (char c : s.toCharArray()) {
            if (c == '-' || c == '.') continue;
            if (DIGITS.indexOf(Character.toUpperCase(c)) >= base) return false;
        }
        return true;
    }

    static double toDecimal(String s, int base) {
        boolean neg = s.startsWith("-");
        if (neg) s = s.substring(1);
        String[] parts = s.split("\\.");
        String whole = parts[0];
        String frac = parts.length > 1 ? parts[1] : "";
        long wholeVal = 0;
        for (char c : whole.toCharArray())
            wholeVal = wholeVal * base + DIGITS.indexOf(Character.toUpperCase(c));
        double fracVal = 0, p = 1.0 / base;
        for (char c : frac.toCharArray()) {
            fracVal += DIGITS.indexOf(Character.toUpperCase(c)) * p;
            p /= base;
        }
        return neg ? -(wholeVal + fracVal) : wholeVal + fracVal;
    }

    static String fromDecimal(double val, int base) {
        boolean neg = val < 0;
        if (neg) val = -val;
        long whole = (long) val;
        double frac = val - whole;
        StringBuilder sb = new StringBuilder();
        if (whole == 0) sb.append('0');
        while (whole > 0) {
            sb.insert(0, DIGITS.charAt((int) (whole % base)));
            whole /= base;
        }
        if (frac > 0) {
            sb.append('.');
            for (int i = 0; i < 5; i++) {
                frac *= base;
                int d = (int) frac;
                sb.append(DIGITS.charAt(d));
                frac -= d;
            }
        }
        if (neg) sb.insert(0, '-');
        return sb.toString();
    }

    static String convert(String num, int fromBase, int toBase) {
        return fromDecimal(toDecimal(num, fromBase), toBase);
    }

    static String operate(String a, String b, String op, int base) {
        if (!isValid(a, base) || !isValid(b, base)) return "Ошибка";
        double x = toDecimal(a, base);
        double y = toDecimal(b, base);
        double r = 0;
        switch (op) {
            case "+": r = x + y; break;
            case "-": r = x - y; break;
            case "*": r = x * y; break;
            case "/": if (y == 0) return "Ошибка"; r = x / y; break;
            case "**": r = Math.pow(x, y); break;
            case "%": r = x % y; break;
            case "&": r = (long) x & (long) y; break;
            case "|": r = (long) x | (long) y; break;
            case "^": r = (long) x ^ (long) y; break;
            default: return "Ошибка";
        }
        return fromDecimal(r, base);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int mode = sc.nextInt();
        if (mode == 1) {
            String num = sc.next();
            int fromBase = sc.nextInt();
            int toBase = sc.nextInt();
            System.out.println(convert(num, fromBase, toBase));
        } else {
            String a = sc.next();
            String b = sc.next();
            String op = sc.next();
            int base = sc.nextInt();
            System.out.println(operate(a, b, op, base));
        }
    }
}
