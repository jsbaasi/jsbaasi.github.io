import json
from datetime import datetime

with open("_data/books.json") as f:
    jf = json.load(f)

for bookname, data in jf["books"].items():
    if data.get("started") and data.get("finished"):
        start = datetime.fromisoformat(data["started"])
        finish = datetime.fromisoformat(data["finished"])
        delta = finish - start
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes = remainder // 60
        data["duration"] = f"{days}d {hours}h {minutes}m"
    else:
        data["duration"] = None

with open("_data/books.json", "w") as f:
    f.write(json.dumps(jf, indent=4))
