# Common 98-dimensional Candidate Prior Pool

Both datasets use the same 98-dimensional candidate pool. Indices below are **0-based** and match the indices stored in the metadata JSON files.

The pool is ordered as:

```text
0–37   Base physical/statistical descriptors (38)
38–50  HOC-related descriptors (13)
51–97  Extended descriptors (47)
```

The names below follow the reference extraction code used to construct the shared pool. Numerical safeguards used by the internal production extractor are omitted from this documentation unless they are part of the descriptor definition.

## Dimension-by-dimension definitions

| Index | Name | Category | Definition |
|---:|---|---|---|
| 0 | `env_stat_00` | Envelope | Mean envelope amplitude: mean(|z|). |
| 1 | `env_stat_01` | Envelope | Standard deviation of the envelope amplitude. |
| 2 | `env_stat_02` | Envelope | Peak-to-mean envelope ratio: max(|z|) / mean(|z|). |
| 3 | `env_stat_03` | Envelope | Excess kurtosis of the mean-normalized envelope. |
| 4 | `env_stat_04` | Envelope | Skewness-like third central moment of the mean-normalized envelope. |
| 5 | `env_stat_05` | Envelope | Envelope coefficient of variation: std(|z|) / mean(|z|). |
| 6 | `env_stat_06` | Envelope | Standard deviation of the first difference of the envelope. |
| 7 | `env_stat_07` | Envelope | Zero-crossing rate of the mean-centered envelope. |
| 8 | `env_stat_08` | Envelope | Minimum-to-mean envelope ratio: min(|z|) / mean(|z|). |
| 9 | `env_stat_09` | I/Q balance | I/Q power ratio: mean(I^2) / mean(Q^2). |
| 10 | `inst_freq_00` | Instantaneous frequency | Mean wrapped phase increment Δφ. |
| 11 | `inst_freq_01` | Instantaneous frequency | Standard deviation of wrapped phase increment Δφ. |
| 12 | `inst_freq_02` | Instantaneous frequency | Maximum absolute wrapped phase increment. |
| 13 | `inst_freq_03` | Instantaneous frequency | Standard deviation of the first difference of wrapped phase increments. |
| 14 | `inst_freq_04` | Instantaneous frequency | Skewness of wrapped phase increments. |
| 15 | `inst_freq_05` | Instantaneous frequency | Excess kurtosis of wrapped phase increments. |
| 16 | `spectrum_shape_00` | Spectrum shape | Upper-sideband energy ratio around the dominant positive-frequency spectral peak. |
| 17 | `spectrum_shape_01` | Spectrum shape | Cosine similarity between upper and lower spectral neighborhoods around the dominant peak. |
| 18 | `spectrum_shape_02` | Spectrum shape | Dominant spectral magnitude divided by the mean positive-frequency magnitude. |
| 19 | `spectrum_shape_03` | Spectrum shape | Dominant spectral magnitude divided by the median positive-frequency magnitude. |
| 20 | `spectrum_shape_04` | Spectrum shape | Entropy of the normalized positive-frequency spectral magnitude. |
| 21 | `spectrum_shape_05` | Spectrum shape | Gini coefficient of the normalized positive-frequency spectral magnitude. |
| 22 | `spectrum_shape_06` | Spectrum shape | Concentration of spectral magnitude in sidebands around the dominant peak. |
| 23 | `spectrum_shape_07` | Spectrum shape | Absolute deviation of the sideband symmetry ratio from 0.5. |
| 24 | `m_power_00` | M-power | Peak-to-mean ratio of the FFT magnitude of the unit-envelope signal raised to power M=2. |
| 25 | `m_power_01` | M-power | Peak-to-sum ratio of the FFT magnitude of the unit-envelope signal raised to power M=2. |
| 26 | `m_power_02` | M-power | Peak-to-mean ratio of the FFT magnitude of the unit-envelope signal raised to power M=4. |
| 27 | `m_power_03` | M-power | Peak-to-sum ratio of the FFT magnitude of the unit-envelope signal raised to power M=4. |
| 28 | `m_power_04` | M-power | Peak-to-mean ratio of the FFT magnitude of the unit-envelope signal raised to power M=8. |
| 29 | `m_power_05` | M-power | Peak-to-sum ratio of the FFT magnitude of the unit-envelope signal raised to power M=8. |
| 30 | `m_power_06` | M-power | Peak-to-mean ratio of the FFT magnitude of the unit-envelope signal raised to power M=16. |
| 31 | `m_power_07` | M-power | Peak-to-sum ratio of the FFT magnitude of the unit-envelope signal raised to power M=16. |
| 32 | `m_power_08` | M-power | Peak-to-mean ratio of the FFT magnitude of the unit-envelope signal raised to power M=32. |
| 33 | `m_power_09` | M-power | Peak-to-sum ratio of the FFT magnitude of the unit-envelope signal raised to power M=32. |
| 34 | `diff_phase_00` | Differential phase | Mean wrapped differential phase. |
| 35 | `diff_phase_01` | Differential phase | Standard deviation of wrapped differential phase. |
| 36 | `diff_phase_02` | Differential phase | Fraction of differential-phase samples with |Δφ| < 0.3 rad. |
| 37 | `diff_phase_03` | Differential phase | Entropy-like statistic derived from softmax-normalized differential phase. |
| 38 | `hoc_00` | HOC/statistical | |C20|, with C20 = M20. |
| 39 | `hoc_01` | HOC/statistical | |C21|, with C21 = M21. |
| 40 | `hoc_02` | HOC/statistical | |C40|, where C40 = M40 - 3 M20^2. |
| 41 | `hoc_03` | HOC/statistical | |C42|, where C42 = M42 - |M20|^2 - 2 M21^2. |
| 42 | `hoc_04` | HOC/statistical | |M42|. |
| 43 | `hoc_05` | HOC/statistical | |M60|. |
| 44 | `hoc_06` | HOC/statistical | |C63|, where C63 = M63 - 9 M42 M21 + 12 M21^3. |
| 45 | `hoc_07` | HOC/statistical | |M80|. |
| 46 | `hoc_08` | HOC/statistical | |M84|. |
| 47 | `hoc_09` | HOC/statistical | |C80|, with the eighth-order cumulant expression used in the reference extractor. |
| 48 | `hoc_10` | HOC/statistical | Standard deviation of the power-normalized envelope. |
| 49 | `hoc_11` | HOC/statistical | Maximum value of the power-normalized envelope. |
| 50 | `hoc_12` | HOC/statistical | Maximum centered periodogram value: (1/N) max |FFT(x - mean(x))|^2. |
| 51 | `env_extra_00` | Envelope extra | Mean envelope amplitude. |
| 52 | `env_extra_01` | Envelope extra | Standard deviation of envelope amplitude. |
| 53 | `env_extra_02` | Envelope extra | Skewness of envelope amplitude. |
| 54 | `env_extra_03` | Envelope extra | Excess kurtosis of envelope amplitude. |
| 55 | `env_extra_04` | Envelope extra | Root-mean-square envelope amplitude. |
| 56 | `env_extra_05` | Envelope extra | Maximum instantaneous power divided by mean instantaneous power. |
| 57 | `env_extra_06` | Envelope extra | Maximum envelope amplitude divided by RMS envelope amplitude. |
| 58 | `env_extra_07` | Envelope extra | 75th-to-25th percentile envelope ratio. |
| 59 | `env_extra_08` | Envelope extra | 32-bin histogram entropy of envelope amplitude. |
| 60 | `env_extra_09` | Envelope extra | Mean absolute first difference of envelope amplitude. |
| 61 | `env_extra_10` | Envelope extra | Standard deviation of the first difference of envelope amplitude. |
| 62 | `env_extra_11` | Envelope extra | Excess kurtosis of the first difference of envelope amplitude. |
| 63 | `phase_extra_00` | Phase extra | Mean unwrapped phase difference. |
| 64 | `phase_extra_01` | Phase extra | Standard deviation of unwrapped phase difference. |
| 65 | `phase_extra_02` | Phase extra | Skewness of unwrapped phase difference. |
| 66 | `phase_extra_03` | Phase extra | Excess kurtosis of unwrapped phase difference. |
| 67 | `phase_extra_04` | Phase extra | Mean absolute unwrapped phase difference. |
| 68 | `phase_extra_05` | Phase extra | Circular variance: 1 - |mean(exp(j·phase))|. |
| 69 | `phase_extra_06` | Phase extra | 32-bin histogram entropy of phase wrapped to [0, 2π). |
| 70 | `phase_extra_07` | Phase extra | Phase-jump rate: fraction of |Δphase| > π/4. |
| 71 | `ifreq_extra_00` | Instantaneous-frequency extra | Mean of Δphase/(2π). |
| 72 | `ifreq_extra_01` | Instantaneous-frequency extra | Standard deviation of Δphase/(2π). |
| 73 | `ifreq_extra_02` | Instantaneous-frequency extra | Skewness of Δphase/(2π). |
| 74 | `ifreq_extra_03` | Instantaneous-frequency extra | Excess kurtosis of Δphase/(2π). |
| 75 | `ifreq_extra_04` | Instantaneous-frequency extra | Mean absolute first difference of instantaneous frequency. |
| 76 | `ifreq_extra_05` | Instantaneous-frequency extra | 90th-to-10th percentile range of instantaneous frequency. |
| 77 | `ifreq_extra_06` | Instantaneous-frequency extra | Maximum absolute instantaneous frequency. |
| 78 | `ifreq_extra_07` | Instantaneous-frequency extra | Sign-change rate of instantaneous frequency. |
| 79 | `spec_extra_00` | Spectrum extra | Spectral centroid on the normalized positive-frequency axis. |
| 80 | `spec_extra_01` | Spectrum extra | Spectral spread around the centroid. |
| 81 | `spec_extra_02` | Spectrum extra | Spectral flatness: geometric mean / arithmetic mean of spectral magnitude. |
| 82 | `spec_extra_03` | Spectrum extra | Entropy of normalized spectral magnitude. |
| 83 | `spec_extra_04` | Spectrum extra | 85% spectral roll-off location. |
| 84 | `spec_extra_05` | Spectrum extra | 95% spectral roll-off location. |
| 85 | `spec_extra_06` | Spectrum extra | Peak-to-mean spectral magnitude ratio. |
| 86 | `spec_extra_07` | Spectrum extra | Largest-to-second-largest spectral magnitude ratio. |
| 87 | `spec_extra_08` | Spectrum extra | Low-half to high-half positive-spectrum magnitude ratio. |
| 88 | `spec_extra_09` | Spectrum extra | Excess kurtosis of positive-frequency spectral magnitude. |
| 89 | `corr_extra_00` | Correlation extra | Absolute normalized autocorrelation at lag 1. |
| 90 | `corr_extra_01` | Correlation extra | Absolute normalized autocorrelation at lag 2. |
| 91 | `corr_extra_02` | Correlation extra | Absolute normalized autocorrelation at lag 4. |
| 92 | `corr_extra_03` | Correlation extra | Absolute normalized autocorrelation at lag 8. |
| 93 | `corr_extra_04` | Correlation extra | Absolute normalized autocorrelation at lag 16. |
| 94 | `corr_extra_05` | Correlation extra | Maximum absolute normalized autocorrelation over lags 1–32. |
| 95 | `corr_extra_06` | Correlation extra | Mean absolute normalized autocorrelation over lags 1–32. |
| 96 | `corr_extra_07` | Correlation extra | Ratio of maximum to mean absolute normalized autocorrelation over lags 1–32. |
| 97 | `corr_extra_08` | Correlation extra | Sum of zero-crossing rates of the real and imaginary components after complex-mean removal. |

## Higher-order/statistical definitions

For the 13-dimensional HOC/statistical block, the complex sequence is first normalized by its mean signal power. The reference block uses the moments

\[M_{20}=E[x^2],\quad M_{21}=E[|x|^2],\quad M_{40}=E[x^4],\quad M_{42}=E[|x|^4],\]

\[M_{60}=E[x^6],\quad M_{63}=E[|x|^6],\quad M_{80}=E[x^8],\quad M_{84}=E[|x|^8].\]

The cumulant-like quantities used by the reference extractor include:

\[C_{40}=M_{40}-3M_{20}^2,\]

\[C_{42}=M_{42}-|M_{20}|^2-2M_{21}^2,\]

\[C_{63}=M_{63}-9M_{42}M_{21}+12M_{21}^3,\]

\[C_{80}=M_{80}-35M_{40}^2-28M_{60}M_{20}+420M_{40}M_{20}^2-630M_{20}^4.\]

The remaining HOC/statistical dimensions are envelope statistics of the power-normalized sequence and the maximum centered periodogram value.

## Pool composition

| Group | Size |
|---|---:|
| Envelope/base statistics | 10 |
| Instantaneous-frequency/base statistics | 6 |
| Spectrum-shape statistics | 8 |
| M-power statistics | 10 |
| Differential-phase statistics | 4 |
| HOC/statistical block | 13 |
| Extended envelope statistics | 12 |
| Extended phase statistics | 8 |
| Extended instantaneous-frequency statistics | 8 |
| Extended spectrum statistics | 10 |
| Extended correlation statistics | 9 |
| **Total** | **98** |
