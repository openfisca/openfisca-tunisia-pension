import math
from openfisca_core.simulations import SimulationBuilder
from openfisca_tunisia_pension import TunisiaPensionTaxBenefitSystem

def test_indemnites_familiales_1_enfant():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "parent_1": {
                    "nombre_enfants_charge": {"2024-01": 1}
                }
            }
        }
    )

    res = sim.calculate("indemnites_familiales", "2024-01")[0]
    print(f"Calculated 1 enfant: {res}")
    assert math.isclose(res, 7.320, abs_tol=1e-5)
    print("Test IF 1 enfant passed!")

def test_indemnites_familiales_3_enfants():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "parent_3": {
                    "nombre_enfants_charge": {"2024-01": 3}
                }
            }
        }
    )

    # 3 children: 7.320 + 6.507 + 5.693 = 19.520 D
    res = sim.calculate("indemnites_familiales", "2024-01")[0]
    expected = 7.320 + 6.507 + 5.693
    assert math.isclose(res, expected, abs_tol=1e-5)
    print("Test IF 3 enfants passed!")

def test_iru_1_enfant():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "retraite_solo": {
                    "nombre_enfants_charge": {"2024-01": 1},
                    "conjoint_sans_revenu": {"2024-01": True}
                }
            }
        }
    )

    res = sim.calculate("indemnite_revenu_unique", "2024-01")[0]
    assert math.isclose(res, 3.125, abs_tol=1e-5)
    print("Test IRU 1 enfant passed!")

def test_iru_2_enfants_mere_divorcee():
    system = TunisiaPensionTaxBenefitSystem()
    sim = SimulationBuilder().build_from_dict(
        system,
        {
            "individus": {
                "mere_divorcee": {
                    "nombre_enfants_charge": {"2024-01": 2},
                    "mere_divorcee_garde_enfants": {"2024-01": True}
                }
            }
        }
    )

    res = sim.calculate("indemnite_revenu_unique", "2024-01")[0]
    assert math.isclose(res, 6.250, abs_tol=1e-5)
    print("Test IRU 2 enfants mere divorcee passed!")

if __name__ == "__main__":
    test_indemnites_familiales_1_enfant()
    test_indemnites_familiales_3_enfants()
    test_iru_1_enfant()
    test_iru_2_enfants_mere_divorcee()
