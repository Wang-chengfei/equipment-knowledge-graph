from config import Config
import unicodedata
import re
config = Config()
discard_list = ["", ",", "/", "[", "]", "citation needed", "and", "now", "at", "&", "later",
                "then", "of", "hybrid", "–", "see", "{", "}", "none", ":", "in", "x", ";",
                "!", "(", ")", "view", "part of", "from", "avre", "list"]


value = ["Military 4x4"]
content = ''
for war in value:
    if not war.startswith("."):
        content += war + " "
content = unicodedata.normalize(config.normalize_signature, content)
content = re.sub(r"\[.*?\]", "", content)
content = re.sub(r"\(.*?\)", "", content)
content = re.sub(r"[^A-Za-z ,\n,/-]", "", content)
content = re.sub(r"-cwt", "", content)
content = re.sub(r"-ton", "", content)
content = re.sub(r" +", " ", content)
content = re.sub(r"truck truck", "truck", content)
content = content.strip()
if content.startswith("x "):
    content = content[2:]
if content.endswith(" x"):
    content = content[:len(content) - 2]
if content.startswith("and "):
    content = content[4:]
if content.endswith(" and"):
    content = content[:len(content) - 4]
content = re.sub(r" +", " ", content)
content = content.strip().lower()
value = []
if "/" in content:
    for item in content.split("/"):
        item = item.strip()
        if item is not None and item.lower() not in discard_list:
            value.append(item)
elif "," in content:
    for item in content.split(","):
        item = item.strip()
        if item is not None and item.lower() not in discard_list:
            value.append(item)
elif "\n" in content:
    for item in content.split("\n"):
        item = item.strip()
        if item is not None and item.lower() not in discard_list:
            value.append(item)
else:
    value = content
print(value)

# string = "T-32 (Š-I-D)"
string = "M939 series 5-ton 6×6 truck"
string = re.search(r"[^A-Za-z0-9 \-()]", string)
print(string)

