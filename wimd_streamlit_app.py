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
        regions_lookup = pd.read_csv(f'{current_dir}/datasets/welsh_code_lookups.csv')
        wimd_data = wimd_data.merge(regions_lookup, left_on="lsoa_code", right_on="Lower Layer Super Output Area (LSOA) Code", how="right")
        wimd_data['lsoa_code'] = wimd_data['lsoa_code'].fillna(wimd_data.pop('Lower Layer Super Output Area (LSOA) Code'))
        wimd_data.fillna(-1, inplace=True)

        major_grouping_column_data = st.radio("Pick a larger group", ["WIMD", "Population", "FPP", "Rural-Urban"])
        if major_grouping_column_data == "Population":
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
            column_data_to_plot = ['wimd_decile',
                'wimd_income_deprivation_count_0_to_4',
                'wimd_income_domain_deciles',
                'wimd_income_domain_people_in_income_deprivation_%',
                'wimd_employment_domain_deciles',
                'wimd_employment_domain_working_age_people_in_employment_deprivation_%',
                'wimd_health_domain_deciles',
                'wimd_health_domain_gp_recorded_chronic_condition_rate_per_100',
                'wimd_health_domain_limiting_long_term_illness_rate_per_100',
                'wimd_health_domain_premature_death_rate_per_100,000',
                'wimd_health_domain_gp_recorded_mental_health_condition_rate_per_100',
                'wimd_health_domain_cancer_incidence_rate_per_100,000',
                'wimd_health_domain_low_birth_weight_live_single_births_less_than_2.5kg_%',
                'wimd_health_domain_children_aged_4_to_5_who_are_obese_%',
                'wimd_education_domain_deciles',
                'wimd_education_domain_foundation_phase_average_point_score',
                'wimd_education_domain_key_stage_2_average_point_score',
                'wimd_education_domain_key_stage_4_average_point_score',
                'wimd_education_domain_repeat_absenteeism_%',
                'wimd_education_domain_key_stage_4_leavers_entering_higher_education_%',
                'wimd_education_domain_adults_aged_25_to_64_with_no_qualifications_%',
                'wimd_access_to_services_domain_deciles',
                'wimd_access_to_services_domain_%_unavailability_of_broadband_at_30mb_s',
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
                'wimd_housing_domain_people_in_overcrowded_households_%',
                'wimd_housing_domain_likelihood_of_poor_quality_housing_%',
                'wimd_housing_domain_likelihood_of_housing_containing_serious_hazards_%',
                'wimd_housing_domain_likelihood_of_housing_being_in_disrepair_%',
                'wimd_physical_environment_domain_deciles',
                'wimd_physical_environment_domain_population_weighted_average_concentration_value_for_no2',
                'wimd_physical_environment_domain_population_weighted_average_concentration_value_for_particulates_<_10_µm',
                'wimd_physical_environment_domain_population_weighted_average_concentration_value_for_particulates_<_2.5_µm',
                'wimd_physical_environment_domain_households_at_risk_of_flooding_score',
                'wimd_physical_environment_domain_proximity_to_accessible_natural_green_space_score_%_of_households',
                'wimd_physical_environment_domain_ambient_green_space_score',
                'wimd_community_safety_domain_deciles',
                'wimd_community_safety_domain_police_recorded_criminal_damage_rate_per_100',
                'wimd_community_safety_domain_police_recorded_violent_crime_rate_per_100',
                'wimd_community_safety_domain_anti_social_behaviour_rate_per_100',
                'wimd_community_safety_domain_police_recorded_burglary_rate_per_100',
                'wimd_community_safety_domain_police_recorded_theft_rate_per_100',
                'wimd_community_safety_domain_fire_incidences_rate_per_100']
        elif major_grouping_column_data == "FPP":
            column_data_to_plot =  ['mean_fpp_score',
                'Mean FPP Score',
                'fpp_mean_difference',
                'fpp_performance_vsmean',
                'fpp_mean_difference_category']
        elif major_grouping_column_data == "Rural-Urban":
            column_data_to_plot = ['rural_urban_settlement_classification_ru_name']
        column_selection = st.selectbox("Please pick a minor category to plot", column_data_to_plot)


        region_filter=regions_lookup["Economic Region/ Economic Action Plan Area (EAP) Name"].unique()
        region_selections=st.multiselect("Choose region to filter down", region_filter)
        if len(region_selections) != 0:
            local_authority_filter = regions_lookup[regions_lookup["Economic Region/ Economic Action Plan Area (EAP) Name"].isin(region_selections)]["Local Authority (LA) Name"].unique()
            local_authority_selections = st.multiselect("Choose LA to filter down", local_authority_filter)

        if len(region_selections) != 0:
            lsoas_to_plot = list(regions_lookup[regions_lookup["Economic Region/ Economic Action Plan Area (EAP) Name"].isin(region_selections)]["Lower Layer Super Output Area (LSOA) Code"])
            if len(local_authority_selections) != 0:
                lsoas_to_plot = list(regions_lookup[regions_lookup["Local Authority (LA) Name"].isin(local_authority_selections)]["Lower Layer Super Output Area (LSOA) Code"])
        else:
            lsoas_to_plot = regions_lookup["Lower Layer Super Output Area (LSOA) Code"].unique()

        regions = alt.topo_feature("https://raw.githubusercontent.com/VolcanoBlue13/streamlit_wimd/main/datasets/welsh_topojson.json", "LSOA_Wales")

        columns_nominal = ["rural_urban_settlement_classification_ru_name", "change_birth_rates_18_to_20", "change_birth_rates_17_to_20", "birthrate_categories_2020", "fpp_performance_vsmean"]
        if column_selection in columns_nominal or "decile" in column_selection:
            encoding_type = ":N"
        else:
            encoding_type = ":Q"
        
        specified_feature_to_plot = column_selection + encoding_type
        alternative_condition = 'datum.' + column_selection + " > 0"
       
        map = alt.Chart(regions).mark_geoshape(stroke="white").transform_lookup(
            lookup='properties.LSOA11Code',
            from_= alt.LookupData(wimd_data, 'lsoa_code', [column_selection,'Rural/ Urban Settlement Classification (RU) Name',"Local Authority (LA) Name", "Economic Region/ Economic Action Plan Area (EAP) Name"]),
        ).transform_filter(alt.FieldOneOfPredicate(field='properties.LSOA11Code', oneOf=lsoas_to_plot)).encode(
        tooltip=alt.Tooltip(['properties.lsoa11name:N',"Local Authority (LA) Name:N","Rural/ Urban Settlement Classification (RU) Name:N"]),
        color=alt.condition(alternative_condition, specified_feature_to_plot, alt.value("lightgrey"))
        ).properties(
            width=1000,
            height=800
        ).configure_view(strokeWidth=0)



        st.altair_chart(map, use_container_width=False)
    with st.expander("Dataframe"):
        #selections_for_dataframe = st.multiselect()
        st.dataframe(wimd_data)

pwd = st.sidebar.text_input("Password:", type='password')
if pwd == st.secrets["PASSWORD"]:
    streamlit_wimd()
elif pwd == '':
    pass
else:
    st.error('Password incorrect. Please try again.')

