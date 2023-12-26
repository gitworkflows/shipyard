from shipyard.packages.api import Package, package


@package(name="terraform")
def terraform_package() -> Package:
    from .terraform import terraform_package

    return terraform_package


@package(name="ffmpeg")
def ffmpeg_package() -> Package:
    from shipyard.packages.ffmpeg import ffmpeg_package

    return ffmpeg_package
