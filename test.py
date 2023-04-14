from unittest import TestCase
from photovoltaiceducation import PhotoVoltaicEducation
from datetime import datetime, timezone

from solarcalculator import SolarResult

class TestFormulas(TestCase):
    def test_power_density(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        result : float = formulas.radiant_power_density(3)
        self.assertAlmostEqual(result, 1397.6, 1)

    def test_simple_airmass(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        result : float = formulas.air_mass_approx(30)
        self.assertAlmostEqual(result, 1.1547, 4)

    def test_compelex_airmass(self) -> None:
            formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
            result : float = formulas.air_mass(30)
            self.assertAlmostEqual(result, 1.15399, 4)

    def test_all_pve(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        date : datetime = datetime(2022, 1, 25, 12, 00, 0)
        longitude : float = 144.9631
        latitude : float = -37.8136
        timezone: float = 10
        result : SolarResult = formulas.calculate(latitude, longitude, 0, date, timezone)
        self.assertAlmostEqual(result.solar_radiation, 1026.286163437431, 4) # 10% off.

    def test_intensity_direct(self) -> None:
            formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
            result : float = formulas.intensity_direct(1.5)
            self.assertAlmostEqual(result, 846, 0)

    def test_intensity_direct_elivation(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        result : float = formulas.intensity_direct_elivation(1.5, 0)
        self.assertAlmostEqual(result, 846, 0)

    def test_intensity_global(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        result : float = formulas.intensity_direct(1.5)
        total : float = formulas.intensity_global(result)
        self.assertAlmostEqual(total, 930.6, 0)

    def test_local_solar_time(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        longitude : float = 150
        timezone: float = 10
        lstm : float = formulas.local_standard_time_meridian(timezone)
        eot : float = formulas.equation_of_time(5)
        tc : float = formulas.time_correction_factor(longitude, lstm, eot)
        lst : float = formulas.local_solar_time(12.5, tc) # 12:30
        self.assertAlmostEqual(lst,12.4, 1)

    def test_tilt(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        tilt : float = 15
        latitude : float = 30
        declination : float = formulas.declination(30)
        hra : float = formulas.hour_angle(12)
        elivation : float = formulas.elivation(declination, latitude, hra)
        factor : float = formulas.tilted_surface_radiation_factor(elivation, tilt)
        self.assertAlmostEqual(factor,0.8383, 4)

    def test_orientation(self) -> None:
        formulas : PhotoVoltaicEducation = PhotoVoltaicEducation()
        tilt : float = 15
        latitude : float = 30
        declination : float = formulas.declination(30)
        hra : float = formulas.hour_angle(12)
        elivation : float = formulas.elivation(declination, latitude, hra)
        factor : float = formulas.orientation_tilt_factor(elivation, 90, tilt, 90)
        self.assertAlmostEqual(factor,0.8383, 4)
