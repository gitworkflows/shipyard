from shipyard.packages import Package, package


@package(name="elasticsearch")
def elasticsearch_package() -> Package:
    from shipyard.services.opensearch.packages import elasticsearch_package

    return elasticsearch_package
