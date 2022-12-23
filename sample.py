from zipfile import ZipFile, ZIP_DEFLATED
from os import listdir

with ZipFile('test.zip', 'w') as zipfile:
    zipfile.write('config.json', compress_type=ZIP_DEFLATED)
    zipfile.write('main.log', compress_type=ZIP_DEFLATED)
    zipfile.close()