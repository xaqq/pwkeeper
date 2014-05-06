#!/usr/bin/env python

import scrypt
import sys
import getpass
from Crypto.Cipher import AES
import json
import re

def my_script(to_hash, salt, size=42):
    h = scrypt.hash(to_hash, salt, 2**18, 4, 4, size)
    return h


def load_file(path, cypher):
    with open(path, "rb") as f:
        try:
            content = f.read()
            print content
            data = json.loads(cypher.decrypt(content))
            return data
        except ValueError as e:
            print e
            return []

def add_pw(base_pw, cmd, pwlist):
    try:
        r = re.match("^add\s+(.*) (\d+)( .*)?$", cmd)
        target = r.group(1)
        size = int(r.group(2))
        if r.group(3):
            comment = r.group(3)
        else:
            comment = " "
        pwlist.append({"target": target, "size": size, "comment": comment[1:]})
    except Exception as e:
        print e

def derive(base_pw, target, pwlist):
    for p in pwlist:
        print p["target"]
        if p["target"] == target:
            h = my_script(base_pw, target, p["size"])
            return h
    return "Not found"

def add_padding(input_str):
    r = len(input_str) % 16
    input_str = input_str + " " * (16 - r)
    return input_str

def main():
    pw = getpass.getpass()
    pw2 = getpass.getpass()
    if pw2 != pw:
        return -1

    cypher = AES.new(my_script(pw, "_NSAKEY", 32), AES.MODE_CBC, my_script(pw, "_KEY_IV", 16))
    d = load_file(sys.argv[1], cypher)
    print d
    while True:
        try:
            r = sys.stdin.readline()
            ret = re.match("^derive (.*)$", r)
            if ret:
                h = derive(pw, ret.group(1), d)
                print h.encode("hex")

            if re.match("^add\s+(.*) (\d+)( .*)?$", r):
                ret = add_pw(pw, r, d)

            if r.startswith("list"):
                for entry in d:
                    print entry
        except KeyboardInterrupt as ctrlc:
            with open(sys.argv[1], "wb") as f:
                f.write(cypher.encrypt(add_padding(json.dumps(d))))

if __name__ == "__main__":
    main()
