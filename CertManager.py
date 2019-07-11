# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

import requests, json, base64
import urllib

# ========== Encode string data  ==========
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')
# ========== Encode string data  ==========

# ========== Encode binary file data  ==========
def fileToBase64(filepath):
    fp = open(filepath, "rb")
    data = fp.read()
    fp.close()
    return base64.b64encode(data).decode('utf-8')
# ========== Encode binary file data  ==========

derFileB64 = fileToBase64('/Users/skcrackers/Documents/cobweb/Modules/modules/certification/ssk/signCert.der')
keyFileB64 = fileToBase64('/Users/skcrackers/Documents/cobweb/Modules/modules/certification/ssk/signPri.key')

print('derFileB64 = ' + derFileB64)
print('keyFileB64 = ' + keyFileB64)
