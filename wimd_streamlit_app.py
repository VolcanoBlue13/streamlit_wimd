# -*- coding: utf-8 -*-
# +
"""
Created on Wed Nov 14 11:30:50 2022
@author: Rachel W
"""
import streamlit as st
import time
import pandas as pd
import numpy as np
import altair as alt
import geopandas as gpd
import utils
from PIL import Image

import os
# -

current_dir = os.getcwd()
alt.themes.register("nestafont", utils.nestafont)
alt.themes.enable("nestafont")

colours = utils.NESTA_COLOURS

im = Image.open(f"{current_dir}/images/favicon.ico")
st.set_page_config(page_title='Welsh IMD analysis',  layout='wide', page_icon=im)


header = st.container()

with header:
    nesta_logo = Image.open(f'{current_dir}/images/nesta_logo.png')
    st.image(nesta_logo, width=250)
# This creates a title and adds some markdown for the second column
    st.title("Welsh Index of Multiple Deprivation analysis")
    st.markdown("  **website:** https://www.nesta.org/ **| email:** lizzie.ingram@nesta.org.uk")

def streamlit_wimd():
    with st.spinner('Updating Report...'):
        wimd_data = pd.read_csv(f'{current_dir}/datasets/extreme_10.csv', index_col=0)
        
        st.dataframe(wimd_data)

        selections = ["All", "England ", "France", "Ireland", "Italy", "Scotland", "Wales"]
        country = st.selectbox('Choose country', selections, help = 'Filter report to show only one country')

        regions = alt.topo_feature("http://lle.gov.wales/catalogue/item/LowerSuperOutputAreasLsoasWales2011_Simplified_TopoJSON.json", "LowerSuperOutputAreasLsoasWales20114326")

        map = alt.Chart(regions).mark_geoshape(
            stroke='white',
            strokeWidth=2
        ).encode(
            color=alt.value('#eee'),
        )

        st.altair_chart(map, use_container_width=False)

pwd = st.sidebar.text_input("Password:", type='password')
if pwd == st.secrets["PASSWORD"]:
    streamlit_wimd()
elif pwd == '':
    pass
else:
    st.error('Password incorrect. Please try again.')

