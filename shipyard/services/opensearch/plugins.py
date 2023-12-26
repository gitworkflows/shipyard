from shipyard.packages import Package, package


@package(name="opensearch")
def opensearch_package() -> Package:
    from shipyard.services.opensearch.packages import opensearch_package

    return opensearch_package
