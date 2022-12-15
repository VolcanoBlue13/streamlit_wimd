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
from itertools import chain

import os
# -

current_dir = os.getcwd()
alt.themes.register("nestafont", utils.nestafont)
alt.themes.enable("nestafont")

colours = utils.NESTA_COLOURS

# here we load the favicon and we set the page config (so what appears in the tab on your web browser)
im = Image.open(f"{current_dir}/images/favicon.ico")
st.set_page_config(page_title='Welsh IMD analysis',  layout='wide', page_icon=im)

# this creates a separate container for us to put the header in
header = st.container()

with header:
    nesta_logo = Image.open(f'{current_dir}/images/nesta_logo.png')
    st.image(nesta_logo, width=250)
# This creates a title and adds some markdown for the second column
    st.title("Welsh Index of Multiple Deprivation analysis")
    st.markdown("  **website:** https://www.nesta.org/ **| email:** lizzie.ingram@nesta.org.uk")

# As it's password protected, we've created a function here which means the app can only run if you've typed the password in.
def streamlit_wimd():
    # This sets a spinner so we know that the report is updating as we change the user selections.
    with st.spinner('Updating Report...'):
        # I've uploaded the dataset to GitHub so it can download everything it git clone and make it work. You can change the dataset locally and it should still work.
        wimd_data = pd.read_csv(f'{current_dir}/datasets/extreme_10.csv', index_col=0)
        # I've added the regions look up so we know which LAs and regions the LSOAs are in.
        regions_lookup = pd.read_csv(f'{current_dir}/datasets/welsh_code_lookups.csv')
        # I've merged the WIMD data with this regions lookup so we have all the of regions data in one dataframe
        wimd_data = wimd_data.merge(regions_lookup, left_on="lsoa_code", right_on="Lower Layer Super Output Area (LSOA) Code", how="right")
        # The "lsoa_code" column will be NaNs for the WIMD data so I've populated the "lsoa_code" column with the LSOA codes that are in the "Lower Layer Super Output Area (LSOA) Code".
        wimd_data['lsoa_code'] = wimd_data['lsoa_code'].fillna(wimd_data.pop('Lower Layer Super Output Area (LSOA) Code'))
        # Everything else that was a NaN I've replaced with -1 (this is any LSOA that wasn't in the original dataset). If you've got a complete dataset, you shouldn't need to do the above line
        # of code or the line below.
        wimd_data.fillna(-1, inplace=True)
        # This radio button lets you pick a larger group so you're not overwhelmed by all the possible categories
        major_grouping_column_data = st.radio("Pick a larger group", ["Population", "WIMD", "FPP", "Rural-Urban"])
        # Once a user has picked a subgroup it assigns it to the variable major_grouping_column_data.
        if major_grouping_column_data == "Population":
            # This is me selecting certain columns which I feel come under the wider group of Population. These huge arrays could go in utils but thought it would be useful to see them here.
            column_data_to_plot = ['number_of_children_0_to_5_2020',
                'number_of_births_2020_to_mothers_24_and_under_years',
                'number_of_births_2020_to_mothers_25_to_34_years',
                'number_of_births_2020_to_mothers_35_and_over_years',
                'total_number_of_births_2020',
                'population_2020_all_ages',
                'birth_rate_per_1000_2020',
                'number_of_births_2019_to_mothers_24_and_under_years',
                'number_of_births_2019_to_mothers_25_to_34_years',
                'number_of_births_2019_to_mothers_35_and_over_years',
                'total_number_of_births_2019',
                'population_2019_all_ages',
                'birth_rate_per_1000_2019',
                'median_age_2019',
                'number_of_births_2018_to_mothers_24_and_under_years',
                'number_of_births_2018_to_mothers_25_to_34_years',
                'number_of_births_2018_to_mothers_35_and_over_years',
                'total_number_of_births_2018',
                'population_2018_all_ages',
                'birth_rate_per_1000_2018',
                'number_of_births_2017_to_mothers_24_and_under_years',
                'number_of_births_2017_to_mothers_25_to_34_years',
                'number_of_births_2017_to_mothers_35_and_over_years',
                'total_number_of_births_2017',
                'population_2017_all_ages',
                'birth_rate_per_1000_2017', 
                'change_birth_rates_18_to_20',
                'change_birth_rates_17_to_20',
                'birthrate_categories_2020',]
        elif major_grouping_column_data == "WIMD":
            # Same here but with the WIMD data
            column_data_to_plot = ['wimd_decile',
                'wimd_income_deprivation_count_0_to_4',
                'wimd_income_domain_deciles',
                'wimd_income_domain_people_in_income_deprivation_percentage',
                'wimd_employment_domain_deciles',
                'wimd_employment_domain_working_age_people_in_employment_deprivation_percentage',
                'wimd_health_domain_deciles',
                'wimd_health_domain_gp_recorded_chronic_condition_rate_per_100',
                'wimd_health_domain_limiting_long_term_illness_rate_per_100',
                'wimd_health_domain_premature_death_rate_per_100,000',
                'wimd_health_domain_gp_recorded_mental_health_condition_rate_per_100',
                'wimd_health_domain_cancer_incidence_rate_per_100,000',
                'wimd_health_domain_low_birth_weight_live_single_births_less_than_2.5kg_percentage',
                'wimd_health_domain_children_aged_4_to_5_who_are_obese_percentage',
                'wimd_education_domain_deciles',
                'wimd_education_domain_foundation_phase_average_point_score',
                'wimd_education_domain_key_stage_2_average_point_score',
                'wimd_education_domain_key_stage_4_average_point_score',
                'wimd_education_domain_repeat_absenteeism_percentage',
                'wimd_education_domain_key_stage_4_leavers_entering_higher_education_percentage',
                'wimd_education_domain_adults_aged_25_to_64_with_no_qualifications_percentage',
                'wimd_access_to_services_domain_deciles',
                'wimd_access_to_services_domain_percentage_unavailability_of_broadband_at_30mb_s',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_pharmacy_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_food_shop_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_gp_surgery_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_post_office_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_primary_school_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_public_library_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_sports_facility_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_secondary_school_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_pharmacy_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_food_shop_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_gp_surgery_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_post_office_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_primary_school_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_public_library_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_sports_facility_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_secondary_school_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_petrol_station_mins',
                'wimd_housing_domain_deciles',
                'wimd_housing_domain_people_in_overcrowded_households_percentage',
                'wimd_housing_domain_likelihood_of_poor_quality_housing_percentage',
                'wimd_housing_domain_likelihood_of_housing_containing_serious_hazards_percentage',
                'wimd_housing_domain_likelihood_of_housing_being_in_disrepair_percentage',
                'wimd_physical_environment_domain_deciles',
                'wimd_physical_environment_domain_population_weighted_average_concentration_value_for_no2',
                'wimd_physical_environment_domain_population_weighted_average_concentration_value_for_particulates_<_10_µm',
                'wimd_physical_environment_domain_population_weighted_average_concentration_value_for_particulates_<_2.5_µm',
                'wimd_physical_environment_domain_households_at_risk_of_flooding_score',
                'wimd_physical_environment_domain_proximity_to_accessible_natural_green_space_score_percentage_of_households',
                'wimd_physical_environment_domain_ambient_green_space_score',
                'wimd_community_safety_domain_deciles',
                'wimd_community_safety_domain_police_recorded_criminal_damage_rate_per_100',
                'wimd_community_safety_domain_police_recorded_violent_crime_rate_per_100',
                'wimd_community_safety_domain_anti_social_behaviour_rate_per_100',
                'wimd_community_safety_domain_police_recorded_burglary_rate_per_100',
                'wimd_community_safety_domain_police_recorded_theft_rate_per_100',
                'wimd_community_safety_domain_fire_incidences_rate_per_100']
        elif major_grouping_column_data == "FPP":
            # And again with the FPP data
            column_data_to_plot =  ['mean_fpp_score',
                'fpp_mean_difference',
                'fpp_performance_vsmean',
                'fpp_mean_difference_category']
            # And I thought this was useful but couldn't fit it into any other larger group
        elif major_grouping_column_data == "Rural-Urban":
            column_data_to_plot = ['rural_urban_settlement_classification_ru_name']
        # This creates a drop down list to then select the column you want to plot. The list is retrieved from the code above.
        column_selection = st.selectbox("Please pick a minor category to plot", column_data_to_plot)

        # I used the "Economic Region/ Economic Action Plan Area (EAP) Name" column as an equivalent for regions.
        region_filter=regions_lookup["Economic Region/ Economic Action Plan Area (EAP) Name"].unique()

        # This lets you select multiple regions. So you can choose North and Mid Wales for example at the same time.
        region_selections=st.multiselect("Choose region to filter down", region_filter)

        #  As the map starts as all of Wales, we don't want it to show an LA filter until someone has selected a region. Once they've selected a region, the region_selections becomes populated
        # so then it'll show the LA selection. Again it's a multiselection option so people can choose more than one LA to view.
        if len(region_selections) != 0:
            local_authority_filter = regions_lookup[regions_lookup["Economic Region/ Economic Action Plan Area (EAP) Name"].isin(region_selections)]["Local Authority (LA) Name"].unique()
            local_authority_selections = st.multiselect("Choose LA to filter down", local_authority_filter)

        # We still want the map to plot, so if they haven't chosen a region selection, we want the lsoas_to_plot dataframe to be just all LSOAs.
        if len(region_selections) != 0:
            lsoas_to_plot = list(regions_lookup[regions_lookup["Economic Region/ Economic Action Plan Area (EAP) Name"].isin(region_selections)]["Lower Layer Super Output Area (LSOA) Code"])
            if len(local_authority_selections) != 0:
                lsoas_to_plot = list(regions_lookup[regions_lookup["Local Authority (LA) Name"].isin(local_authority_selections)]["Lower Layer Super Output Area (LSOA) Code"])
        else:
            lsoas_to_plot = regions_lookup["Lower Layer Super Output Area (LSOA) Code"].unique()

        # Streamlit will only plot choropleth maps in altair if the shapefile (in this case a topojson) is remote. So I've uploaded the data to my github
        # Altair likes topojsons, so I've used that file format, but we could read in a Shapefile with geopandas and then convert it to a topojson.
        regions = alt.topo_feature("https://raw.githubusercontent.com/VolcanoBlue13/streamlit_wimd/main/datasets/welsh_topojson.json", "LSOA_Wales")
        
        # You need to set the type for altair to plot, so I've created an encoding type if/else. If it's going to be text, we want it to be :N, if it's a decile we want it to be :O and if it's a number
        # we want it to be :Q
        columns_nominal = ["rural_urban_settlement_classification_ru_name", "change_birth_rates_18_to_20", "change_birth_rates_17_to_20", "birthrate_categories_2020", "fpp_performance_vsmean"]
        if column_selection in columns_nominal:
            encoding_type = ":N"
        elif "decile" in column_selection:
            encoding_type = ":O"
        else:
            encoding_type = ":Q"
        
        # This allows you to create the column_name:Q variable for altair
        specified_feature_to_plot = column_selection + encoding_type

        # This is an alternative condition that I've set up so it plots the LSOAs where there is no value. Earlier on I set the LSOAs which weren't in the original dataset to be -1,
        # so anything that is above 0 we want it to plot normally (i.e. with a colour scale), but if it's got no value, we want it to be a light grey. This sets up the query for later
        # on.
        alternative_condition = 'datum.' + column_selection + " > 0"
        
        ## This sets up the altair selection, so if you click select an LSOA on either the map or the bar chart, it's highlighted on the other one. You need to have a field that is in both charts
        ## for it to link across them.
        click = alt.selection_multi(fields=['LSOA Name'])

        ## The choropleth map is plotted using "regions" which is the remote topojson and we then use altairs .transform_lookup function to link it to the WIMD dataset.
        map = alt.Chart(regions).mark_geoshape(stroke="white").transform_lookup(
            # We want the LSOA11Code field to be the linking column in the regions data.
            lookup='properties.LSOA11Code',
            # And we want to combine it with the wimd_data, using the "lsoa_code" field to link it, and then we want to bring across a number of columns from the WIMD dataset.
            from_= alt.LookupData(wimd_data, 'lsoa_code', [column_selection,"LSOA Name", 'Rural/ Urban Settlement Classification (RU) Name',"Local Authority (LA) Name", "Economic Region/ Economic Action Plan Area (EAP) Name"]),
        # We then can filter the data if you only want to have a selection of LSOAs.
        ).transform_filter(alt.FieldOneOfPredicate(field='properties.LSOA11Code', oneOf=lsoas_to_plot)).encode(
        # As with normal altair functions, we can add a tooltip using any column in the topojson file or one of the columns we've brought across from the other data.
        tooltip=alt.Tooltip(['properties.lsoa11name:N',"Local Authority (LA) Name:N","Rural/ Urban Settlement Classification (RU) Name:N"]),
        # We've used alt.condition so altair knows to plot every LSOA that's not got a value as "lightgrey", we set the condition as < 0 as we filled the NaNs as -1. Without this line, it would only
        # plot the LSOAs that have a value.
        color=alt.condition(alternative_condition, specified_feature_to_plot, alt.value("lightgrey")),
        # This condition is dependent on the "click" selection. We want the opacity to be fully opaque normally, but as soon as the selection is in place, we want the rest of the LSOAs to be 0.2 opacity.
        opacity=alt.condition(click, alt.value(1), alt.value(0.2))
        # We need this add_selection to ensure the "click" is added to the choropleth.
        ).add_selection(click).properties(
            width=700,
            height=500
        )

        # We don't need every LSOA in the bar chart, but sometimes the column selected might make more sense as ascending than descending or vice versa. So I've added this radio button so you can
        # change which one you want to view.
        ascending_option = st.radio("Select ascending or descending for bar chart", ["Ascending", "Descending"])
        # I've added a slider so you can select a number of LSOAs to show in the bar chart. You may only want to see the top 10 or perhaps you want more.
        no_to_show = st.slider('How many LSOAs to show in bar chart', 0, 5, 50)
        # Unfortunately in pandas, ascending is a True/False value so I've added this in to convert it.
        if ascending_option == "Ascending":
            ascending_val = True
        else:
            ascending_val = False
        # We don't want all the LSOAs, so I've only selected those that are in the WIMD dataset.
        data_for_bar_chart = wimd_data[(wimd_data.lsoa_code.isin(utils.LSOA_IN_EXTREME_10)) & (wimd_data.lsoa_code.isin(lsoas_to_plot))]
        # This then sorts the bar chart by the column selection which is also showing on the map. And it shows the number of rows as selected by the slider.
        data_for_bar_chart = data_for_bar_chart.sort_values(by = column_selection, ascending=ascending_val)[:no_to_show]

        # This plots a normal bar chart with the added opacity "alt.condition". This is the same as above.
        bar_chart = alt.Chart(data_for_bar_chart).mark_bar(color=utils.NESTA_COLOURS[1]).encode(
            x = column_selection,
            y = alt.Y("LSOA Name", sort="-x"),
            opacity=alt.condition(click, alt.value(1), alt.value(0.2))
        ).add_selection(click).properties(width=400, height=300)

        # To show it in streamlit, you just need st.altair_chart, and then it can do the rest!
        st.altair_chart(alt.hconcat(map,bar_chart).configure_view(strokeWidth=0).resolve_scale("independent"), use_container_width=False)

    # This adds an expander in so you can hide the dataframe and just have the bar charts.
    with st.expander("Dataframe"):
        # The same as before, we want to have the larger groupings first so you're not overwhelmed by choice
        major_grouping_column_data_df = st.multiselect("Pick a larger group for dataframe", ["Population", "WIMD", "FPP", "Rural-Urban"])
        # Again we only want the LSOAs which are in the WIMD data.
        dataframe_to_plot = wimd_data[wimd_data.lsoa_code.isin(utils.LSOA_IN_EXTREME_10)]
        # This is an empty dataframe so we can add column selection choices to it.
        columns_for_df = []
        if "Population" in major_grouping_column_data_df:
            columns_for_df.append(['number_of_children_0_to_5_2020',
                'number_of_births_2020_to_mothers_24_and_under_years',
                'number_of_births_2020_to_mothers_25_to_34_years',
                'number_of_births_2020_to_mothers_35_and_over_years',
                'total_number_of_births_2020',
                'population_2020_all_ages',
                'birth_rate_per_1000_2020',
                'number_of_births_2019_to_mothers_24_and_under_years',
                'number_of_births_2019_to_mothers_25_to_34_years',
                'number_of_births_2019_to_mothers_35_and_over_years',
                'total_number_of_births_2019',
                'population_2019_all_ages',
                'birth_rate_per_1000_2019',
                'median_age_2019',
                'number_of_births_2018_to_mothers_24_and_under_years',
                'number_of_births_2018_to_mothers_25_to_34_years',
                'number_of_births_2018_to_mothers_35_and_over_years',
                'total_number_of_births_2018',
                'population_2018_all_ages',
                'birth_rate_per_1000_2018',
                'number_of_births_2017_to_mothers_24_and_under_years',
                'number_of_births_2017_to_mothers_25_to_34_years',
                'number_of_births_2017_to_mothers_35_and_over_years',
                'total_number_of_births_2017',
                'population_2017_all_ages',
                'birth_rate_per_1000_2017', 
                'change_birth_rates_18_to_20',
                'change_birth_rates_17_to_20',
                'birthrate_categories_2020'])
        if "WIMD" in major_grouping_column_data_df:
            columns_for_df.append(['wimd_decile',
                'wimd_income_deprivation_count_0_to_4',
                'wimd_income_domain_deciles',
                'wimd_income_domain_people_in_income_deprivation_percentage',
                'wimd_employment_domain_deciles',
                'wimd_employment_domain_working_age_people_in_employment_deprivation_percentage',
                'wimd_health_domain_deciles',
                'wimd_health_domain_gp_recorded_chronic_condition_rate_per_100',
                'wimd_health_domain_limiting_long_term_illness_rate_per_100',
                'wimd_health_domain_premature_death_rate_per_100,000',
                'wimd_health_domain_gp_recorded_mental_health_condition_rate_per_100',
                'wimd_health_domain_cancer_incidence_rate_per_100,000',
                'wimd_health_domain_low_birth_weight_live_single_births_less_than_2.5kg_percentage',
                'wimd_health_domain_children_aged_4_to_5_who_are_obese_percentage',
                'wimd_education_domain_deciles',
                'wimd_education_domain_foundation_phase_average_point_score',
                'wimd_education_domain_key_stage_2_average_point_score',
                'wimd_education_domain_key_stage_4_average_point_score',
                'wimd_education_domain_repeat_absenteeism_percentage',
                'wimd_education_domain_key_stage_4_leavers_entering_higher_education_percentage',
                'wimd_education_domain_adults_aged_25_to_64_with_no_qualifications_percentage',
                'wimd_access_to_services_domain_deciles',
                'wimd_access_to_services_domain_percentage_unavailability_of_broadband_at_30mb_s',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_pharmacy_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_food_shop_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_gp_surgery_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_post_office_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_primary_school_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_public_library_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_sports_facility_mins',
                'wimd_access_to_services_domain_average_public_return_travel_time_to_a_secondary_school_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_pharmacy_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_food_shop_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_gp_surgery_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_post_office_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_primary_school_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_public_library_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_sports_facility_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_secondary_school_mins',
                'wimd_access_to_services_domain_average_private_return_travel_time_to_a_petrol_station_mins',
                'wimd_housing_domain_deciles',
                'wimd_housing_domain_people_in_overcrowded_households_percentage',
                'wimd_housing_domain_likelihood_of_poor_quality_housing_percentage',
                'wimd_housing_domain_likelihood_of_housing_containing_serious_hazards_percentage',
                'wimd_housing_domain_likelihood_of_housing_being_in_disrepair_percentage',
                'wimd_physical_environment_domain_deciles',
                'wimd_physical_environment_domain_population_weighted_average_concentration_value_for_no2',
                'wimd_physical_environment_domain_population_weighted_average_concentration_value_for_particulates_<_10_µm',
                'wimd_physical_environment_domain_population_weighted_average_concentration_value_for_particulates_<_2.5_µm',
                'wimd_physical_environment_domain_households_at_risk_of_flooding_score',
                'wimd_physical_environment_domain_proximity_to_accessible_natural_green_space_score_percentage_of_households',
                'wimd_physical_environment_domain_ambient_green_space_score',
                'wimd_community_safety_domain_deciles',
                'wimd_community_safety_domain_police_recorded_criminal_damage_rate_per_100',
                'wimd_community_safety_domain_police_recorded_violent_crime_rate_per_100',
                'wimd_community_safety_domain_anti_social_behaviour_rate_per_100',
                'wimd_community_safety_domain_police_recorded_burglary_rate_per_100',
                'wimd_community_safety_domain_police_recorded_theft_rate_per_100',
                'wimd_community_safety_domain_fire_incidences_rate_per_100'])
        if "FPP" in major_grouping_column_data_df:
            columns_for_df.append(['mean_fpp_score',
                'Mean FPP Score',
                'fpp_mean_difference',
                'fpp_mean_difference_category'])
        if "Rural-Urban" in major_grouping_column_data_df:
            columns_for_df.append(['rural_urban_settlement_classification_ru_name'])
        if len(columns_for_df) != 0:
            # when you append arrays, you end up with arrays within arrays. This handy bit of code flattens arrays.
            columns_for_df = list(chain(*columns_for_df))
        ## Using the list of columns, which is selected from the bigger group selection, they can select a number of columns to preview.
        selections_for_dataframe = st.multiselect("Choose one or more columns for dataframe", columns_for_df)
        ## If they haven't selected anything, we still want a dataframe to appear.
        if len(selections_for_dataframe) == 0: 
            selections_for_dataframe = ["LSOA Name", "Local Authority (LA) Name", "Rural/ Urban Settlement Classification (RU) Name", "fpp_performance_vsmean"]
        else:
        ## This combines the columns which I think you'll always want plus any selections made.
            selections_for_dataframe = ["LSOA Name", "Local Authority (LA) Name", "Rural/ Urban Settlement Classification (RU) Name", "fpp_performance_vsmean"] + selections_for_dataframe
        ## We then select a dataframe which only has these columns
        dataframe_to_plot=dataframe_to_plot[selections_for_dataframe]
        # Reset the index so it's not weirdly numbered
        dataframe_to_plot.reset_index(inplace=True)
        # We want it to highlight every column, so we need to know how many columns are in the dataframe
        column_number_to_highlight = len(selections_for_dataframe)
        # st.dataframe produces an interactive dataframe and then I've applied styling which means it's red if fpp_performance_vsmean is underperforming and green if it's overperforming.
        st.dataframe(dataframe_to_plot[selections_for_dataframe].style.apply(lambda x: ['background-color: mistyrose']*column_number_to_highlight if x.fpp_performance_vsmean == "Underperforming" else ['background-color: honeydew']*column_number_to_highlight, axis=1))

# This adds on the password protection
pwd = st.sidebar.text_input("Password:", type='password')
# st.secrets reads it in from the toml folder, and then runs the streamlit_wimd function if the password matches.
if pwd == st.secrets["PASSWORD"]:
    streamlit_wimd()
elif pwd == '':
    pass
else:
    st.error('Password incorrect. Please try again.')

