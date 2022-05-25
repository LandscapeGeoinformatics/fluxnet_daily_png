#!/bin/bash

export CONDA_EXE=/opt/anaconda/miniconda/bin/conda
export GDAL_DATA=/opt/anaconda/miniconda/envs/geopy2020/share/gdal
export CONDA_PREFIX=/opt/anaconda/miniconda/envs/geopy2020
export CONDA_PYTHON_EXE=/opt/anaconda/miniconda/bin/python
export CONDA_PROMPT_MODIFIER=(geopy2020)
export PATH=/opt/anaconda/miniconda/envs/geopy2020/bin:/opt/anaconda/miniconda/condabin:$PATH
export CONDA_DEFAULT_ENV=geopy2020

cd /home/DOMENIS.UT.EE/kmoch/dev/build/fluxnet_daily_png

SHORT_LONG=1

if [ "$1" = "long" ]; then
    SHORT_LONG=2
fi

# https://cloud.google.com/storage/docs/metadata#cache-control
CACHE_DIRECTIVE="Cache-Control:public, max-age=600"

# days_back = 3
# include_now = 0
# parameter = "H2O_dry_Avg"
# station_table = "Soontaga_HFdata"
# filename_def = 'three_days_back'

# Soontaga
for param in w_Avg T_Avg CO2_dry_Avg H2O_dry_Avg; do
    station=Soontaga_HFdata

    if [ $SHORT_LONG = 2 ]; then
        /opt/anaconda/miniconda/envs/geopy2020/bin/papermill fluxnet_scripted.ipynb - -p days_back 3 -p include_now 0 -p parameter ${param} -p station_table ${station} -p filename_def three_days_back_${station}_${param}

        /usr/bin/gsutil -h "$CACHE_DIRECTIVE" cp images/three_days_back_${station}_${param}.png gs://geo-assets/fluxnet/three_days_back_${station}_${param}.png
    else

        /opt/anaconda/miniconda/envs/geopy2020/bin/papermill fluxnet_scripted.ipynb - -p days_back 1 -p include_now 1 -p parameter ${param} -p station_table ${station} -p filename_def today_and_yesterday_${station}_${param}

        /usr/bin/gsutil -h "$CACHE_DIRECTIVE" cp images/today_and_yesterday_${station}_${param}.png gs://geo-assets/fluxnet/today_and_yesterday_${station}_${param}.png
    fi

done

# Agali_II_FluxHFdata - WindSpeed_Z Wind_Temperature AD_CH4 AD_N20  CO2_DryMoleFractions  H2O_DryMoleFractions
for param in WindSpeed_Z Wind_Temperature AD_CH4 AD_N20 CO2_DryMoleFractions H2O_DryMoleFractions; do
    station=Agali_II_FluxHFdata

    if [ $SHORT_LONG = 2 ]; then
        /opt/anaconda/miniconda/envs/geopy2020/bin/papermill fluxnet_scripted.ipynb - -p days_back 3 -p include_now 0 -p parameter ${param} -p station_table ${station} -p filename_def three_days_back_${station}_${param}

        /usr/bin/gsutil -h "$CACHE_DIRECTIVE" cp images/three_days_back_${station}_${param}.png gs://geo-assets/fluxnet/three_days_back_${station}_${param}.png
    else

        /opt/anaconda/miniconda/envs/geopy2020/bin/papermill fluxnet_scripted.ipynb - -p days_back 1 -p include_now 1 -p parameter ${param} -p station_table ${station} -p filename_def today_and_yesterday_${station}_${param}

        /usr/bin/gsutil -h "$CACHE_DIRECTIVE" cp images/today_and_yesterday_${station}_${param}.png gs://geo-assets/fluxnet/today_and_yesterday_${station}_${param}.png
    fi

done

# Palo_Forest_II_FluxHFdata - WindSpeed_Z  Wind_Temperature CO2  H2O
for param in WindSpeed_Z Wind_Temperature CO2 H2O; do
    station=Palo_Forest_II_FluxHFdata

    if [ $SHORT_LONG = 2 ]; then
        /opt/anaconda/miniconda/envs/geopy2020/bin/papermill fluxnet_scripted.ipynb - -p days_back 3 -p include_now 0 -p parameter ${param} -p station_table ${station} -p filename_def three_days_back_${station}_${param}

        /usr/bin/gsutil -h "$CACHE_DIRECTIVE" cp images/three_days_back_${station}_${param}.png gs://geo-assets/fluxnet/three_days_back_${station}_${param}.png
    else

        /opt/anaconda/miniconda/envs/geopy2020/bin/papermill fluxnet_scripted.ipynb - -p days_back 1 -p include_now 1 -p parameter ${param} -p station_table ${station} -p filename_def today_and_yesterday_${station}_${param}

        /usr/bin/gsutil -h "$CACHE_DIRECTIVE" cp images/today_and_yesterday_${station}_${param}.png gs://geo-assets/fluxnet/today_and_yesterday_${station}_${param}.png
    fi

done

# Palo_ClearCut_PaloclearHFdata  -  CO2_dry_Avg  H2O_dry_Avg   Aux_3_Avg  Aux_4_Avg
for param in CO2_dry_Avg H2O_dry_Avg Aux_3_Avg Aux_4_Avg; do
    station=Palo_ClearCut_PaloclearHFdata

    if [ $SHORT_LONG = 2 ]; then
        /opt/anaconda/miniconda/envs/geopy2020/bin/papermill fluxnet_scripted.ipynb - -p days_back 3 -p include_now 0 -p parameter ${param} -p station_table ${station} -p filename_def three_days_back_${station}_${param}

        /usr/bin/gsutil -h "$CACHE_DIRECTIVE" cp images/three_days_back_${station}_${param}.png gs://geo-assets/fluxnet/three_days_back_${station}_${param}.png
    else

        /opt/anaconda/miniconda/envs/geopy2020/bin/papermill fluxnet_scripted.ipynb - -p days_back 1 -p include_now 1 -p parameter ${param} -p station_table ${station} -p filename_def today_and_yesterday_${station}_${param}

        /usr/bin/gsutil cp images/today_and_yesterday_${station}_${param}.png gs://geo-assets/fluxnet/today_and_yesterday_${station}_${param}.png
    fi

done
