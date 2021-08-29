import sys
from itertools import combinations
# import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def sum_nums(doc_list, loto_setting, n):

    if n == loto_setting["main_n"]:
        ptn = [" ".join([f"[{c}]" for c in doc["main"]]) for doc in doc_list]
        cnt = [1 for i in range(len(doc_list))]
        return ptn, cnt

    sum_dict = {
        " ".join([f"[{c}]" for c in com]): 0
        for com in combinations(loto_setting["nums"], n)
    }

    for doc in doc_list:
        for com in combinations(doc["main"], n):
            sum_dict[" ".join([f"[{c}]" for c in com])] += 1

    sroted_res = sorted(sum_dict.items(), key=lambda x: x[1], reverse=True)
    filtered = [(k, v) for k, v in sroted_res if v > 0]

    return [k for k, v in filtered], [v for k, v in filtered]


def create_summary_loto(data, context):
    # trigger_resource = "projects/roto6-306206/databases/(default)/documents/loto_results/LOTO6/results/0xgWNjRRi6Er6nIv6Y7v"
    # json_str = '''
    # {
    # "oldValue": {},
    # "updateMask": {},
    # "value": {
    #     "createTime": "2021-08-24T14:48:49.835583Z",
    #     "fields": {
    #     "sfdf": {"stringValue": ""}
    #     },
    #     "name": "projects/roto6-306206/databases/(default)/documents/loto_results/LOTO7/results/igVaG1T4VrfKhjVd2gKe",
    #     "updateTime": "2021-08-24T14:48:49.835583Z"}
    # }
    # '''
    # data = json.loads(json_str)

    trigger_resource = context.resource

    if 'loto_results' not in trigger_resource:
        return

    if data["oldValue"] != {}:
        return

    SETTING = {
        "LOTO6": {"nums": range(1, 44), "main_n": 6, "bonus_n": 1},
        "LOTO7": {"nums": range(1, 38), "main_n": 7, "bonus_n": 2},
        "MINI_LOTO": {"nums": range(1, 32), "main_n": 5, "bonus_n": 1},
    }

    # 期間組み合わせ
    PERIOD_PATTERN = [sys.maxsize, 1000, 500, 300, 100, 50, 30, 20]

    # LOTO名称取得
    name = trigger_resource.split('loto_results/')[1].split('/')[0]

    name = "MINI_LOTO"

    # DB設定
    cred = credentials.Certificate('./serviceAccount.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # 読み込み
    users_ref = db.collection('loto_results').document(
        name).collection('results')
    docs = users_ref.stream()
    doc_list = [doc.to_dict() for doc in docs]

    loto_setting = SETTING[name]

    # 回数を数値化
    for i, v in enumerate(doc_list):
        v["title_num"] = int(v["title"].replace('第', '').replace('回', ''))

    latest_title_num = max(dct['title_num'] for dct in doc_list)
    res = []
    for p in PERIOD_PATTERN:
        period_list = list(
            filter(lambda x: x["title_num"] > (latest_title_num - p), doc_list))
        res.append(
            {
                "title": f"{name}",
                "period": f"過去 {p} 回" if p != sys.maxsize else "過去全期間",
                "triple_num_sum": sum_nums(period_list, loto_setting, 3),
                "double_num_sum": sum_nums(period_list, loto_setting, 2),
                "single_num_sum": sum_nums(period_list, loto_setting, 1),
                "complete_num_sum": sum_nums(period_list, loto_setting, loto_setting["main_n"])
            }
        )

    df_base = db.collection('loto_count_summary').document(name)

    for num in ["triple_num_sum", "double_num_sum", "single_num_sum", "complete_num_sum"]:
        for r in res:
            print(num, r["period"])
            doc_ref = df_base.collection(num).document(r['period'])
            doc_ref.set(
                {
                    "title": r["title"],
                    "period": r['period'],
                    "x_axis": r[num][0],
                    "y_axis": r[num][1]
                }
            )
    print('Done')


# target = res[0]
# df = pd.DataFrame.from_dict(target["triple_num_sum"][:100])

# fig = px.bar(
#     df, x=df.key, y=df.value,
#     labels={
#         "key": "組み合わせパターン",
#         "value": "出現回数"
#     },
#     title=f"{name} {target['period']} TOP 100"
# )

# fig.write_html('histogram_with_boxplot.html', auto_open=False)
# fig.show()

# https://plotly.com/python-api-reference/generated/plotly.io.to_html.html
# to_html(fig, include_plotlyjs="cdn", full_html=False,
#         default_width="60%", default_height="60%")
