from configparser import InterpolationMissingOptionError
import subprocess as sb
from time import sleep
import os

def get_ips():
    output = sb.getoutput("kubectl get pods -ocustom-columns=NAME:.metadata.name,IP:.status.podIP")
    output = output.split("\n")
    output.pop(0)
    ips = {} #Stores the hash of Names and IPs of all pods
    for pod in output:
        pod = pod.replace(pod.count(" ")*" ", "@").split("@")
        print(pod)
        ips[pod[0]] = pod[1]

    return ips

def cluster_info():
    sb.run("kubectl exec -it redis-cluster-0  -- redis-cli -c cluster info", shell=True)

sb.run("kubectl apply -f .", shell=True)
pods = sb.getoutput("kubectl get pods | grep redis-cluster | wc -l")
while int(pods) < 9:
    print("\n" + pods, "pods created")
    print("Waiting for for all the pods to be up...")
    sleep(5)
    pods = sb.getoutput("kubectl get pods | grep redis-cluster | wc -l")
    if int(pods) == 9:
        sleep(5)
        print("All pods created successfully...!")

ips = get_ips()
state = sb.getoutput("kubectl exec -it redis-cluster-0  -- redis-cli -c cluster info | grep cluster_state")
print(state)
if "ok" not in state:
    cmd = "kubectl exec -it redis-cluster-0  -- redis-cli  --cluster-replicas 2 --cluster create "
    
    for pod in ips:
        if "redis-cluster" in pod:
            cmd += ips[pod] + ":6379 "
    print(cmd)
    sb.run("echo 'yes' | "+ cmd, shell=True)
    sleep(2)
    state = sb.getoutput("kubectl exec -it redis-cluster-0  -- redis-cli -c cluster info | grep cluster_state")
    if "ok" in state:
        print("\nCluster created successfully..!\n")
        cluster_info()
    else:
        print("\nFailed...!\n")
        cluster_info()
else:   
    print("\nCluster is already active...!\n")
    cluster_info()

