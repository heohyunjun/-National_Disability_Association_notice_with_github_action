import os
print(os.getenv('TEST'))
print('hi')

os.environ['TEST'] = 1234