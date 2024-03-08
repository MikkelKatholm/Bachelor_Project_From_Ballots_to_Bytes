def normalize(poly):
    while poly and poly[-1] == 0:
        poly.pop()
    if poly == []:
        poly.append(0)


def poly_divmod(num, den):
    #Create normalized copies of the args
    num = num[:]
    normalize(num)
    den = den[:]
    normalize(den)

    if len(num) >= len(den):
        #Shift den towards right so it's the same degree as num
        shiftlen = len(num) - len(den)
        den = [0] * shiftlen + den
    else:
        return [0], num

    quot = []
    divisor = float(den[-1])
    for i in range(shiftlen + 1):
        #Get the next coefficient of the quotient.
        mult = num[-1] / divisor
        quot = [mult] + quot

        #Subtract mult * den from num, but don't bother if mult == 0
        #Note that when i==0, mult!=0; so quot is automatically normalized.
        if mult != 0:
            d = [mult * u for u in den]
            num = [u - v for u, v in zip(num, d)]

        num.pop()
        den.pop(0)

    normalize(num)
    return quot, num


def test(num, den):
    print ("%s / %s ->" % (num, den))
    q, r = poly_divmod(num, den)
    print ("quot: %s, rem: %s\n" % (q, r))
    return q, r


def main():
    num = [1, 5, 10, 2, 1]
    num = num[::-1]
    den = [1, 2, 1]
    test(num, den)

    num = [5, 16, 10, 22, 7, 11, 1, 3]
    den = [1, 2, 1, 3]

    quot = [5, 1, 3, 0, 1]
    rem = [0, 5]

    q, r = test(num, den)
    assert quot == q
    assert rem == r


if __name__ == '__main__':
    main()