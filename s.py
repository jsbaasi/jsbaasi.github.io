import json
import os

with open("_data/books.json", "r") as f:
    data = json.load(f)

for key, book in data["books"].items():
    old_cover = book["cover"]
    if old_cover:
        ext = os.path.splitext(old_cover)[1]
        new_cover = key + ext
        old_path = os.path.join("covers", old_cover)
        new_path = os.path.join("covers", new_cover)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"Renamed {old_cover} -> {new_cover}")
        else:
            print(f"File not found: {old_path}")
        book["cover"] = new_cover

with open("_data/books.json", "w") as f:
    json.dump(data, f, indent=2)
