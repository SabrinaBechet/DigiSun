
def gregorian_to_JD_Fliegel(y, m, d, hour, minute):
    """algo from Henry F. Fliegel and Thomas C. Van Flandern, 1968 """

    day_frac = (hour + minute/60.)/24.

    part1 = int((m - 14) / 12.)
    part2 = 1461 * (y + 4800 + part1)
    part3 = 367 * (m - 2 - 12 * (part1))
    part4 = int((y + 4900 + part1) / 100. )
    
    jd = ( int(part2 / 4.) +
           int(part3 / 12.) -
           int(3 * part4 / 4.) +
           day_frac + 
           d - 32075)

    # this line to express time in UTC while the reference is at noon -> 0.5 difference
    jd-= 0.5
    
    return jd


def gregorian_to_JD_Meeus(y, m, d, hour, minute):
    """algo from Jean Meeus- Astronomical Algorithms, 1991 """
    if m<3:
        y-=1
        m+=12

    a = int(y/100.)
    if y > 1582:
        b = 2 - a + int(a/4.)
    else:
        b = 0

    day_frac = (hour + minute/60.)/24.
    JD = (int(1461 * (y + 4716)/4.) +
          int(153 * (m + 1)/5.) +
          d +
          day_frac +
          b -
          1524.5)

    return JD
