##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : S1mh0
# @Time : 2024/7/30
# @Version : 1.1--自主选择base85解码方式

import re
import base64, base58, base91, py3base92, base62
import argparse

BASE58 = re.compile("[lI0O]")
BASE32 = re.compile('[a-z189]')

# 判断base92解密是否为正常字符
def check_bytes(aList):
    for i in aList:
        if i > 128:
            return False
    return True


def b16_decode(s):
    try:
        s = base64.b16decode(s)
        try:
            s.decode()
        except:
            return False

        return s
    except:
        return False


def b32_decode(s):
    try:
        s = base64.b32decode(s)
        try:
            s.decode()
        except:
            return False

        return s
    except:
        return False


def b58_decode(s):
    try:
        s = base58.b58decode(s)
        try:
            s.decode()
        except:
            return False

        return s
    except:
        return False


def b62_decode(s):
    try:
        s = s.decode()
        s = base62.decodebytes(s)
        try:
            s.decode()
        except:
            return False

        return s
    except:
        return False


def b64_decode(s):
    try:
        s = base64.b64decode(s)
        try:
            s.decode()
        except:
            return False

        return s
    except:
        return False


def b85_decode(s):
    try:
        if base85_mode == 0:
            s = base64.a85decode(s)
        else:
            s = base64.b85decode(s) # 一般是a85

        try:
            s.decode()
        except:
            return False

        return s
    except:
        return False


def b91_decode(s):
    try:
        s = s.decode()
        s = base91.decode(s)
        try:
            s.decode()
        except:
            return False

        return s
    except:
        return False


def b92_decode(s):
    try:
        s = str(s, 'ascii').replace('\\\\', '\\')
        s = py3base92.b92decode(s).encode()

        list1 = list(s)
        if check_bytes(list1):
            return s
        else:
            return False
    except:
        return False

def all_decode(s):
    count = 0  # 解密次数
    is_ch = 0  # 判断是否是中文

    while True:
        # flag用来记录字符串在当前循环有无被解密过
        flag = 0

        if s.decode() != '':
            # base16
            if b16_decode(s):
                s = b16_decode(s)
                count = count + 1
                print("base16:", s)
                print("\n")
                flag = 1
                continue

            # base32
            if not BASE32.search(s.decode()):  # 加了些限制条件
                if b32_decode(s):
                    s = b32_decode(s)
                    count = count + 1
                    print("base32:", s)
                    print("\n")
                    flag = 1
                    continue

            # base64
            if len(s) % 4 == 0 and '===' not in s[-3:].decode():  # 加了些限制条件
                if b64_decode(s):
                    s = b64_decode(s)
                    count = count + 1
                    print("base64:", s)
                    print("\n")
                    flag = 1
                    continue

            # base58
            if not BASE58.search(s.decode()):  # 加了些限制条件
                if b58_decode(s):
                    s = b58_decode(s)
                    count = count + 1
                    print("base58:", s)
                    print("\n")
                    flag = 1
                    continue

            # base85
            if b85_decode(s):
                s = b85_decode(s)
                count = count + 1
                print("base85:", s)
                print("\n")
                flag = 1
                continue

            # base62
            if b62_decode(s):
                s = b62_decode(s)
                count = count + 1
                print("base62:", s)
                print("\n")
                flag = 1
                continue

            # base91
            if b91_decode(s):
                s = b91_decode(s)
                count = count + 1
                s = bytes(s)
                print("base91:", s)
                print("\n")
                flag = 1
                continue

            # base92
            if b92_decode(s):
                s = b92_decode(s)
                count = count + 1
                print("base92:", s)
                print("\n")
                flag = 1
                continue

        else:
            is_ch = 1
            count = count - 1

        if flag == 0:
            if count == 0:
                print("解密失败")
                break
            else:
                if is_ch == 0:
                    print("结果为：", s)
                else:
                    print("结果为：", s.decode('utf8'))
                print("共解密： " + str(count) + "次")
                break

def main():
    parser = argparse.ArgumentParser(description="Decrypt the strings encrypted by base_encode")
    parser.add_argument('-f', '--file', help='add the path of encrypt strings')
    parser.add_argument('-t', '--text', help='add the encrypt strings')
    parser.add_argument('-b', '--b85', action="store_true", help='use b85decode to decode, default: a85decode')
    args = parser.parse_args()
    global base85_mode
    base85_mode = 0

    if args.b85:
        base85_mode = 1

    if args.file and args.text:
        print("Error: -f and -t parameters cannot be used together.")

    if args.file:
        try:
            s = open(args.file, 'rb').read()
            all_decode(s)
        except:
            print("Error: The file in this path is unreachable.")
    elif args.text:
        s = bytes(args.text.encode())
        all_decode(s)
    else:
        print("Error: Either -f or -t parameter is required.\n")
        print("You can use `-f` to set the path with encrypt_strings_file, such as:")
        print("  base_tool.exe -f base.txt")
        print("or use `-t` to set the encrypt_strings_strings, such as:")
        print("  base_tool.exe -t \"T1JTWEc1QT0=\"")
        print("PS: base85 uses the a85decode, add `-b` to change to the b85decode")

if __name__ == "__main__":
    print("******************************************************************")
    main()
