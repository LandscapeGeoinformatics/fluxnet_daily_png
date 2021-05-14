# Fluxnet tower HF data graphs

![](https://storage.googleapis.com/geo-assets/fluxnet/today_and_yesterday_Palo_ClearCut_PaloclearHFdata_CO2_dry_Avg.png)

We use `papermill` to run the template Jupyter notebook with parameters for a scripted generation of HF EDI tower data graphs for visual inspection.

Interesting side notes:

- `Pandas` read from MS SQL
- several million datapoints, so Pandas plot with Matplotlib is slow
- so we convert to `Xarray` dataset, which adds more logic and efficiency

