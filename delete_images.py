import os, logging
path = os.path.dirname(os.path.realpath(__file__))

print('Removing temporary image files...')
for file in os.listdir(path):
    if "Graph" in file and file.endswith('.png'):
        os.remove(file)
        print('File: {}'.format(file))
