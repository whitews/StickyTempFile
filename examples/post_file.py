import sys
import httplib
from httplib import HTTPException
import json

DEBUG = False

file_path_list = sys.argv[1:]

if len(file_path_list) == 0:
    sys.exit("No files specified")

HOST = "localhost:8000"
POST_URL = '/api/files/'

BOUNDARY = '--------Boundary'


def post_file(host, file_path=None):
    """
    POST a file

    Returns a dictionary with keys:
        'status': The HTTP response code
        'reason': The HTTP response reason
        'headers': The HTTP response headers
        'data': JSON string representation of the file successfully posted, or maybe errors if unsuccessful
    """

    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    body = list()

    # get file and append to body
    file_obj = open(file_path, "rb")
    filename = file_obj.name.split('/')[-1]
    body.append('--%s' % BOUNDARY)
    body.append('Content-Disposition: form-data; name="uploaded_file"; filename="%s"' % filename)
    body.append('Content-Type: application/octet-stream')
    file_obj.seek(0)
    body.append('')
    body.append(file_obj.read())
    file_obj.close()
    body.append('--' + BOUNDARY + '--')
    body.append('')

    body = '\r\n'.join(body)

    conn = httplib.HTTPConnection(host)
    if DEBUG:
        conn.set_debuglevel(1)
    headers = {
        'User-Agent': 'python',
        'Content-Type': content_type,
        'Content-Length': str(len(body)),
        'Connection': 'keep-alive',
    }

    conn.request('POST', POST_URL, body, headers)

    try:
        response = conn.getresponse()
    except Exception, e:
        print e.__class__
        return {
            'status': None,
            'reason': 'No response',
            'data': '',
            'headers': ''
        }

    if response.status == 201:
        try:
            resp = response.read()
            headers = response.getheaders()
        except HTTPException, e:
            print e
            return {
                'status': response.status,
                'reason': 'Could not read response',
                'data': '',
                'headers': ''
            }

        try:
            data = json.loads(resp)
        except Exception, e:
            data = resp
            print e
    else:
        data = response.read()

    return {
        'status': response.status,
        'reason': response.reason,
        'headers': headers,
        'data': data,
    }

print '=' * 40
print 'The following files will be uploaded:'
for file_path in file_path_list:
    print '\t%s' % file_path
print '=' * 40

upload_choice = None
while upload_choice not in ['continue', 'exit']:
    upload_choice = raw_input("Type 'continue' to upload, 'exit' abort: ")
    if upload_choice == 'exit':
        sys.exit()

print 'Uploading...'

for file_path in file_path_list:
    response_dict = post_file(HOST, file_path)

    print "Response: ", response_dict['status'], response_dict['reason']
    print "Headers: "
    print response_dict['headers']
    print "Data:"
    print response_dict['data']
