from progress.bar import FillingCirclesBar


def download_progress(resource_count):
    return FillingCirclesBar('Downloading', max=resource_count)
