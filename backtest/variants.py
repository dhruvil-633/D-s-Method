from dataclasses import dataclass

@dataclass(frozen=True)
class Variant:
    name: str
    use_linear_sentiment: bool
    use_interaction: bool
V0 = Variant("V0_numeric", False, False)
V1 = Variant("V1_linear", True, False)
V2 = Variant("V2_interaction", False, True)
V3 = Variant("V3_full", True, True)

ALL_VARIANTS = [V0, V1, V2, V3]
