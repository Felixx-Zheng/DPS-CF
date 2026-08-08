"""
Compact reference definition of the DPS-CF fusion architecture.

This file intentionally omits the internal CNN-LSTM backbone implementation,
training loop, checkpoint handling, and data pipeline. A compatible backbone
must expose ``extract_features(iq) -> Tensor[B, 128]``.
"""

from __future__ import annotations

from typing import Protocol
import torch
from torch import nn


class BackboneInterface(Protocol):
    """Minimal interface expected by DPS-CF."""

    def extract_features(self, iq: torch.Tensor) -> torch.Tensor:
        ...


class PriorProjection(nn.Module):
    def __init__(self, prior_dim: int = 24) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(prior_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.25),
            nn.Linear(64, 64),
            nn.ReLU(),
        )

    def forward(self, prior: torch.Tensor) -> torch.Tensor:
        return self.net(prior)


class ScalarGate(nn.Module):
    def __init__(self, prior_dim: int = 24) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(prior_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid(),
        )

    def forward(self, prior: torch.Tensor) -> torch.Tensor:
        return self.net(prior)


class FusionClassifier(nn.Module):
    def __init__(self, num_classes: int) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(192, 256),
            nn.ReLU(),
            nn.Dropout(0.30),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.30),
            nn.Linear(128, num_classes),
        )

    def forward(self, fused: torch.Tensor) -> torch.Tensor:
        return self.net(fused)


class DPSCF(nn.Module):
    """
    Method-level reference implementation.

    The supplied backbone is expected to return a 128-D feature vector.
    Backbone construction and pretrained weights are deliberately not included
    in this repository.
    """

    def __init__(
        self,
        backbone: nn.Module,
        num_classes: int,
        prior_dim: int = 24,
    ) -> None:
        super().__init__()
        self.backbone = backbone
        self.projection = PriorProjection(prior_dim)
        self.gate = ScalarGate(prior_dim)
        self.classifier = FusionClassifier(num_classes)

    def freeze_backbone(self) -> None:
        for parameter in self.backbone.parameters():
            parameter.requires_grad = False
        self.backbone.eval()

    def forward(
        self,
        iq: torch.Tensor,
        selected_prior: torch.Tensor,
        return_gate: bool = False,
    ):
        # A compatible internal backbone must implement extract_features().
        with torch.no_grad():
            h = self.backbone.extract_features(iq)

        e_p = self.projection(selected_prior)
        alpha = self.gate(selected_prior)
        z = torch.cat([h, alpha * e_p], dim=1)
        logits = self.classifier(z)

        if return_gate:
            return logits, alpha.squeeze(1)
        return logits
