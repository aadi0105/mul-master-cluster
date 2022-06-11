import subprocess as sb
import json


def generator(choice, n, start):
    for seq in range(start, start+n+1):
        if choice == 1:
            content.append(dict({"key" : "new"+str(seq)}))
        if choice == 2:
            content.append(dict({"key" : "new"+str(seq), "value" : "value"+str(seq)}))

    json_object=(json.dumps(content, indent=2))
    
    return json_object
    # with open("keys.json","w") as output:
        # output.write(json_object)


def get_ips():
    output = sb.getoutput("kubectl get pods -ocustom-columns=NAME:.metadata.name,IP:.status.podIP")
    output = output.split("\n")
    output.pop(0)
    ips = {} #Stores the hash of Names and IPs of all pods
    for pod in output:
        pod = pod.split("   ")
        ips[pod[0]] = pod[1]

    return ips


def write_keys(redis_ip, content):
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



    ips = get_ips()
    
    choice = int(input("You want \n1. Keys\n2. Key and Value both\nEnter choice: "))
    n = int(input("Number of keys you want : "))
    start = int(input("Enter starting pont : "))
    content = generator(choice, n, start)
    write_keys(ips['redis-cluster-0'], content)

    print("Entries form b1: ")
    print(get_ips(ips['redis-cluster-5'], keys))
    print("Entries form b1: ")
    print(get_ips(ips['redis-cluster-7'], keys))

    
