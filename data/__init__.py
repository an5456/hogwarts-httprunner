# class F(object):
#     # def __init__(self):
#     #     self.name = 'A'
#
#     def __getattr__(self, item):
#         if item == 'age':
#             return 40
#         else:
#             raise AttributeError('没有这个属性')
#
#
# f = F()
# print(f.age)
