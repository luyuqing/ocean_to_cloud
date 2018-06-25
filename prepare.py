from math import ceil


def zip_form(form):
    list_1 = []
    list_2 = []
    table_list = []
    for field in form:
        table_list.append(field)
    for i, v in enumerate(table_list):
        print(i, v)
        if i % 2 == 0:
            list_1.append(v)
        else:
            list_2.append(v)
    if len(list_1) == len(list_2):
        return list(zip(list_1, list_2))
    final = list(zip(list_1, list_2))
    final.append((list_1[-1], ))
    return final


def ceil_result(res):
    return ceil(res * 100) / 100
