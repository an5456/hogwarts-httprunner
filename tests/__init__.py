import os

print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "login.csv"))
print(os.path.join(os.path.dirname(__file__), "api", "get_home_page.yml"))

import random
a = [random.randint(0,10000) for i in range(10)]
print(a)