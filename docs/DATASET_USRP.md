# Self-built USRP OTA Dataset

This document records the acquisition, partitioning, and SNR-construction protocol used for the self-built over-the-air (OTA) dataset in the DPS-CF experiments.

## Acquisition setup

The dataset was collected in one laboratory acquisition round using two USRP B210 devices as transmitter and receiver.

| Item | Setting |
|---|---|
| Transmitter / receiver | USRP B210 / USRP B210 |
| Environment | Short-range laboratory |
| TX/RX distance | approximately 10 m |
| TX/RX position | fixed during acquisition |
| Channel condition | approximately static during the acquisition round |
| TX/RX gain | fixed during acquisition |
| Center frequency | 4 GHz |
| Master-clock frequency | 40 MHz |
| Baseband sampling rate | 200 kHz |
| Samples per raw acquisition frame | 8192 |
| Raw frames per modulation class | 250 |
| Model input length | 1024 |

The 13 modulation classes are:

`ASK, BPSK, QPSK, 8PSK, 16QAM, 32QAM, 64QAM, AM, FM, 2FSK, 4FSK, GMSK, OFDM`.

A new random baseband symbol sequence is generated for each raw frame; different raw frames do not repeatedly transmit one identical fixed sequence.

## Frame-level partitioning

Partitioning is performed **before segmentation and AWGN augmentation**.

The construction order is:

```text
8192-sample raw acquisition frames
            |
            +-- training portion
            |       +-- training subset
            |       +-- validation subset
            |
            +-- fixed test set
                    |
          8 non-overlapping segments
             of 1024 samples each
                    |
         subset-internal AWGN generation
```

The training/test assignment is made at the original 8192-sample acquisition-frame level. Ten percent of the training portion is then assigned to validation data, also at the raw-frame level.

Each 8192-sample frame is split into eight **non-overlapping** 1024-sample segments. All segments and all SNR-augmented versions derived from one raw frame remain in the same training, validation, or test subset.

After segmentation and SNR augmentation, the complete dataset contains 416,000 examples. The training portion contains 332,800 examples before the internal training/validation split, and the fixed test set contains 83,200 examples.

## Hardware-noise estimation

The original OTA recordings already contain receiver noise. The augmentation procedure therefore accounts for the measured hardware-noise component rather than treating the raw waveform as noise-free.

For the same fixed acquisition system, local window energy is calculated as

$$
E_k = \frac{1}{L}\sum_{n=k}^{k+L-1}|x[n]|^2.
$$

Low-energy windows corresponding to noise-only intervals are used to estimate the receiver-noise power. The resulting value used in the experiment is

$$
P_{n,\mathrm{hw}} = 3.1149 \times 10^{-6}.
$$

This value is measured from the acquisition system rather than introduced as an empirical constant.

For a complex received sequence $c[n] = I[n] + jQ[n]$,

$$
P_{\mathrm{raw}} = \frac{1}{N}\sum_n |c[n]|^2,
$$

and the effective signal power is estimated as

$$
P_s = \max\left(P_{\mathrm{raw}} - P_{n,\mathrm{hw}},\,10^{-10}\right).
$$

The corresponding estimated raw SNR is

$$
\mathrm{SNR}_{\mathrm{raw}}
=
10\log_{10}\left(\frac{P_s}{P_{n,\mathrm{hw}}}\right).
$$

The raw acquisition frames used in the experiments were checked to have estimated SNR values above 20 dB.

## Controlled AWGN construction

The target SNR levels are

```text
-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20 dB
```

For target SNR $\gamma_{\mathrm{dB}}$, the required **total** noise power is

$$
P_{n,\mathrm{target}}
=
\frac{P_s}{10^{\gamma_{\mathrm{dB}}/10}}.
$$

Because the recorded OTA waveform already contains the measured hardware noise, only the additional noise power required to reach the target is added:

$$
P_{n,\mathrm{add}}
=
\max\left(
P_{n,\mathrm{target}} - P_{n,\mathrm{hw}},
0
\right).
$$

Complex Gaussian noise is generated as

$$
w[n]
=
\sqrt{\frac{P_{n,\mathrm{add}}}{2}}
\left(u[n] + jv[n]\right),
\qquad
u[n],v[n] \sim \mathcal{N}(0,1),
$$

and the augmented signal is

$$
c_{\mathrm{aug}}[n] = c[n] + w[n].
$$

Thus, the target SNR construction combines the measured receiver-noise component already present in the OTA recording with the additional software-generated AWGN.

## Evaluation scope

Training, validation, and test frames come from the same acquisition round, fixed TX/RX geometry, and approximately static channel condition. The USRP experiment therefore evaluates frame-level independent samples under controlled SNR variation within one acquisition environment. It is not a cross-session, cross-device, cross-location, or dynamic-channel generalization benchmark.

## Data availability

The self-built USRP OTA dataset is available from the authors upon reasonable request.
