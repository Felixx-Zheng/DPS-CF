"""
Compact reference implementation of the DPS-CF multi-criteria selector.

The input prior matrix is assumed to have been constructed from training data
and standardized using training-subset statistics. Dataset loading, caching,
validation search, repeated-seed experiment orchestration, and report export
are intentionally omitted.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.linear_model import LogisticRegression


def _minmax(values: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    lo = float(values.min())
    hi = float(values.max())
    return (values - lo) / (hi - lo + eps)


@dataclass
class SelectionResult:
    indices: np.ndarray
    aggregate_score: np.ndarray
    lr_score: np.ndarray
    et_score: np.ndarray
    mi_score: np.ndarray


class MultiCriteriaSelector:
    """LR + ExtraTrees + mutual-information prior ranking."""

    def __init__(self, top_k: int = 24, random_state: int = 7) -> None:
        self.top_k = int(top_k)
        self.random_state = int(random_state)

    def fit(self, X_prior: np.ndarray, y: np.ndarray) -> SelectionResult:
        X_prior = np.asarray(X_prior, dtype=np.float64)
        y = np.asarray(y)

        lr = LogisticRegression(
            penalty="l1",
            C=0.1,
            solver="saga",
            max_iter=1200,
            random_state=self.random_state,
        )
        lr.fit(X_prior, y)
        lr_raw = np.mean(np.abs(lr.coef_), axis=0)

        et = ExtraTreesClassifier(
            n_estimators=400,
            random_state=self.random_state,
            n_jobs=-1,
        )
        et.fit(X_prior, y)
        et_raw = et.feature_importances_

        mi_raw = mutual_info_classif(
            X_prior,
            y,
            random_state=self.random_state,
        )

        lr_score = _minmax(lr_raw)
        et_score = _minmax(et_raw)
        mi_score = _minmax(mi_raw)

        aggregate = (lr_score + et_score + mi_score) / 3.0
        order = np.argsort(-aggregate)
        selected = order[: self.top_k]

        return SelectionResult(
            indices=selected,
            aggregate_score=aggregate,
            lr_score=lr_score,
            et_score=et_score,
            mi_score=mi_score,
        )
