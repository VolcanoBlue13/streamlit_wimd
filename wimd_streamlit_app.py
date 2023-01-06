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
import utils
from PIL import Image
from itertools import chain

import os

# -

current_dir = os.getcwd()
alt.themes.register("nestafont", utils.nestafont)
alt.themes.enable("nestafont")

colours = utils.NESTA_COLOURS

# here we load the favicon and we set the page config (so what appears in the tab on your web browser)
im = Image.open(f"{current_dir}/images/favicon.ico")
st.set_page_config(page_title="Welsh IMD analysis", layout="wide", page_icon=im)

# this creates a separate container for us to put the header in
header = st.container()

with header:
    nesta_logo = Image.open(f"{current_dir}/images/nesta_logo.png")
    st.image(nesta_logo, width=250)
    # This creates a title and adds some markdown for the second column
    st.title("Welsh Index of Multiple Deprivation analysis")
    st.markdown(
        "  **website:** https://www.nesta.org/ **| email:** lizzie.ingram@nesta.org.uk"
    )

# As it's password protected, we've created a function here which means the app can only run if you've typed the password in.
def streamlit_wimd():
    # This sets a spinner so we know that the report is updating as we change the user selections.
    with st.spinner("Updating Report..."):
        # I've uploaded the dataset to GitHub so it can download everything it git clone and make it work. You can change the dataset locally and it should still work.
        wimd_data = pd.read_csv(f"{current_dir}/datasets/wimd_data.csv")
        regions_lookup = pd.read_csv(f"{current_dir}/datasets/welsh_code_lookups.csv")
        wimd_data = wimd_data.merge(
            regions_lookup,
            left_on="lsoa_code",
            right_on="Lower Layer Super Output Area (LSOA) Code",
            how="right",
        )
        # This radio button lets you pick a larger group so you're not overwhelmed by all the possible categories
        major_grouping_column_data = st.radio(
            "Pick a larger group", ["Population", "WIMD", "FPP", "Rural-Urban"]
        )
        # Once a user has picked a subgroup it assigns it to the variable major_grouping_column_data.
        if major_grouping_column_data == "Population":
            # This is me selecting certain columns which I feel come under the wider group of Population. These huge arrays could go in utils but thought it would be useful to see them here.
            column_data_to_plot = [
                "Number of children 0-5 (2020)",
                "Number of births to mothers aged 24 and under (2020)",
                "Number of births to mothers aged 25-34 (2020)",
                "Number of births to mothers aged 35 and over (2020)",
                "Total number of births (2020)",
                "Population - all ages (2020)",
                "Birth rate per 1000 (2020)",
                "Number of births to mothers aged 24 and under (2019)",
                "Number of births to mothers aged 25-34 (2019)",
                "Number of births to mothers aged 35 and over (2019)",
                "Total number of births (2019)",
                "Population - all ages (2019)",
                "Birth rate per 1000 (2019)",
                "Number of births to mothers aged 24 and under (2018)",
                "Number of births to mothers aged 25-34 (2018)",
                "Number of births to mothers aged 35 and over (2018)",
                "Total number of births (2018)",
                "Population - all ages (2018)",
                "Birth rate per 1000 (2018)",
                "Number of births to mothers aged 24 and under (2017)",
                "Number of births to mothers aged 25-34 (2017)",
                "Number of births to mothers aged 35 and over (2017)",
                "Total number of births (2017)",
                "Population - all ages (2017)",
                "Birth rate per 1000 (2017)",
            ]

        elif major_grouping_column_data == "WIMD":
            # Same here but with the WIMD data
            column_data_to_plot = [
                "WIMD decile",
                "Number of children living in income deprivation aged 0-4 years old (2019)",
                "WIMD income domain deciles",
                "WIMD income domain - percentage of people in income deprivation",
                "WIMD employment domain deciles",
                "WIMD employment domain - percentage of people in employment deprivation",
                "WIMD health domain deciles",
                "WIMD health domain - GP recorded chronic condition rate (per 100)",
                "WIMD health domain - limiting long-term illness rate (per 100)",
                "WIMD health domain - premature death rate (per 100,000)",
                "WIMD health domain - GP recorded mental health condition rate (per 100)",
                "WIMD health domain - cancer incidence rate (per 100,000)",
                "WIMD health domain - low birth weight, live single births less than 2.5 kg (percentage)",
                "WIMD health domain - percentage of children aged 4-5 who are obese",
                "WIMD education domain deciles",
                "WIMD education domain - foundation phase average point score",
                "WIMD education domain - key stage 2 average point score",
                "WIMD education domain - key stage 4 average point score",
                "WIMD education domain - repeat absenteeism percentage",
                "WIMD education domain - percentage of key stage 4 leavers entering higher education",
                "WIMD education domain - percentage of adults aged 25-64 with no qualifications",
                "WIMD access to services domain deciles",
                "WIMD access to services domain - percentage unavailability of broadband at 30 mb/s",
                "WIMD access to services domain - average public return traveltime to a pharmacy (mins)",
                "WIMD access to services domain - average public return traveltime to a food shop (mins)",
                "WIMD access to services domain - average public return traveltime to a GP surgery (mins)",
                "WIMD access to services domain - average public return traveltime to a post office (mins)",
                "WIMD access to services domain - average public return traveltime to a primary school (mins)",
                "WIMD access to services domain - average public return traveltime to a public library (mins)",
                "WIMD access to services domain - average public return traveltime to a sports facility (mins)",
                "WIMD access to services domain - average public return traveltime to a secondary school (mins)",
                "WIMD access to services domain - average private return traveltime to a pharmacy (mins)",
                "WIMD access to services domain - average private return traveltime to a food shop (mins)",
                "WIMD access to services domain - average private return traveltime to a GP surgery (mins)",
                "WIMD access to services domain - average private return traveltime to a post office (mins)",
                "WIMD access to services domain - average private return traveltime to a primary school (mins)",
                "WIMD access to services domain - average private return traveltime to a public library (mins)",
                "WIMD access to services domain - average private return traveltime to a sports facility (mins)",
                "WIMD access to services domain - average private return traveltime to a secondary school (mins)",
                "WIMD access to services domain - average private return traveltime to a petrol station (mins)",
                "WIMD housing domain deciles",
                "WIMD housing domain - percentage of people in overcrowded households",
                "WIMD housing domain - percentage likelihood of poor quality housing",
                "WIMD housing domain - percentage likelihood of housing containing serious hazards",
                "WIMD housing domain - percentage likelihood of housing being in disrepair",
                "WIMD physical environment domain deciles",
                "WIMD physical environment domain - population weighted average concentration value for no2",
                "WIMD physical environment domain - population weighted average concentration value for particulates <10μm",
                "WIMD physical environment domain - population weighted average concentration value for particulates <2.5μm",
                "WIMD physical environment domain - households at risk of flooding score",
                "WIMD physical environment domain - proximity to accessible natural green space score (percentage of households)",
                "WIMD physical environment domain - ambient green space score",
                "WIMD community safety domain deciles",
                "WIMD community safety domain - police recorded criminal damage (rate per 100)",
                "WIMD community safety domain - police recorded violent crime (rate per 100)",
                "WIMD community safety domain - police recorded anit-social behaviour (rate per 100)",
                "WIMD community safety domain - police recorded burglary (rate per 100)",
                "WIMD community safety domain - police recorded theft (rate per 100)",
                "WIMD community safety domain - fire incidences (rate per 100)",
            ]
        elif major_grouping_column_data == "FPP":
            # And again with the FPP data
            column_data_to_plot = ["Foundation phase (mean difference)"]
            # And I thought this was useful but couldn't fit it into any other larger group
        elif major_grouping_column_data == "Rural-Urban":
            column_data_to_plot = ["Rural-Urban", "Rural-Urban detailed classification"]
        # This creates a drop down list to then select the column you want to plot. The list is retrieved from the code above.
        column_selection = st.selectbox(
            "Please pick a minor category to plot", column_data_to_plot
        )

        # filtering down on performance
        if len(column_selection) != 0:
            performance_filter = wimd_data["fpp_performance"].unique()
            performance_selections = st.multiselect(
                "Choose LSOA FPP performance to filter down", performance_filter
            )

        # filtering down on wimd decile
        if len(column_selection) != 0:
            wimd_filter = sorted(wimd_data["wimd_decile"].unique())
            wimd_selections = st.multiselect(
                "Choose WIMD decile to filter down", wimd_filter
            )

        # I used the "Economic Region/ Economic Action Plan Area (EAP) Name" column as an equivalent for regions.
        region_filter = wimd_data[
            "Economic Region/ Economic Action Plan Area (EAP) Name"
        ].unique()

        # This lets you select multiple regions. So you can choose North and Mid Wales for example at the same time.
        region_selections = st.multiselect(
            "Choose region to filter down", region_filter
        )

        #  As the map starts as all of Wales, we don't want it to show an LA filter until someone has selected a region. Once they've selected a region, the region_selections becomes populated
        # so then it'll show the LA selection. Again it's a multiselection option so people can choose more than one LA to view.
        if len(region_selections) != 0:
            local_authority_filter = wimd_data[
                wimd_data["Economic Region/ Economic Action Plan Area (EAP) Name"].isin(
                    region_selections
                )
            ]["Local Authority (LA) Name"].unique()
            local_authority_selections = st.multiselect(
                "Choose LA to filter down", local_authority_filter
            )

        # We still want the map to plot, so if they haven't chosen a region selection, we want the lsoas_to_plot dataframe to be just all LSOAs.
        if len(region_selections) != 0:
            lsoas_to_plot = list(
                wimd_data[
                    wimd_data[
                        "Economic Region/ Economic Action Plan Area (EAP) Name"
                    ].isin(region_selections)
                ]["lsoa_code"]
            )
            if len(local_authority_selections) != 0:
                lsoas_to_plot = list(
                    wimd_data[
                        wimd_data["Local Authority (LA) Name"].isin(
                            local_authority_selections
                        )
                    ]["lsoa_code"]
                )
        else:
            lsoas_to_plot = wimd_data["lsoa_code"].unique()

        # Streamlit will only plot choropleth maps in altair if the shapefile (in this case a topojson) is remote. So I've uploaded the data to my github
        # Altair likes topojsons, so I've used that file format, but we could read in a Shapefile with geopandas and then convert it to a topojson.
        regions = alt.topo_feature(
            "https://raw.githubusercontent.com/VolcanoBlue13/streamlit_wimd/main/datasets/welsh_topojson.json",
            "LSOA_Wales",
        )

        columns = utils.COLUMN_NAME_MAPPINGS
        column_selection_actual_column_name = columns[column_selection]
        # You need to set the type for altair to plot, so I've created an encoding type if/else. If it's going to be text, we want it to be :N, if it's a decile we want it to be :O and if it's a number
        # we want it to be :Q
        columns_nominal = ["rural_urban_classification", "fpp_performance"]
        if column_selection_actual_column_name in columns_nominal:
            encoding_type = ":N"
        elif "decile" in column_selection_actual_column_name:
            encoding_type = ":O"
        else:
            encoding_type = ":Q"

        # This allows you to create the column_name:Q variable for altair
        specified_feature_to_plot = column_selection_actual_column_name + encoding_type

        # This is an alternative condition that I've set up so it plots the LSOAs where there is no value. Earlier on I set the LSOAs which weren't in the original dataset to be -1,
        # so anything that is above 0 we want it to plot normally (i.e. with a colour scale), but if it's got no value, we want it to be a light grey. This sets up the query for later
        # on.
        alternative_condition = "datum." + column_selection_actual_column_name + " > 0"

        ## This sets up the altair selection, so if you click select an LSOA on either the map or the bar chart, it's highlighted on the other one. You need to have a field that is in both charts
        ## for it to link across them.
        click = alt.selection_multi(fields=["lsoa_name_1"])

        data_for_map = wimd_data.copy()
        if len(performance_selections) != 0:
            data_for_map_performance = data_for_map[
                data_for_map["fpp_performance"].isin(performance_selections)
            ]
            if len(wimd_selections) != 0:
                data_for_map_wimd = data_for_map_performance[
                    data_for_map_performance["wimd_decile"].isin(wimd_selections)
                ]
                data_for_map_everything_else = data_for_map[
                    ~(
                        (data_for_map["fpp_performance"].isin(performance_selections))
                        & (data_for_map["wimd_decile"].isin(wimd_selections))
                    )
                ]
                data_for_map_everything_else[column_selection_actual_column_name] = -1
                data_for_map = pd.concat(
                    [data_for_map_performance, data_for_map_everything_else], axis=0
                )
            else:
                data_for_map_everything_else_performance = data_for_map_performance[
                    ~data_for_map_performance["fpp_performance"].isin(
                        performance_selections
                    )
                ]
                data_for_map_everything_else_performance[
                    column_selection_actual_column_name
                ] = -1
                data_for_map = pd.concat(
                    [
                        data_for_map_performance,
                        data_for_map_everything_else_performance,
                    ],
                    axis=0,
                )
        else:
            if len(wimd_selections) != 0:
                data_for_map_wimd = data_for_map[
                    data_for_map["wimd_decile"].isin(wimd_selections)
                ]
                data_for_map_everything_else_wimd = data_for_map[
                    ~data_for_map["wimd_decile"].isin(wimd_selections)
                ]
                data_for_map_everything_else_wimd[
                    column_selection_actual_column_name
                ] = -1
                data_for_map = pd.concat(
                    [data_for_map_wimd, data_for_map_everything_else_wimd], axis=0
                )

        ## The choropleth map is plotted using "regions" which is the remote topojson and we then use altairs .transform_lookup function to link it to the WIMD dataset.
        map = (
            alt.Chart(regions)
            .mark_geoshape(stroke="white")
            .transform_lookup(
                # We want the LSOA11Code field to be the linking column in the regions data.
                lookup="properties.LSOA11Code",
                # And we want to combine it with the wimd_data, using the "lsoa_code" field to link it, and then we want to bring across a number of columns from the WIMD dataset.
                from_=alt.LookupData(
                    data_for_map,
                    "lsoa_code",
                    [
                        column_selection_actual_column_name,
                        "lsoa_name_1",
                        "Rural/ Urban Settlement Classification (RU) Name",
                        "Local Authority (LA) Name",
                        "Economic Region/ Economic Action Plan Area (EAP) Name",
                        "wimd_decile",
                    ],
                ),
                # We then can filter the data if you only want to have a selection of LSOAs.
            )
            .transform_filter(
                alt.FieldOneOfPredicate(
                    field="properties.LSOA11Code", oneOf=lsoas_to_plot
                )
            )
            .encode(
                # As with normal altair functions, we can add a tooltip using any column in the topojson file or one of the columns we've brought across from the other data.
                tooltip=[
                    alt.Tooltip(specified_feature_to_plot, title=column_selection),
                    alt.Tooltip("lsoa_name_1:N", title="LSOA name (1)"),
                    alt.Tooltip("Local Authority (LA) Name:N", title="LA name"),
                    alt.Tooltip(
                        "Rural/ Urban Settlement Classification (RU) Name:N",
                        title="RU name",
                    ),
                    alt.Tooltip("wimd_decile:N", title="WIMD decile"),
                ],
                # We've used alt.condition so altair knows to plot every LSOA that's not got a value as "lightgrey", we set the condition as < 0 as we filled the NaNs as -1. Without this line, it would only
                # plot the LSOAs that have a value.
                color=alt.condition(
                    alternative_condition,
                    alt.Color(
                        specified_feature_to_plot,
                        legend=alt.Legend(
                            orient="none", legendX=-1, title=column_selection
                        ),
                        scale=alt.Scale(scheme="yellowgreenblue"),
                    ),
                    alt.value("lightgrey"),
                ),
                # This condition is dependent on the "click" selection. We want the opacity to be fully opaque normally, but as soon as the selection is in place, we want the rest of the LSOAs to be 0.2 opacity.
                opacity=alt.condition(click, alt.value(1), alt.value(0.2))
                # We need this add_selection to ensure the "click" is added to the choropleth.
            )
            .add_selection(click)
            .properties(width=700, height=650)
        )

        # We don't need every LSOA in the bar chart, but sometimes the column selected might make more sense as ascending than descending or vice versa. So I've added this radio button so you can
        # change which one you want to view.
        ascending_option = st.radio(
            "Select ascending or descending for bar chart", ["Ascending", "Descending"]
        )
        # I've added a slider so you can select a number of LSOAs to show in the bar chart. You may only want to see the top 10 or perhaps you want more.
        no_to_show = st.slider("How many LSOAs to show in bar chart", 0, 5, 100)
        # Unfortunately in pandas, ascending is a True/False value so I've added this in to convert it.
        if ascending_option == "Ascending":
            ascending_val = True
        else:
            ascending_val = False
        # We don't want all the LSOAs, so I've only selected those that are in the WIMD dataset.
        data_for_bar_chart = wimd_data[(wimd_data.lsoa_code.isin(lsoas_to_plot))]
        data_for_bar_chart = data_for_bar_chart.rename(
            columns={"Economic Region/ Economic Action Plan Area (EAP) Name": "Region"}
        )
        if len(performance_selections) != 0:
            data_for_bar_chart = data_for_bar_chart[
                data_for_bar_chart["fpp_performance"].isin(performance_selections)
            ]
        if len(wimd_selections) != 0:
            data_for_bar_chart = data_for_bar_chart[
                data_for_bar_chart["wimd_decile"].isin(wimd_selections)
            ]
        # This then sorts the bar chart by the column selection which is also showing on the map. And it shows the number of rows as selected by the slider.
        data_for_bar_chart = data_for_bar_chart.sort_values(
            by=column_selection_actual_column_name, ascending=ascending_val
        )[:no_to_show]

        # This plots a normal bar chart with the added opacity "alt.condition". This is the same as above.
        bar_chart = (
            alt.Chart(data_for_bar_chart)
            .mark_bar(color=utils.NESTA_COLOURS[1])
            .encode(
                x=alt.X(column_selection_actual_column_name, title=column_selection),
                y=alt.Y(
                    "lsoa_name_1",
                    sort="-x",
                    title="LSOA name (1)",
                    axis=alt.Axis(labelOverlap=False),
                ),
                opacity=alt.condition(click, alt.value(1), alt.value(0.2)),
                tooltip=[
                    alt.Tooltip(
                        column_selection_actual_column_name, title=column_selection
                    ),
                    alt.Tooltip("lsoa_name_1", title="LSOA name (1)"),
                    alt.Tooltip("Local Authority (LA) Name", title="LA name"),
                    alt.Tooltip("Region"),
                    alt.Tooltip("fpp_performance", title="FPP performance"),
                    alt.Tooltip("wimd_decile", title="WIMD decile"),
                ],
            )
            .add_selection(click)
            .properties(width=400, height=400)
        )

        comparator_data = pd.read_csv(f"{current_dir}/datasets/comparator_data.csv")
        comparator_bar_chart = (
            alt.Chart(comparator_data)
            .mark_bar(color=colours[1])
            .encode(
                x=alt.X(column_selection_actual_column_name, title=column_selection),
                y=alt.Y(
                    "comparator_group",
                    sort=[
                        "All LSOAs",
                        "IMD Decile 1",
                        "IMD Decile 2",
                        "IMD Decile 3",
                        "IMD Decile 4",
                        "IMD Decile 5",
                        "IMD Decile 6",
                        "IMD Decile 7",
                        "IMD Decile 8",
                        "IMD Decile 9",
                        "IMD Decile 10",
                    ],
                    title="Comparator Group",
                    axis=alt.Axis(labelOverlap=False),
                ),
            )
        )

        bar_charts = alt.vconcat(bar_chart, comparator_bar_chart)

        # To show it in streamlit, you just need st.altair_chart, and then it can do the rest!
        st.altair_chart(
            alt.hconcat(map, bar_charts)
            .configure_view(strokeWidth=0)
            .resolve_scale("independent")
            .configure_axis(labelLimit=0, titleLimit=0)
            .configure_legend(labelLimit=0, titleLimit=0),
            use_container_width=False,
        )

    # This adds an expander in so you can hide the dataframe and just have the bar charts.
    with st.expander("Dataframe"):
        # The same as before, we want to have the larger groupings first so you're not overwhelmed by choice
        major_grouping_column_data_df = st.multiselect(
            "Pick a larger group for dataframe",
            ["Population", "WIMD", "FPP", "Rural-Urban"],
        )
        # Again we only want the LSOAs which are in the WIMD data.
        dataframe_to_plot = wimd_data.rename(
            columns=dict((v, k) for k, v in utils.COLUMN_NAME_MAPPINGS.items())
        )
        dataframe_to_plot = dataframe_to_plot.rename(
            columns={"Economic Region/ Economic Action Plan Area (EAP) Name": "Region"}
        )
        # This is an empty dataframe so we can add column selection choices to it.
        columns_for_df = []
        if "Population" in major_grouping_column_data_df:
            # This is me selecting certain columns which I feel come under the wider group of Population. These huge arrays could go in utils but thought it would be useful to see them here.
            columns_for_df.append(
                [
                    "Number of children 0-5 (2020)",
                    "Number of births to mothers aged 24 and under (2020)",
                    "Number of births to mothers aged 25-34 (2020)",
                    "Number of births to mothers aged 35 and over (2020)",
                    "Total number of births (2020)",
                    "Population - all ages (2020)",
                    "Birth rate per 1000 (2020)",
                    "Number of births to mothers aged 24 and under (2019)",
                    "Number of births to mothers aged 25-34 (2019)",
                    "Number of births to mothers aged 35 and over (2019)",
                    "Total number of births (2019)",
                    "Population - all ages (2019)",
                    "Birth rate per 1000 (2019)",
                    "Number of births to mothers aged 24 and under (2018)",
                    "Number of births to mothers aged 25-34 (2018)",
                    "Number of births to mothers aged 35 and over (2018)",
                    "Total number of births (2018)",
                    "Population - all ages (2018)",
                    "Birth rate per 1000 (2018)",
                    "Number of births to mothers aged 24 and under (2017)",
                    "Number of births to mothers aged 25-34 (2017)",
                    "Number of births to mothers aged 35 and over (2017)",
                    "Total number of births (2017)",
                    "Population - all ages (2017)",
                    "Birth rate per 1000 (2017)",
                ]
            )
        if "WIMD" in major_grouping_column_data_df:
            # Same here but with the WIMD data
            columns_for_df.append(
                [
                    "Number of children living in income deprivation aged 0-4 years old (2019)",
                    "WIMD income domain deciles",
                    "WIMD income domain - percentage of people in income deprivation",
                    "WIMD employment domain deciles",
                    "WIMD employment domain - percentage of people in employment deprivation",
                    "WIMD health domain deciles",
                    "WIMD health domain - GP recorded chronic condition rate (per 100)",
                    "WIMD health domain - limiting long-term illness rate (per 100)",
                    "WIMD health domain - premature death rate (per 100,000)",
                    "WIMD health domain - GP recorded mental health condition rate (per 100)",
                    "WIMD health domain - cancer incidence rate (per 100,000)",
                    "WIMD health domain - low birth weight, live single births less than 2.5 kg (percentage)",
                    "WIMD health domain - percentage of children aged 4-5 who are obese",
                    "WIMD education domain deciles",
                    "WIMD education domain - foundation phase average point score",
                    "WIMD education domain - key stage 2 average point score",
                    "WIMD education domain - key stage 4 average point score",
                    "WIMD education domain - repeat absenteeism percentage",
                    "WIMD education domain - percentage of key stage 4 leavers entering higher education",
                    "WIMD education domain - percentage of adults aged 25-64 with no qualifications",
                    "WIMD access to services domain deciles",
                    "WIMD access to services domain - percentage unavailability of broadband at 30 mb/s",
                    "WIMD access to services domain - average public return traveltime to a pharmacy (mins)",
                    "WIMD access to services domain - average public return traveltime to a food shop (mins)",
                    "WIMD access to services domain - average public return traveltime to a GP surgery (mins)",
                    "WIMD access to services domain - average public return traveltime to a post office (mins)",
                    "WIMD access to services domain - average public return traveltime to a primary school (mins)",
                    "WIMD access to services domain - average public return traveltime to a public library (mins)",
                    "WIMD access to services domain - average public return traveltime to a sports facility (mins)",
                    "WIMD access to services domain - average public return traveltime to a secondary school (mins)",
                    "WIMD access to services domain - average private return traveltime to a pharmacy (mins)",
                    "WIMD access to services domain - average private return traveltime to a food shop (mins)",
                    "WIMD access to services domain - average private return traveltime to a GP surgery (mins)",
                    "WIMD access to services domain - average private return traveltime to a post office (mins)",
                    "WIMD access to services domain - average private return traveltime to a primary school (mins)",
                    "WIMD access to services domain - average private return traveltime to a public library (mins)",
                    "WIMD access to services domain - average private return traveltime to a sports facility (mins)",
                    "WIMD access to services domain - average private return traveltime to a secondary school (mins)",
                    "WIMD access to services domain - average private return traveltime to a petrol station (mins)",
                    "WIMD housing domain deciles",
                    "WIMD housing domain - percentage of people in overcrowded households",
                    "WIMD housing domain - percentage likelihood of poor quality housing",
                    "WIMD housing domain - percentage likelihood of housing containing serious hazards",
                    "WIMD housing domain - percentage likelihood of housing being in disrepair",
                    "WIMD physical environment domain deciles",
                    "WIMD physical environment domain - population weighted average concentration value for no2",
                    "WIMD physical environment domain - population weighted average concentration value for particulates <10μm",
                    "WIMD physical environment domain - population weighted average concentration value for particulates <2.5μm",
                    "WIMD physical environment domain - households at risk of flooding score",
                    "WIMD physical environment domain - proximity to accessible natural green space score (percentage of households)",
                    "wimd_physical_environment_domain_proximity_to_accessible_natural_green_space_score_percentage_of_households",
                    "WIMD physical environment domain - ambient green space score",
                    "WIMD community safety domain deciles",
                    "WIMD community safety domain - police recorded criminal damage (rate per 100)",
                    "WIMD community safety domain - police recorded violent crime (rate per 100)",
                    "WIMD community safety domain - police recorded anit-social behaviour (rate per 100)",
                    "WIMD community safety domain - police recorded burglary (rate per 100)",
                    "WIMD community safety domain - police recorded theft (rate per 100)",
                    "WIMD community safety domain - fire incidences (rate per 100)",
                ]
            )
        if "FPP" in major_grouping_column_data_df:
            # And again with the FPP data
            columns_for_df.append(
                [
                    "Mean foundation phase score",
                    "Mean foundation phase score (rounded)",
                    "Foundation phase (mean difference)",
                    "Foundation phase performance",
                ]
            )
            # And I thought this was useful but couldn't fit it into any other larger group
        if "Rural-Urban" in major_grouping_column_data_df:
            columns_for_df.append(
                ["Rural-Urban", "Rural-Urban detailed classification"]
            )
        if len(columns_for_df) != 0:
            # when you append arrays, you end up with arrays within arrays. This handy bit of code flattens arrays.
            columns_for_df = list(chain(*columns_for_df))
        ## Using the list of columns, which is selected from the bigger group selection, they can select a number of columns to preview.
        selections_for_dataframe = st.multiselect(
            "Choose one or more columns for dataframe", columns_for_df
        )
        ## If they haven't selected anything, we still want a dataframe to appear.
        if len(selections_for_dataframe) == 0:
            selections_for_dataframe = [
                "LSOA name (1)",
                "LA name",
                "Region",
                "Rural-Urban",
                "Rural-Urban detailed classification",
                "WIMD decile",
                "Foundation phase performance",
            ]
        else:
            ## This combines the columns which I think you'll always want plus any selections made.
            selections_for_dataframe = [
                "LSOA name (1)",
                "LA name",
                "Region",
                "Rural-Urban",
                "Rural-Urban detailed classification",
                "WIMD decile",
                "Foundation phase performance",
            ] + selections_for_dataframe
        ## We then select a dataframe which only has these columns
        dataframe_to_plot = dataframe_to_plot[selections_for_dataframe]
        # Reset the index so it's not weirdly numbered
        dataframe_to_plot.reset_index(inplace=True)
        # We want it to highlight every column, so we need to know how many columns are in the dataframe
        column_number_to_highlight = len(selections_for_dataframe)

        # filtering down on performance
        performance_filter_df = wimd_data["fpp_performance"].unique()
        performance_selections_df = st.multiselect(
            "Optional FPP filter", performance_filter_df
        )

        # filtering down on wimd decile
        wimd_filter_df = sorted(wimd_data["wimd_decile"].unique())
        wimd_selections_df = st.multiselect("Optional WIMD filter", wimd_filter_df)

        # Optional filter for region
        region_filter_df = wimd_data[
            "Economic Region/ Economic Action Plan Area (EAP) Name"
        ].unique()
        region_selections_df = st.multiselect(
            "Optional region filter", region_filter_df
        )

        # creating colours for different fpp_performance conditions
        def performance_colour(x):
            if x["Foundation phase performance"] == "Outperforming":
                return ["background-color: honeydew"] * column_number_to_highlight
            elif x["Foundation phase performance"] == "Underperforming":
                return ["background-color: mistyrose"] * column_number_to_highlight
            elif x["Foundation phase performance"] == "Other":
                return ["background-color: whitesmoke"] * column_number_to_highlight

        if len(performance_selections_df) != 0:
            dataframe_to_plot = dataframe_to_plot[
                dataframe_to_plot["Foundation phase performance"].isin(
                    performance_selections_df
                )
            ]
        if len(wimd_selections_df) != 0:
            dataframe_to_plot = dataframe_to_plot[
                dataframe_to_plot["WIMD decile"].isin(wimd_selections_df)
            ]
        # if len(region_selections_df) != 0:
        # dataframe_to_plot = dataframe_to_plot[dataframe_to_plot["Economic Region/ Economic Action Plan Area (EAP) Name"].isin(region_selections_df)]

        # st.dataframe produces an interactive dataframe and then I've applied styling which means it's red if fpp_performance is underperforming and green if it's overperforming.
        st.dataframe(
            dataframe_to_plot[selections_for_dataframe].style.apply(
                performance_colour, axis=1
            )
        )

    # code to add correlation matrices
    matrix_data_to_plot = wimd_data.rename(
        columns=dict((v, k) for k, v in utils.COLUMN_NAME_MAPPINGS.items())
    )
    vars_for_matrix = [
        var
        for var in matrix_data_to_plot.columns
        if var.startswith(("Number", "Total", "Birth", "Population", "WIMD"))
    ]

    with st.expander("Correlation Matrix"):
        selected_data_for_matrix = st.multiselect(
            "Pick two or more variables to plot in a correlation matrix",
            vars_for_matrix,
        )
        selected_data_for_matrix_copy = selected_data_for_matrix.copy()
        rows = []
        for e1 in selected_data_for_matrix:
            for e2 in selected_data_for_matrix_copy:
                rows.append(
                    [
                        e1,
                        e2,
                        matrix_data_to_plot[selected_data_for_matrix]
                        .corr()
                        .loc[e1, e2],
                    ]
                )
            selected_data_for_matrix_copy.remove(e1)
        df_corr = pd.DataFrame(rows, columns=["Var1", "Var2", "Corr"])
        df_corr = df_corr[df_corr["Var1"] != df_corr["Var2"]]

        if len(selected_data_for_matrix) != 0:
            fig_corr = alt.Chart(df_corr).encode(
                y=alt.Y(
                    "Var2:O", sort=alt.EncodingSortField(order="ascending"), title=None
                ),
                x=alt.X(
                    "Var1:O", sort=alt.EncodingSortField(order="ascending"), title=None
                ),
            )
            domain = [-1, +1]
            cor_plot = fig_corr.mark_rect().encode(
                color=alt.Color("Corr:Q", scale=alt.Scale(domain=domain))
            )
            st.altair_chart(
                (cor_plot)
                .configure_view(strokeWidth=0)
                .resolve_scale("independent")
                .configure_axis(labelLimit=0, titleLimit=0)
            )

    # adding an expanded with further plots for Helen
    with st.expander("Further plots"):
        chart_meanfpp_by_decile = (
            alt.Chart(wimd_data)
            .mark_point(color="#18A48C", size=150)
            .encode(
                x=alt.X(
                    "wimd_decile:N",
                    stack="zero",
                    title="WIMD Decile",
                    axis=alt.Axis(labelAngle=0),
                ),
                y=alt.Y(
                    "mean_fpp_score_rounded:N",
                    sort="descending",
                    title="Mean FPP Score",
                    axis=alt.Axis(grid=True),
                ),
            )
        )
        st.altair_chart(
            (chart_meanfpp_by_decile)
            .properties(width=850, height=450)
            .configure_axis(
                labelLimit=0, titleLimit=0, titleFontSize=15, labelFontSize=15
            )
        )

        chart = (
            alt.Chart(wimd_data)
            .mark_point()
            .encode(
                x=alt.X(
                    "wimd_decile:N",
                    stack="zero",
                    title="WIMD Deprivation Decile",
                    axis=alt.Axis(labelAngle=0),
                ),
                y=alt.Y(
                    "fpp_mean_difference:Q",
                    sort="ascending",
                    title="Difference between FPP Score and Group Mean",
                ),
                size="count():N",
                color=alt.condition(
                    alt.datum.fpp_mean_difference > 0,
                    alt.value("blue"),  # The positive color
                    alt.value("green"),  # The negative color
                ),
            )
        )
        line = alt.Chart(pd.DataFrame({"y": [0]})).mark_rule().encode(y="y")
        st.altair_chart(
            (chart + line)
            .properties(width=1000, height=500)
            .configure_axis(
                labelLimit=0, titleLimit=0, titleFontSize=15, labelFontSize=15
            )
        )


# This adds on the password protection
pwd = st.sidebar.text_input("Password:", type="password")
# st.secrets reads it in from the toml folder, and then runs the streamlit_wimd function if the password matches.
if pwd == st.secrets["PASSWORD"]:
    streamlit_wimd()
elif pwd == "":
    pass
else:
    st.error("Password incorrect. Please try again.")
