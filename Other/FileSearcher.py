import os, fnmatch
import re

path = "C:/TZsofia/TFS/Ingrid_UJ/trunk/web/web2016/frontend/src"


def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            print(re.search(pattern, basename))
            if re.search(pattern, basename):
                filename = os.path.join(root, basename)
                yield filename
            # if fnmatch.fnmatch(basename, pattern):
            #     filename = os.path.join(root, basename)
            #     yield filename


for filename in find_files(path, 'select|union|update|delete|insert|table|from|ascii|hex|unhex|drop'):
    print('Found C source:', filename)



# matches = []
# for root, dirnames, filenames in os.walk(path):
#     for filename in fnmatch.filter(filenames, '*.js'):
#         matches.append(os.path.join(root, filename))


