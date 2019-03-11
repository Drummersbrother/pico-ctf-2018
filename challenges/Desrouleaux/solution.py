from json import load
from collections import Counter as cnt

with open("incidents.json", mode="r") as f:
    incidents = load(f)

tickets = incidents["tickets"]
c = cnt([x["src_ip"] for x in tickets])

print(c)
to_check = input("Who to target?")
targeted = set()
for ticket in tickets:
    if ticket["src_ip"] == to_check:
        targeted.add(ticket["dst_ip"])

print(len(targeted))

file_hash_to_recs = {}
for ticket in tickets:
    if ticket["file_hash"] not in file_hash_to_recs:
        file_hash_to_recs[ticket["file_hash"]] = set()
    file_hash_to_recs[ticket["file_hash"]].add(ticket["dst_ip"])
print(file_hash_to_recs)
print(sum(len(x) for x in file_hash_to_recs.values())/len(file_hash_to_recs))

