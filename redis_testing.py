from shelve import Shelf
import subprocess as sb
import json
import unittest
import redis
import requests

from unittest import TestCase    

class TestListElements(unittest.TestCase):
    def __init__(self, first, second):
        self.expected = first
        self.result = second

    def test_count_eq(self):
        self.assertListEqual(self.result, self.expected)


def generator(choice, n, start):
    content = []
    for seq in range(start, start+n):
        if choice == 1:
            content.append(dict({"key" : "new"+str(seq)}))
        if choice == 2:
            content.append(dict({"key" : "new"+str(seq), "value" : "value"+str(seq)}))

    return content
    # with open("keys.json","w") as output:
        # output.write(json_object)


def get_ips():
    output = sb.getoutput("kubectl get pods -ocustom-columns=NAME:.metadata.name,IP:.status.podIP")
    output = output.split("\n")
    output.pop(0)
    ips = {} #Stores the hash of Names and IPs of all pods
    for pod in output:
        pod = pod.replace(pod.count(" ")*" ", "@").split("@")
        ips[pod[0]] = pod[1]

    return ips


def write_keys(redis_ip, content):
    print("Writing to : ", redis_ip)
    try:
        r = requests.post('http://redis.jungle.me/write', json={
            "server" : redis_ip,
            "port" : 6379,
            "content" : content
        })

        return r.text
    except Exception as e:
        return str(e)

def read_keys(redis_ip, keys):
    print("Reading from : ", redis_ip)
    try:
        r = requests.post('http://redis.jungle.me/read', json={
            "server" : redis_ip,
            "port" : 6379,
            "content" : keys
        })

        r = r.json()
        return json.dumps(r)

    except Exception as e:
        return str(e)

def test(N, counter):
    ips = get_ips()
    # Write N keys to A
    content = generator(2, N, counter)
    print(content[0], content[-1])
    print(write_keys(ips['redis-cluster-0'], content), "\n")

    outs = [] #list for storing all outputs from read requests
    # Show all entries in b1 and c2
    content = generator(1, N, counter)
    
    b1 = json.loads(read_keys(ips['redis-cluster-7'], content))
    c2 = json.loads(read_keys(ips['redis-cluster-8'], content))

    outs.append(b1)
    outs.append(c2)

    # Bring down B and immediately write M  entries into C
    print("\nBringing down B..")
    sb.run("kubectl delete pod redis-cluster-1", shell=True)

    M = N*2 
    content = generator(2, M, counter+N)  # Starts righht after the previous key
    print()  
    print(content[0], content[-1])
    print(write_keys(ips['redis-cluster-2'], content), "\n")
    
    # wait for 5 seconds
    sb.run("sleep 5", shell=True)

    # Show all N and M entries in a2 and b1
    content = generator(1, N+M, counter)
    a2 = json.loads(read_keys(ips['redis-cluster-5'], content))
    b1 = json.loads(read_keys(ips['redis-cluster-7'], content))
    outs.append(a2)
    outs.append(b1)

    return outs





# choice = int(input("You want \n1. Keys\n2. Key and Value both\nEnter choice: "))
# n = int(input("Number of keys you want : "))
# start = int(input("Enter starting pont : "))
# content = generator(choice, n, start)
# print(content)
# #write N keys in A

# # Get N keys from b1 and c2
# print("Entries form b1: ")
# print(read_keys(ips['redis-cluster-7'], content))
# print("Entries form c2: ")
# print(read_keys(ips['redis-cluster-8'], content))

