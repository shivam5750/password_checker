import requests
import hashlib
import sys


def check_firs_5hash(query):
    url = "https://api.pwnedpasswords.com/range/" + query
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check the api and try again')
    else:
        return response


def get_password_leak_count(hashesh, hash_to_check):
    hashesh = (line.split(':') for line in hashesh.text.splitlines())
    for hash, count in hashesh:
        if hash == hash_to_check:
            return count
    return 0


def generating_hash_pass(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5, last_5 = sha1password[0:5], sha1password[5:]
    res = check_firs_5hash(first_5)
    return get_password_leak_count(res, last_5)


def main(args):
    for password in args:
        count = generating_hash_pass(password)
        if count:
            return f'your password has been hacked {count} times. You should probably change your password.'
        else:
            return 'You are safe.Go ahead with this password'
    return 'All done'


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
