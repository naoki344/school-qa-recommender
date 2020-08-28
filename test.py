import json
from operator import itemgetter
from itertools import groupby

data = [{
    'comment_id': 100,
    'register_date': '2020-02-20T00:18:16.874000+09:00',
    'comment_type': 'message',
    'parent_comment_id': None
}, {
    'comment_id': 102,
    'register_date': '2020-02-22T00:18:16.874000+09:00',
    'comment_type': 'message',
    'parent_comment_id': None
}, {
    'comment_id': 101,
    'register_date': '2020-02-21T00:18:16.874000+09:00',
    'comment_type': 'topic',
    'parent_comment_id': None
}, {
    'comment_id': 103,
    'register_date': '2020-02-23T00:18:16.874000+09:00',
    'comment_type': 'message',
    'parent_comment_id': 101
}, {
    'comment_id': 104,
    'register_date': '2020-02-24T00:18:16.874000+09:00',
    'comment_type': 'message',
    'parent_comment_id': 101
}]

sorted_data = sorted(data, key=itemgetter('comment_id'))

topic_list = []
root_message_list = []
topic_message_list = []
for item in sorted_data:
    if item['parent_comment_id'] is not None:
        topic_message_list.append(item)
        continue

    if item['comment_type'] == 'topic':
        topic_list.append(item)
    else:
        root_message_list.append(item)

sorted_data = sorted(topic_message_list, key=itemgetter('parent_comment_id'))

topic_message_dict = [{
    k: [item for item in v]
} for k, v in groupby(sorted_data, key=itemgetter('parent_comment_id'))]

result = {
    "topic_list": topic_list,
    "root_message_list": root_message_list,
    "topic_message_dict": topic_message_dict,
}
print(json.dumps(result, indent=2))
