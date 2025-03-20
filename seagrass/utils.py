from numerize import numerize


def get_data_size(limit=None):
    size_data = "all"
    if limit:
        size_data = numerize.numerize(limit)
    return size_data


def stringify_crs_distance(max_distance=0.01):
    # Set CRS distance for the points embedded in the target polygons
    crs_distance = max_distance * 100
    if crs_distance < 1:
        crs_distance = str(crs_distance).replace(".", "_")
    else:
        crs_distance = str(int(crs_distance))
    return crs_distance
