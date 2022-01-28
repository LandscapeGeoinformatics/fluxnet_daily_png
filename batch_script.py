import os
import sys
import subprocess
import pprint

import pyodbc
import get_conf
from datetime import timedelta, date, datetime
import pandas as pd
import os
import xarray as xr
import dask
import matplotlib.pyplot as plt

from xarray.coding.times import decode_cf_datetime


def format_date(x, pos=None):
    calendar = "standard"
    units = "days since 1970-01-01 00:00:00"

    np_ts = decode_cf_datetime([x], units, calendar=calendar, use_cftime=None)[0]
    return pd.Timestamp(np_ts).strftime("%d.%b %Hh")


def actual_plot(
    days_back=1,
    include_now=1,
    parameter="CO2_dry_Avg",
    station_table="Palo_ClearCut_PaloclearHFdata",
    filename_def="today_and_yesterday",
    log=False,
):

    conn = pyodbc.connect(get_conf.conn_string())

    d3 = timedelta(days=days_back)

    normal_shift = 1 if include_now < 1 else 0

    dt_today = date.today() - timedelta(days=normal_shift)

    a = (
        dt_today.strftime("%Y-%m-%d 23:59:59")
        if include_now <= 0
        else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    b = (dt_today - d3).strftime("%Y-%m-%d 00:00:00")

    a_str = a.replace(" ", "_").replace(":", ".")
    b_str = b.replace(" ", "_").replace(":", ".")

    filename_pref = (
        f"{parameter}_{station_table}_{b_str}_{a_str}"
        if len(filename_def) <= 0
        else f"{filename_def}"
    )

    outfilename = f"{filename_pref}.png"

    if log == True:
        print(a)
        print(b)
        print(outfilename)

    param = parameter
    table = station_table
    from_ts = b
    to_ts = a

    sql_query = f"SELECT {param}, TmStamp FROM {table} WHERE TmStamp >= '{from_ts}' AND TmStamp <= '{to_ts}'"

    if log == True:
        print(sql_query)

    df = (
        pd.read_sql_query(
            sql_query, conn, coerce_float=True, parse_dates=["TmStamp"], chunksize=None
        )
        .rename(columns={"TmStamp": "time"})
        .set_index("time")
    )

    if len(df) <= 0:
        error_msg = f"sql query returned zero elements - must skip ({sql_query})"
        if log == True:
            print(error_msg)
        return (1, error_msg)

    qr = df.quantile([0.01, 0.99])
    qr_min = qr.iloc[0, 0]
    qr_max = qr.iloc[1, 0]

    iqrx = qr_max - qr_min

    vmin = qr_min - iqrx * 1.5
    vmax = qr_max + iqrx * 1.5

    if log == True:
        print(f"vmin {vmin} vmax {vmax}")

    dset = xr.Dataset.from_dataframe(df)

    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_ylim(vmin, vmax)
    ax.xaxis.set_major_formatter(format_date)
    dset[parameter].plot(ax=ax, color="black", lw=0.2)

    fig.autofmt_xdate()
    plt.title(f"{station_table}: {param} | {from_ts} - {to_ts}", fontsize=18)

    plt.savefig(os.path.join("images", outfilename))

    return (0, f"finished plotting {outfilename} at {datetime.now().isoformat()}")


def gen_plot(SHORT_LONG, param, station, log=False):
    days_back = 1
    include_now = 1
    parameter = param
    station_table = station
    filename_def = f"today_and_yesterday_{station}_{param}"

    if SHORT_LONG == 2:
        days_back = 3
        include_now = 0
        parameter = param
        station_table = station
        filename_def = f"three_days_back_{station}_{param}"

    try:
        p = actual_plot(
            days_back, include_now, parameter, station_table, filename_def, log=log
        )
        return (p[0], "", p[1])
    except Exception as ex:
        return (
            1,
            str(ex),
            ", ".join(
                [
                    str(p)
                    for p in [
                        days_back,
                        include_now,
                        parameter,
                        station_table,
                        filename_def,
                    ]
                ]
            ),
        )


def gs_upload(SHORT_LONG, param, station, CACHE_DIRECTIVE, log=False):
    outfile = os.path.join("images", f"today_and_yesterday_{station}_{param}.png")
    exec_params = f"gsutil -h {CACHE_DIRECTIVE} cp {outfile} gs://geo-assets/fluxnet/today_and_yesterday_{station}_{param}.png"

    if SHORT_LONG == 2:
        outfile = os.path.join("images", f"three_days_back_{station}_{param}.png")
        exec_params = f"gsutil -h {CACHE_DIRECTIVE} cp {outfile} gs://geo-assets/fluxnet/three_days_back_{station}_{param}.png"

    if log == True:
        print(exec_params)

    proc = subprocess.run(
        exec_params.split(" "), shell=True, capture_output=True, text=True
    )
    if not proc.returncode == 0:
        return (proc.returncode, proc.stderr, exec_params)
    else:
        return (proc.returncode, proc.stdout, exec_params)


def main(stat_param, SHORT_LONG, CACHE_DIRECTIVE, log=False):

    print("starting work in main")
    results = []

    for k, v in stat_param.items():
        for param in v:
            x = gen_plot(SHORT_LONG, param=param, station=k, log=log)
            results.append(
                {
                    "param": param,
                    "station": k,
                    "SHORT_LONG": SHORT_LONG,
                    "exec": x[0],
                    "out": x[1],
                    "command": x[2],
                }
            )

            x = gs_upload(
                SHORT_LONG,
                param=param,
                station=k,
                CACHE_DIRECTIVE=CACHE_DIRECTIVE,
                log=log,
            )
            results.append(
                {
                    "param": param,
                    "station": k,
                    "SHORT_LONG": SHORT_LONG,
                    "exec": x[0],
                    "out": x[1],
                    "command": x[2],
                }
            )

    for res_d in results:
        if "out" in res_d.keys():
            if res_d["exec"] is not None and res_d["exec"] != 0:
                print(f"There was an error: ")
                print(pprint.pprint(res_d))
    return 0


if __name__ == "__main__":

    stat_param = {
        "Soontaga_HFdata": ["w_Avg", "T_Avg", "CO2_dry_Avg", "H2O_dry_Avg"],
        "Agali_II_FluxHFdata": [
            "WindSpeed_Z",
            "Wind_Temperature",
            "AD_CH4",
            "AD_N20",
            "CO2_DryMoleFractions",
            "H2O_DryMoleFractions",
        ],
        "Palo_Forest_FluxHFdata": ["WindSpeed_Z", "Wind_Temperature", "CO2", "H2O"],
        "Palo_ClearCut_PaloclearHFdata": [
            "CO2_dry_Avg",
            "H2O_dry_Avg",
            "Aux_3_Avg",
            "Aux_4_Avg",
        ],
    }

    # https://cloud.google.com/storage/docs/metadata#cache-control
    CACHE_DIRECTIVE = "Cache-Control:public,max-age=600"

    SHORT_LONG = 1
    LOG = False

    print(f"Hello work: " + ",".join(sys.argv))

    if "long" in sys.argv:
        SHORT_LONG = 2
    if "log" in sys.argv:
        LOG = True

    main(stat_param, SHORT_LONG, CACHE_DIRECTIVE, log=LOG)
