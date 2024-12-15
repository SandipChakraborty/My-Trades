

def is_hammer(o, h, l, c):
    body = abs(c - o)
    candle_length = h - l
    lower_shadow = min(o, c) - l
    upper_shadow = h - max(o, c)

    is_small_body = body <= candle_length * 0.3
    is_long_lower_shadow = lower_shadow >= 2 * body
    is_small_upper_shadow = upper_shadow <= body * 0.1

    if is_small_body and is_long_lower_shadow and is_small_upper_shadow:
        return True
    return False


def is_marubozu(open_price, high_price, low_price, close_price, tolerance=0.05):
    upper_shadow = high_price - max(open_price, close_price)
    lower_shadow = min(open_price, close_price) - low_price

    is_bullish_marubozu = close_price == high_price and open_price == low_price
    is_bearish_marubozu = open_price == high_price and close_price == low_price
    is_no_significant_shadows = upper_shadow <= tolerance * (high_price - low_price) and lower_shadow <= tolerance * (
                high_price - low_price)

    if (is_bullish_marubozu or is_bearish_marubozu) and is_no_significant_shadows:
        return True
    return False


def is_green(open_price, close_price):
    return close_price > open_price
