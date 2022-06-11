import json

content = []
choice = int(input("You want \n1. Keys\n2. Key and Value both\nEnter choice: "))
n = int(input("Number of keys you want : "))

for seq in range(1, n):
    if choice == 1:
        content.append(dict({"key" : "new"+str(seq)}))
    if choice == 2:
        content.append(dict({"key" : "new"+str(seq), "value" : "value"+str(seq)}))

json_object=(json.dumps(content, indent=2))
with open("keys.json","w") as output:
    output.write(json_object)
