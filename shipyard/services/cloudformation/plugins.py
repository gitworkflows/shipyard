from shipyard.packages import Package, package


@package(name="cloudformation-libs")
def cloudformation_package() -> Package:
    from shipyard.services.cloudformation.packages import cloudformation_package

    return cloudformation_package
