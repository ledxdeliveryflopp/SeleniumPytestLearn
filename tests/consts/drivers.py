from dataclasses import dataclass


class BrowserDrivers:
    drivers: dict = {"Chrome": "ChromeOptions", "Firefox": "FirefoxOptions"}


@dataclass
class DriverConst:
    browser_drivers: BrowserDrivers


drivers_const = DriverConst(BrowserDrivers())
