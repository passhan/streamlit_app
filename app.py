import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
st.set_page_config(page_title="海外生活における性別ごとの孤独感の分布", layout="wide")
#page_titleはブラウザのタブのタイトルをアプリ名にしている
#layout="wide"は画面横いっぱい使えるようにし、グラフを見やすくしている

st.title('海外生活における性別ごとの孤独感の分布 ')
st.write('海外における孤独・孤立感について、性別ごとの分布をグラフや表で示すアプリです。')

#CSV読み込み
df = pd.read_csv(r'C:\Users\T125025\Documents\streamlit.最終課題\loneliness_by_gender.csv',
                 encoding="utf-8-sig",  #encoding="utf-8-sig"は、日本語のCSVファイルの文字化けやエラーを防いでいる
                 header=1)  

gender_map = {
     "男性": "male",
     "女性": "female",
     "その他": "other",
     "全体":["male", "female", "other"]
}

#サイドバー
with st.sidebar:
    st.header('条件選択')

    gender = st.multiselect('性別を選択してください',
                            ['男性', '女性', 'その他','全体'])
    
    option = st.radio('表示形式を選択してください',
                      ['表', 'グラフ'])

selected_gender = []  #空のリストを作り英語の性別を入れる
for g in gender:  #サイドバーで選んだ性別を取りだす
     if g == "全体":  #全体が選ばれたときのみ、maleとfemaleとotherの3つのため特別処理
          selected_gender.extend(gender_map[g])
     else:
      selected_gender.append(gender_map[g])
    
# フィルタリング
filtered_df = df[df["gender"].isin(selected_gender)]
#選んだ性別だけを残した新しいデータフレームを作る→liltered_df

#表
if option == "表":
     st.dataframe(filtered_df)
    
#横棒グラフ
elif option == "グラフ":
     chart_df = df.pivot(
          index="loneliness_level",
          columns="gender",
          values="count"
     )
     st.line_chart(chart_df)