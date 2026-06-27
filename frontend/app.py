import streamlit as st
import pandas as pd
import requests
import time
import os

from dotenv import load_dotenv

load_dotenv()

Gemini_API_Key = os.getenv("Gemini_API_Key")

st.sidebar.title("メニュー") # サイドバー（ページ切り替えメニューなど）
page = st.sidebar.radio("ページ", ["問い合わせ入力", "履歴一覧"])

if page == "問い合わせ入力": # 問い合わせ入力ページ
    st.title("問い合わせ入力欄")
    st.write("問い合わせを入力してください。")

    with st.form("inquiry_form"): # フォームの開始
        # 1行テキスト
        name = st.text_input("氏名", placeholder="山田太郎")
        question = st.text_area("問い合わせ内容", height=100, placeholder="有給の申請方法を教えてください。")
        category = st.selectbox("カテゴリ", ["休暇", "給与", "福利厚生", "その他"])
        priority = st.select_slider("緊急度", ["高", "中", "低"])
        # agree = st.checkbox("内容を確認しました")
        submitted = st.form_submit_button("送信")

    if submitted:
        errors = [] # バリデーションエラーを格納するリスト
        if name.strip() == "":
            errors.append("氏名を入力してください。")
        if question.strip() == "":
            errors.append("問い合わせ内容を入力してください。")

        # エラー表示
        if errors:
            for error in errors:
                st.error(error)
        else:
            # st.success("入力内容を受け付けました。")
            with st.spinner("回答を生成中..."):
                time.sleep(2)  # 時間のかかる処理を模倣
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/analyze",
                        json={
                            "name": name,
                            "question": question,
                            "category": category,
                            "priority": priority
                        }, #json形式でデータを送る
                        timeout=50 #タイムアウトを50秒に設定
                    )
                    result = response.json()

                    st.write("氏名:", result["name"]) 
                    st.write("カテゴリ:", result["category"])
                    st.write("緊急度:", result["priority"])

                    # 回答の一部を表示（例：最初の50文字）
                    short_answer = result["answer"][:50]
                    st.write("回答案:", short_answer + "...")

                    # 長い回答は折りたたみ
                    with st.expander("回答の全文を見る"):
                        st.write(result["answer"])

                    # st.write("回答案:", result["answer"])
                    # with st.expander("回答の詳細を見る"):
                    #     if result:
                    #         st.write(question)
                    #     else:
                    #         st.write("ここに詳細内容が入ります。")
                except requests.exceptions.RequestException as e:
                    st.error(f"APIへのリクエストに失敗しました: {e}")

# st.success("登録が完了しました。")              # 緑
# st.error("入力に誤りがあります。")               # 赤
# st.warning("この操作は取り消せません。")          # 黄
# st.info("担当者が回答するまでお待ちください。")    # 青

# st.title("ページタイトル")
# st.header("大見出し")
# st.subheader("小見出し")
# st.write("本文テキスト")
# st.markdown("**太字**や *斜体* も書けます")

    

# 列分割（入力フォームと結果を横並びにするときなど）
# col1, col2 = st.columns(2)
# with col1:
#     st.write("左側：入力フォーム")
# with col2:
#     st.write("右側：回答結果")

# 折りたたみ（詳細情報を隠しておくときなど）

elif page == "履歴一覧":   # 問い合わせ履歴ページ
    st.title("問い合わせ履歴")
    resp = requests.get("http://127.0.0.1:8000/inquiries", timeout=10)
    if resp.status_code == 200:
        inquiries = resp.json()
        df = pd.DataFrame(inquiries)
        st.dataframe(df)
        
        if inquiries:
            for item in inquiries:
                 st.write(f"[{item['id']}]{item['created_at']} | {item['name']} {item['question'][:40]}") # 問い合わせ内容の最初の40文字を表示
                 with st.expander("回答の全文を見る"):
                        st.write(item["answer"])
        else:
            st.info("問い合わせ履歴がありません。")

       # 操作可能なテーブル（列幅調整・ソートができる）
# st.table(df)       # 静的なテーブル