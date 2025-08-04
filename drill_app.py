# Import Python Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from collections import namedtuple
from math import radians, isclose, acos, asin, cos, sin, tan, atan, degrees, sqrt
from PIL import Image

# Insert an icon
icon = Image.open("Resources/well.jpg")

# State the design of the app
st.set_page_config(page_title="DE APP", page_icon=icon)

# Inset CSS Codes to improve the design of the app
st.markdown(
    """
<style>
h1 {text-align: center;
}
body {background-color: #DCE3D5;
      width: 1400px;
      margin: 15px auto;
}
footer {
  display: none;
}
</style>""",
    unsafe_allow_html=True,
)


# Insert title for app
st.title("Drilling Engineering APP.")

st.write("---")

# Add information of the app
st.markdown("""
This app is used to see 3D Wells, as well as, 
calculate basic information about directional trajectories.

**Python:** Pandas, Numpy, Streamlit, PIL, Plotly.
""")

# Add additional information
expander = st.expander("Information")
expander.write("This is an open-source web app fully programmed in Python"
               "for calculating drilling parameters.")

# Insert Image
image = Image.open("Resources/dd.jpg")
st.image(image, width=100, use_container_width=True)

# Insert subheader
st.subheader("**Drilling Fundamentals**")

# Insert a video
video = open("Resources/drilling.mp4", "rb")
st.video(video)

# Inser caption
st.caption("*Video about Drilling Engineering*")

# Sidebar Section
logo = Image.open("Resources/ESPOL.png")
st.sidebar.image(logo)

# Add title to the sidebar section
st.sidebar.title("⬇ Navigation")

# Upload files
file = st.sidebar.file_uploader("**Upload your csv file**")

# Add sections of the app
with st.sidebar:
    options = option_menu(menu_title="Menu", options=["Home", "Data", "3D Plots", "Basic Calculations"],
                          icons=["house", "database", "tv-fill", "calculator"])


# Useful functions to activate each section
# Function to check data
def data(dataframe):
    st.subheader("View Dataframe")
    st.write(dataframe.head())
    st.subheader("Statistical Summary")
    st.write(dataframe.describe())


# Function to visualize 3D Wells
def plots(dataframe):
    st.subheader("Visualize 3D Trajectory of a well")
    x = st.selectbox("Choose DispNS", dataframe.columns)
    y = st.selectbox("Choose DispEW", dataframe.columns)
    z = st.selectbox("Choose TVD", dataframe.columns)
    fig = px.line_3d(dataframe, x, y, z)
    st.plotly_chart(fig)


# Functions to calculate directional parameters
# Function for J type well
Data = namedtuple("Input", "TVD KOP BUR DH")
Output = namedtuple("Output", "R Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_total")


def well_J(data:Data, unit='ingles') -> Output:
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dh = data.DH
    if unit == 'ingles':
        R = 5729.58 / bur
    else:
        R = 1718.87 / bur
    if dh > R:
        dc = dh - R
    elif dh < R:
        dc =  R - dh
    do = tvd - kop
    doc = degrees(atan(dc / do))
    oc = sqrt(dc**2 + do**2)
    boc = degrees(acos(R / oc))
    if R < dh:
        bod = boc - doc
    elif R > dh:
        bod = boc + doc
    theta = 90 - bod
    tvd_eob = kop + abs(R * sin(radians(theta)))
    if unit == 'ingles':
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R - R * cos(radians(theta))
    tan_len = sqrt(oc**2 - R**2)
    if unit == 'ingles':
        md_total = kop + (theta / bur) * 100 + tan_len
    else:
        md_total = kop + (theta / bur) * 30 + tan_len

    output_J = Output(R=R, Theta=theta, TVD_EOB=tvd_eob, Md_EOB=md_eob, Dh_EOB=dh_eob, \
                  Tan_len=tan_len, Md_total=md_total)

    names = ['R', 'theta', 'tvd_EOB', 'Md_EOB', 'Dh_EOB', 'Lengh_tan', 'Md_Total']
    for param, value in zip(names, output_J):
        if unit == "ingles":
            if param == 'theta':
                st.success(f"{param} -> {value:.3f} degrees")
            else:
                st.success(f"{param} -> {value:.3f} ft")

        else:
            if param == 'theta':
                st.success(f"{param} -> {value:.3f} degrees")
            else:
                st.success(f"{param} -> {value:.3f} m")


# Function to calculate S type wells parameters
# Function for S-Type wells

# Function to calculate parameters from a S-Type well
Data_S = namedtuple("Input", "TVD KOP BUR DOR DH")
Output_S = namedtuple("Output", "R1 R2 Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_SOD TVD_SOD Dh_SOD Md_total")


def well_S(data:Data_S, unit='ingles'):
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dor = data.DOR
    dh = data.DH
    if unit == 'ingles':
        R1 = 5729.58 / bur
        R2 = 5729.58 / dor
    else:
        R1 = 1718.87 / bur
        R2 = 1718.87 / dor
    if dh > (R1 + R2):
        fe = dh - (R1 + R2)
    elif dh < (R1 + R2):
        fe = R1 - (dh - R2)
    eo = tvd - kop
    foe = degrees(atan(fe / eo))
    of = sqrt(fe**2 + eo**2)
    fg = R1 + R2
    fog = degrees(asin(fg / of))
    theta = fog - foe
    tvd_eob = kop + R1 * sin(radians(theta))
    if unit == 'ingles':
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R1 - abs(R1 * cos(radians(theta)))
    tan_len = sqrt(of**2 - fg**2)
    if unit == 'ingles':
        md_sod = kop + (theta / bur) * 100 + tan_len
    else:
         md_sod = kop + (theta / bur) * 30 + tan_len
    tvd_sod = tvd_eob + tan_len * abs(cos(radians(theta)))
    dh_sod = dh_eob + abs(tan_len * sin(radians(theta)))
    if unit == 'ingles':
        md_total = kop + (theta / bur) * 100 + tan_len + (theta / dor) * 100
    else:
        md_total = kop + (theta / bur) * 30 + tan_len + (theta / dor) * 30

    output_S = Output_S(R1=R1, R2=R2, Theta=theta, TVD_EOB=tvd_eob, Md_EOB=md_eob, Dh_EOB=dh_eob, \
                    Tan_len=tan_len, Md_SOD=md_sod, TVD_SOD=tvd_sod, Dh_SOD=dh_sod, Md_total=md_total)

    names = ['R1', 'R2', 'theta', 'tvd_EOB', 'Md_EOB', 'Dh_EOB', 'Lengh_tan', 'Md_SOD', 'tvd_SOD', 'Dh_SOD', 'Md_Total']
    for param , value in zip(names, output_S):
        if unit == 'ingles':
            if param == 'theta':
                st.success(f"{param} -> {value:.2f} degrees")
            else:
                st.success(f"{param} -> {value:.2f} ft")
        else:
             if param == 'theta':
                st.success(f"{param} -> {value:.2f} degrees")
             else:
                st.success(f"{param} -> {value:.2f} m")

# Function to calculate Horizontal well parameters
# Function for horizontal wells


# Function to calculate parameters of a Horizontal Well
Data_H = namedtuple("Input", "TVD KOP BUR1 BUR2 DH")
Output_H = namedtuple("Output",
                      "R1 R2 Theta TVD_EOB1 Md_EOB1 Dh_EOB1 Tan_len Md_SOB2 Md_total")


def well_H(data: Data_H, unit='ingles'):
    # Define the variables
    tvd = data.TVD
    kop = data.KOP
    bur1 = data.BUR1
    bur2 = data.BUR2
    dh = data.DH
    # Define curvature radius
    if unit == 'ingles':
        R1 = 5729.58 / bur1
        R2 = 5729.58 / bur2
    else:
        R1 = 1718.87 / bur1
        R2 = 1718.87 / bur2

    eg = (tvd - kop) - R2
    eo = dh - R1
    goe = degrees(atan(eg / eo))
    og = sqrt(eg ** 2 + eo ** 2)
    of = R1 - R2
    gof = degrees(acos(of / og))
    # angle of tangent section
    theta = 180 - goe - gof
    # tvd @ EOB1
    tvd_eob1 = kop + (R1 * sin(radians(theta)))
    # MD @ EOB1
    if unit == 'ingles':
        md_eob1 = kop + (theta / bur1) * 100
    else:
        md_eob1 = kop + (theta / bur1) * 30
    # dh @ EOB1
    dh_eob1 = R1 - (R1 * cos(radians(theta)))
    # BC segment
    tan_len = sqrt(og ** 2 - of ** 2)
    if unit == 'ingles':
        md_sob2 = kop + (theta / bur1) * 100 + tan_len
    else:
        md_sob2 = kop + (theta / bur1) * 30 + tan_len
    # MD total
    if unit == 'ingles':
        md_total = kop + (theta / bur1) * 100 + tan_len + ((90 - theta) / bur2) * 100
    else:
        md_total = kop + (theta / bur1) * 30 + tan_len + ((90 - theta) / bur2) * 30

    output_H = Output_H(R1=R1, R2=R2, Theta=theta, TVD_EOB1=tvd_eob1, Md_EOB1=md_eob1, \
                        Dh_EOB1=dh_eob1, Tan_len=tan_len, Md_SOB2=md_sob2,
                        Md_total=md_total)

    names = ['R1', 'R2', 'Theta', 'TVD_EOB1', 'Md_EOB1', 'Dh_EOB1', 'Tan_len',
             'Md_SOB2', 'Md_total']
    for param, value in zip(names, output_H):
        if unit == 'ingles':
            if param == 'Theta':
                st.success(f"{param} -> {value:.2f} degrees")
            else:
                st.success(f"{param} -> {value:.2f} ft")
        else:
            if param == 'Theta':
                st.success(f"{param} -> {value:.2f} degrees")
            else:
                st.success(f"{param} -> {value:.2f} m")


# Call data
if file:
    df = pd.read_csv(file)

    if options == "Data":
        data(df)

    elif options == "3D Plots":
        plots(df)

if options == "Basic Calculations":
    st.subheader("**Select Units**")
    units = st.selectbox("Units", ("ingles", "metric"))

    if st.checkbox("J type well"):
        Data = namedtuple("Input", "TVD KOP BUR DH")
        st.subheader("**Enter input values**")
        kop = st.number_input("Enter kop value: ")
        tvd = st.number_input("Enter TVD value: ")
        dh = st.number_input("Enter DH value: ")
        bur = st.number_input("Enter bur value: ")
        st.subheader("**Show results**")
        well_J(Data(tvd, kop, bur, dh), units)

    elif st.checkbox("S type well"):
        Data = namedtuple("Input", "TVD KOP BUR DOR DH")
        st.subheader("**Enter input values**")
        kop = st.number_input("Enter kop value: ")
        tvd = st.number_input("Enter TVD value: ")
        dh = st.number_input("Enter DH: ")
        bur = st.number_input("Enter bur: ")
        dor = st.number_input("Enter dor: ")
        st.subheader("**Show results**")
        well_S(Data(tvd, kop, bur, dor, dh), units)

    elif st.checkbox("Horizontal wells"):
        Data = namedtuple("Input", "TVD KOP BUR1 BUR2 DH")
        st.subheader("**Enter input values**")
        kop = st.number_input("Enter kop value: ")
        tvd = st.number_input("Enter TVD value: ")
        dh = st.number_input("Enter dh value: ")
        bur1 = st.number_input("Enter bur1 value: ")
        bur2 = st.number_input("Enter bur2 value: ")
        st.subheader("**Show results**")
        well_H(Data(tvd, kop, bur1, bur2, dh))