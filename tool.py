# 最大公約数を取得
def get_gcd(num_a, num_b):
    if num_a == num_b:
        return num_a
    elif num_a > num_b:
        big = num_a
        small = num_b
    else:
        big = num_b
        small = num_a
    surplus = big % small
    if surplus == 0:
        result = small
    else:
        result = get_gcd(small, surplus)
    return result


def get_ratio(num_a, num_b):
    gcd = get_gcd(num_a, num_b)
    if gcd != 1:
        print(str(int(num_a / gcd)) + ' : ' + str(int(num_b / gcd)))
    else:
        print('their gcd is 1')


if __name__ == '__main__':
    get_ratio(1280, 480)
