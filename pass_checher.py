import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char[0:5]
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}')
    return res

def get_password_leaked_count(hashes, tail):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:    
        if h == tail:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first_5char)
    return get_password_leaked_count(response, tail)
    
def main(args):
    for pword in args:
        count = pwned_api_check(pword)
        if count:
            print(f'The password {pword} was found {count} times. You should consider to change your password.')
        else:
            print('The password {pword} wasn\'t found.')
    return 'All done!'


if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))

