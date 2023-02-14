h_w = list(map(int, input("Введите случайные числа:").split()))  # input to list convert to int
h_w.sort()  # sort list("sort" can be used only for lists)
print("Наименьшее число:", h_w[0])  # output first index from list
print("Наибольшее число:", h_w[-1])  # output last index from list
