# Self-built USRP OTA Dataset

This document records the data-construction protocol used for the self-built over-the-air (OTA) dataset in the DPS-CF experiments.

## Acquisition setup

The OTA dataset was collected in a short-range laboratory environment using two USRP B210 devices as the transmitter and receiver.

| Item | Setting |
|---|---|
| Transmitter | USRP B210 |
| Receiver | USRP B210 |
| Environment | Short-range laboratory |
| Center frequency | 4 GHz |
| Master-clock frequency | 40 MHz |
| Baseband sampling rate | 200 kHz |
| Samples per acquisition frame | 8192 |
| Model input length | 1024 samples |

Parameters not listed above are not specified in this repository.

## Modulation classes

The dataset contains 13 modulation classes:

1. ASK
2. BPSK
3. QPSK
4. 8PSK
5. 16QAM
6. 32QAM
7. 64QAM
8. AM
9. FM
10. 2FSK
11. 4FSK
12. GMSK
13. OFDM

## SNR construction

High-SNR OTA samples were first collected. Controlled offline additive white Gaussian noise (AWGN) was then used to construct 16 SNR levels:

```text
-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20 dB
```

The target SNR range is therefore -10 to 20 dB with a 2-dB interval.

## Frame-level partitioning

Data partitioning is performed **before segmentation and AWGN augmentation**.

The construction order is:

```text
8192-sample OTA acquisition frames
            │
            ├── training portion
            │       ├── training subset
            │       └── validation subset
            │
            └── fixed test set
                    │
              segmentation
                    │
              AWGN augmentation
```

The training/test assignment is made at the original acquisition-frame level. The training-validation partition inside the training portion is also performed at the acquisition-frame level.

Consequently, every 1024-sample segment and every AWGN-augmented variant derived from a given 8192-sample acquisition frame remains exclusively in the same subset. Samples derived from one acquisition frame are not distributed across training, validation, and test partitions.

## Dataset size

After segmentation and AWGN augmentation, the dataset contains 416,000 examples:

| Partition | Number of examples |
|---|---:|
| Training portion | 332,800 |
| Fixed test set | 83,200 |
| **Total** | **416,000** |

The training portion is further divided into training and validation subsets at the acquisition-frame level. The exact internal train/validation counts are not specified here.

## Input representation

Each model input is a two-channel I/Q sequence:

```text
shape = 2 × 1024
```

where the first channel contains the in-phase component and the second channel contains the quadrature component.

## Data availability

The self-built USRP OTA dataset is available from the authors upon reasonable request.
