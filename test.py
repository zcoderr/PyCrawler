import requests
import time

def test():
    for i in range(10):
        time.sleep(1)
        for i in range(10):
            requests.get("http://140.143.197.154:8080/ifanr/all")
            print(i)


if __name__ == '__main__':
    test()