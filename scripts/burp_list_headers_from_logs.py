import xml.etree.ElementTree as ET
import base64
from http.client import HTTPResponse
from io import BytesIO
import sys

class FakeSocket():
    def __init__(self, response_bytes):
        self._file = BytesIO(response_bytes)
    def makefile(self, *args, **kwargs):
        return self._file

tree = ET.parse(sys.argv[1])
root = tree.getroot()

resps = root.findall('item/response')
headers_list = {}
for r in resps:
    try:
        http_response_bytes = base64.b64decode(r.text)
    except:
        pass
    source = FakeSocket(http_response_bytes)
    response = HTTPResponse(source)
    response.begin()
    headers = response.getheaders() #[('Date', 'Thu, Jul  3 15:27:54 2014'), ('Content-Type', 'text/xml; charset="utf-8"'), ('Connection', 'close'), ('Content-Length', '626')]

    for header in headers:
        if header[0] not in headers_list:
            headers_list[header[0]] = [header[1]]
        else:
            if header[1] not in headers_list[header[0]]:
                headers_list[header[0]].append(header[1])

for k,v in headers_list.items():
    print(k)
    for h in v:
        print("\t"+h)
