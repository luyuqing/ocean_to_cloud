from math import ceil
from collections import OrderedDict


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


def wtcal_output(r1, r2, r3, r4):
    r_max = max(r1, r2, r3, r4)
    r_max = ceil(r_max * 100) / 100
    results = OrderedDict()
    results['Min Requirement For Wall Thickness'] = r_max
    results['Min Requirement For Pressure Containment'] = r1
    results['Min Requirement For Collaps'] = r2
    results['Min Requirement For Propgation Buckling'] = r3
    results['Min Requirement For Reeling Screening Check'] = r4
    # only keeps non-zero value, ie. cal_with checked True
    output = ''
    for k, v in list(results.items()):
        if v:
            output += k + ': ...' + '{:.2f}'.format(v) + '\n'
    return output
