import re
import unicodedata

#
# def clean_entity(entity, config):
#     content = []
#     for war in value:
#         war = unicodedata.normalize(config.normalize_signature, war)
#         war = re.sub(r"\[.*?\]", "", war)
#         war = re.sub(r"\[", "", war)
#         war = re.sub(r"\]", "", war)
#         war = re.sub(r"\(.*?\)", "", war)
#         war = re.sub(r"\(", "", war)
#         war = re.sub(r"\)", "", war)
#         war = re.sub(r"and others", "", war)
#         war = war.strip()
#         war = war.strip(".")
#         if war.startswith("x "):
#             war = war[2:]
#         if war.endswith(" x"):
#             war = war[:len(war) - 2]
#         if war.startswith("and "):
#             war = war[4:]
#         if war.endswith(" and"):
#             war = war[:len(war) - 4]
#         add_flag = True  # 是否添加的标记
#         if ":" in war or "see" in war.lower() or "other" in war.lower():
#             add_flag = False
#         elif "operator" in war.lower() or "below" in war.lower():
#             add_flag = False
#         elif war.startswith("-") or war.startswith("from ") or war.startswith("."):
#             add_flag = False
#         elif war.endswith(" by") or war.endswith("-") or war.endswith(" in"):
#             add_flag = False
#         # 检查是否在之前出现过
#         for item in content:
#             if war.lower() in item.lower():
#                 add_flag = False
#                 break
#         if add_flag and war is not None and war.lower() not in discard_list:
#             if "/" in war and key != "Armament":
#                 for item in war.split("/"):
#                     item = item.strip()
#                     if item is not None and item.lower() not in discard_list:
#                         content.append(item)
#             elif "," in war and key != "Armament":
#                 for item in war.split(","):
#                     item = item.strip()
#                     if item is not None and item.lower() not in discard_list:
#                         content.append(item)
#             else:
#                 content.append(war)