from shipyard.packages import Package, package


@package(name="kinesis-mock")
def kinesismock_package() -> Package:
    from shipyard.services.kinesis.packages import kinesismock_package

    return kinesismock_package
