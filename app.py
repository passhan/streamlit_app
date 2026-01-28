import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

st.set_page_config(page_title="海外生活における性別ごとの孤独感の分布", layout="wide")
#page_titleはブラウザのタブのタイトルをアプリ名にしている
#layout="wide"は画面横いっぱい使えるようにし、グラフを見やすくしている

st.title('海外生活における性別ごとの孤独感の分布 ')
st.write('海外における孤独・孤立感について、性別ごとの分布をグラフや表で示すアプリです。')

#CSV読み込み
df = pd.read_csv(r'C:\Users\T125025\Documents\streamlit.最終課題\loneliness_by_gender.csv',
                 encoding="utf-8-sig",  #encoding="utf-8-sig"は、日本語のCSVファイルの文字化けやエラーを防いでいる
                 header=1)  
df["count"] = pd.to_numeric(df["count"].astype(str).str.replace('"', ''),errors="coerce")
#df["count"].astype(str)で数値も文字列として扱う

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

selected_gender = []  #空のリストを作り英語の性別を入れる
for g in gender:  #サイドバーで選んだ性別を取りだす
     if g == "全体":  #全体が選ばれたときのみ、maleとfemaleとotherの3つのため特別処理
          selected_gender.extend(gender_map[g])
     else:
      selected_gender.append(gender_map[g])

# フィルタリング
filtered_df = df[df["gender"].isin(selected_gender)]
#選んだ性別だけを残した新しいデータフレームを作る→liltered_df

total = filtered_df["count"].sum()
st.metric("選択した性別の総人数", f"{total:,}人")

tab1, tab2 = st.tabs(["表", "グラフ"])

#表タブ
with tab1:
    st.dataframe(filtered_df)
#グラフタブ
with tab2:
    color_on = st.toggle("性別で色分けする")  #toggleで色分けをON/OFFしている
    if color_on:
        color_option = "gender:N"
    else:
        color_option = alt.value("steelblue")

    chart = (alt.Chart(filtered_df)  #filtered_dfで選んだ性別だけのグラフが描かれる
             .mark_bar()  #棒グラフを描く指示
             .encode(  #どのデータをどの軸に置くのか
                 x="count:Q",  #count(人数)をX軸に置く
                 y=alt.Y("loneliness_level:N", sort=["always", "often", "sometimes", "rarely"]),  #孤独レベルをY軸に置く、sort=[]で表示順を指定
                 color=color_option
             )
    )
    st.altair_chart(chart, use_container_width=True)  #作成したグラフをStreamlit上に表示し、chart, use_container_width=Trueで横幅いっぱいに広げ、レイアウトをきれいに見せる