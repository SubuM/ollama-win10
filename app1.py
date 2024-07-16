
import streamlit as st
import os
import time
import math
import subprocess
import pandas as pd


with st.chat_message(name='assistant'):
    st.write('Welcome to Meta Llama 3: The most capable openly available LLM to date')
    st.write('Please write your query in the chat box below')

text_query = st.chat_input(placeholder='Enter your query')
payload = ''
wrt_done = False

if os.path.isfile('./templlama.txt'):
    os.remove('./templlama.txt')

cmd = ["curl", "http://localhost:11434/api/generate", "-o", "./templlama.txt", "-d"]

if text_query:
    with st.chat_message(name='human'):
        st.write(text_query)

    payload = '{\"model\": \"llama3\", \"prompt\": \"' + text_query + '\"}'
    cmd.append(payload)
    start_time = time.time()
    wrt_done = False
    if not wrt_done:
        with st.spinner('Searching for answer...'):
            time.sleep(1)

    retRes = subprocess.run(cmd)

    wrt_done = True

    df = pd.read_csv('./templlama.txt', sep='\t', header=None)
    tot_time = round(math.ceil(time.time() - start_time))

    if os.path.isfile('./templlama.txt'):
        os.remove('./templlama.txt')

    sub1 = 'response":'
    sub2 = '","done'
    res = ''
    for i in range(len(df)):
        idx1 = df[0][i].index(sub1)
        idx2 = df[0][i].index(sub2)
        res += df[0][i][idx1 + len(sub1) + 1: idx2]

    res = res.replace('\\n', '\n')
    res = res.replace('\\t', '\t')

    with st.chat_message(name='assistant'):
        m, s = divmod(tot_time,60)
        st.write('Response given in: ', m, ' min ', s, ' secs')
        st.write(res)