import streamlit as st
import cv2 as cv
import time  # to simulate a real time data, time loop
import pandas as pd
import plotly.express as px  # interactive charts
import plotly.graph_objects as go

# f = st.file_uploader("Upload Camels Video")

st.title("Real Time Camels Stride Dashboard")
st.markdown('Powered by **IT Gates Corp.**')

@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_excel('data.xlsx')

df = get_data()
df=df.drop(['Unnamed: 0'],1)

cap = cv.VideoCapture('result.mp4')

stframe = st.empty()
placeholder = st.empty()
i=0
prev_1=0
prev_2=0
first=0
with st.sidebar:
    st.write("This Demo includes:-")
    st.write("1. Camels Detection ✅")
    st.write("2. Camels Tracking ✅")
    st.write("3. Camels Pose Estimation ✅")
    st.write("4. Camels ID Recognition ✅")
    st.write("5. Camels Stride Angle Caclulation ✅")
    v=st.slider( 'Speed',0.5, 2.0, 0.5)
    st.write(f'Delay between frames:%f seconds' %v)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

while cap.isOpened():
    try:
        tempdf=df.iloc[:i+1,:]
    except:
        print('no data')
    ret, frame = cap.read()
    camel1_angle=int(df['Camel 5'][i])
    camel2_angle=int(df['Camel 24'][i])

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        st.success("Done!")
        break
    if df.iloc[i,1]==5 :
        camel1_angle= int(df.iloc[i,2])
        camel2_angle=0
    elif df.iloc[i,1]==24 :
        camel1_angle=0
        camel2_angle= int(df.iloc[i,2])
    stframe.image(frame)
    if first ==0:
        first=1
        time.sleep(1)
        continue
    with placeholder.container():
        camel1, camel2 = st.columns(2)
        camel1.metric(
            label="Camel 🐪: 5",
            value=camel1_angle,
            delta=camel1_angle-prev_1,
        )

        camel2.metric(
            label="Camel 🐪: 24",
            value=camel2_angle,
            delta= camel2_angle-prev_2,
        )
        prev_1=camel1_angle
        prev_2=camel2_angle
        
        st.markdown("### Stride Chart")
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=tempdf['Frame'], y=tempdf['Camel 5'],
                            mode='lines+markers',
                            name='Camel 🐪: 5'))
        fig.add_trace(go.Scatter(x=tempdf['Frame'], y=tempdf['Camel 24'],
                            mode='lines+markers',
                            name='Camel 🐪:24 '))
        st.write(fig)

        st.markdown("### Detailed Data View")
        fig2 = go.Figure(data=[go.Table( header=dict(values=list(df.columns), align='center'),
                        cells=dict(values=[df['Frame'], df['Camel 5'], df['Camel 24']],align='center'))])
        st.write(fig2)

        time.sleep(v)
    i+=1

cap.release()
cv.destroyAllWindows()
        


