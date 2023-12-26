from shipyard.packages import Package, package


@package(name="vosk")
def vosk_package() -> Package:
    from shipyard.services.transcribe.packages import vosk_package

    return vosk_package
