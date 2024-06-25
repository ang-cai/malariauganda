import numpy
import rioxarray
import matplotlib.pyplot as plt

distances = [1.0, 2.2, 10.2] # in meters

# Subtract smooth from raw and then create a correlation graphic between covariates
for distance in distances:
    # Covariates
    lst_smooth = rioxarray.open_rasterio("Smoothed Uganda/smooth_uganda_lst_" + str(distance) + "m_2018.tif")
    rainfall_smooth = rioxarray.open_rasterio("Smoothed Uganda/smooth_uganda_rain_" + str(distance) + "m_2018.tif")
    elevation_smooth = rioxarray.open_rasterio("Smoothed Uganda/smooth_uganda_elevation_" + str(distance) + "m_2018.tif")

    lst = rioxarray.open_rasterio("Standardized Uganda/standard_uganda_LSTday_2km_2018.tif")
    rainfall = rioxarray.open_rasterio("Standardized Uganda/standard_uganda_Rainfall_CHIRPS_2km_2018.tif")
    elevation= rioxarray.open_rasterio("Standardized Uganda/standard_uganda_elevation.tif")
    
    lst = lst - lst_smooth
    rainfall = rainfall - rainfall_smooth
    elevation = elevation - elevation_smooth

    lst_values = lst.to_numpy().flatten()
    rainfall_values = rainfall.to_numpy().flatten()
    elevation_values = elevation.to_numpy().flatten()

    # Prepare matrix in style of slideshow example
    covariates = numpy.vstack((lst_values, rainfall_values, elevation_values))
    correlation_matrix = numpy.corrcoef(covariates)
    pretty_correlation_matrix = numpy.absolute(numpy.rot90(correlation_matrix))

    # Plot the correlation matrix
    fig, ax = plt.subplots(figsize=(6, 6))
    cax = ax.matshow(pretty_correlation_matrix, cmap="viridis")
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])
    ax.set_xticklabels(["LST", "Rainfall", "Elevation"], rotation=90, fontsize=16)
    ax.set_yticklabels(["Elevation", "Rainfall", "LST"], fontsize=16)
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_label_position('bottom')
    plt.title(str(-distance) + "m smooth", fontsize=20)
    plt.tight_layout()
    plt.savefig("Uganda Malaria/" + str(distance) + "m_covariates_correlation_uganda_2km_2018.png") 