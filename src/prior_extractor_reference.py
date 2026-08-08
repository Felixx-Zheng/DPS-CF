"""
Reference interface for the common 98-dimensional DPS-CF prior pool.

The complete dimension names and mathematical/statistical definitions are
documented in ``docs/PRIOR_POOL.md``. The production extraction routines,
numerical safeguards, vectorized acceleration, and dataset integration are
intentionally not included in this public reference release.
"""

from __future__ import annotations

import numpy as np


BASE38_NAMES = (
    [f"env_stat_{i:02d}" for i in range(10)]
    + [f"inst_freq_{i:02d}" for i in range(6)]
    + [f"spectrum_shape_{i:02d}" for i in range(8)]
    + [f"m_power_{i:02d}" for i in range(10)]
    + [f"diff_phase_{i:02d}" for i in range(4)]
)

HOC13_NAMES = [f"hoc_{i:02d}" for i in range(13)]

EXTRA47_NAMES = (
    [f"env_extra_{i:02d}" for i in range(12)]
    + [f"phase_extra_{i:02d}" for i in range(8)]
    + [f"ifreq_extra_{i:02d}" for i in range(8)]
    + [f"spec_extra_{i:02d}" for i in range(10)]
    + [f"corr_extra_{i:02d}" for i in range(9)]
)

PRIOR_NAMES = BASE38_NAMES + HOC13_NAMES + EXTRA47_NAMES
assert len(PRIOR_NAMES) == 98


class PriorExtractorReference:
    """
    Organization of the shared 98-D candidate pool.

    A production implementation should return dimensions in exactly the order
    documented by PRIOR_NAMES. This repository does not provide the internal
    numerical implementation used to generate the experimental prior cache.
    """

    @property
    def feature_names(self) -> list[str]:
        return list(PRIOR_NAMES)

    def extract_base38(self, iq: np.ndarray) -> np.ndarray:
        raise NotImplementedError(
            "Production 38-D physical/statistical extraction is not included. "
            "See docs/PRIOR_POOL.md for the dimension definitions."
        )

    def extract_hoc13(self, iq: np.ndarray) -> np.ndarray:
        raise NotImplementedError(
            "Production 13-D HOC/statistical extraction is not included. "
            "See docs/PRIOR_POOL.md for the dimension definitions."
        )

    def extract_extended47(self, iq: np.ndarray) -> np.ndarray:
        raise NotImplementedError(
            "Production 47-D extended-statistics extraction is not included. "
            "See docs/PRIOR_POOL.md for the dimension definitions."
        )

    def extract(self, iq: np.ndarray) -> np.ndarray:
        base = self.extract_base38(iq)
        hoc = self.extract_hoc13(iq)
        extra = self.extract_extended47(iq)
        prior = np.concatenate([base, hoc, extra], axis=-1)

        if prior.shape[-1] != 98:
            raise ValueError(
                f"Expected 98 prior dimensions, got {prior.shape[-1]}."
            )
        return prior
