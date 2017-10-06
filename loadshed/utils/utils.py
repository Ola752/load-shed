
def calc_cumulative_values(a):
    for i in range(1, len(a)):
        a[i] += a[ i -1]

