# import csv
#
# from collections import defaultdict
#
# with open(filename, 'r') as handle:
#     reader = csv.DictReader(handle, ['name', 'miles', 'country'])
#     data = defaultdict(list)
#
#     for line in reader:
#         data[line['name']).append(int(line['miles']))
#
#     for runner, distances in data.items():
#         print '{} ran a total of {} miles and an average of {} miles'.format(
#             runner, sum(distances), sum(distances) / float(len(distances))
#
#         )
from tests.test_testcase import TestSingle


def res(fun_name):
    f = TestSingle.__dict__
    if fun_name in f:

        f[fun_name]()


res("test_get_login_submit")
