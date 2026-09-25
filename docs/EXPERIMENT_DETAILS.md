# Experiment and Reproducibility Details

This document complements the compact reference code in this repository. It records the implementation settings and controlled analyses used for the revised DPS-CF manuscript without turning the main paper into an engineering log.

The complete 98-dimensional prior definitions remain in [`PRIOR_POOL.md`](PRIOR_POOL.md). The ranked Top-24 records are stored in:

- [`../metadata/selected_priors_rml2018.json`](../metadata/selected_priors_rml2018.json)
- [`../metadata/selected_priors_usrp.json`](../metadata/selected_priors_usrp.json)

## 1. CNN+LSTM backbone and fusion head

Input shape for both datasets: $2 \times 1024$.

The CNN+LSTM backbone contains three 1-D convolutional stages followed by a two-layer unidirectional LSTM.

| Stage | Main configuration | Output after pooling |
|---|---|---:|
| Conv1 | 64 channels, kernel 8, stride 1, padding 4 | $64 \times 512$ |
| Conv2 | 64 channels, kernel 5, stride 1, padding 2 | $64 \times 256$ |
| Conv3 | 64 channels, kernel 3, stride 1, padding 1 | $64 \times 128$ |

Each convolution is followed by:

`BatchNorm -> ReLU -> MaxPool1d(kernel=2, stride=2)`.

The convolutional output is treated as a sequence of length 128 with 64 features per step. The LSTM uses two unidirectional layers, hidden size 128, and inter-layer dropout 0.3. The output of the second LSTM layer at the final time step is used as the 128-dimensional backbone representation.

For the main $k=24$ setting:

- prior projection: $24 \rightarrow 64 \rightarrow 64$, ReLU hidden activation, dropout 0.25 after the first layer;
- scalar gate: $24 \rightarrow 32 \rightarrow 1$, ReLU hidden activation and Sigmoid output;
- fused representation: $128 + 64 = 192$ dimensions;
- classifier: $192 \rightarrow 256 \rightarrow 128 \rightarrow C$, ReLU hidden activations and dropout 0.30.

The CNN+LSTM backbone is pretrained and frozen during the main fusion-stage training.

## 2. Training and validation protocol

Main optimization settings:

- optimizer: AdamW;
- initial learning rate: $10^{-3}$;
- weight decay: $10^{-4}$;
- batch size: 512;
- maximum epochs: 80;
- early-stopping patience: 10;
- label smoothing: 0.05;
- gate regularization coefficient: $10^{-3}$.

For RML2018.01A, a fixed class-SNR-stratified 50%/50% train/test split is used. Ten percent of the training portion is held out as validation data using the same class-SNR stratification.

For the self-built USRP dataset, train/test assignment and the 10% validation split are performed at the original acquisition-frame level before segmentation and AWGN augmentation.

Validation data are used for early stopping, checkpoint selection, hyperparameter selection, and selection of $k$. The test set is used only for final evaluation.

The main reported neural-network results use five training seeds. The dataset split and the final Top-24 indices are fixed across these five runs; only neural-network training randomness changes.

## 3. SNR-weighted training

The same SNR-weighting rule is applied to DPS-CF and the external baselines.

$$
\gamma_{\min} = -10\ \mathrm{dB},
\qquad
\gamma_{\max} = 20\ \mathrm{dB},
\qquad
\rho = 0.5.
$$

Samples inside $[-10,20]$ dB use unit weight and samples outside this interval use relative weight $\rho$. This weighting is applied only to the neural-network training loss and does not participate in LR, ET, or MI scoring.

All USRP SNR levels lie inside $[-10,20]$ dB, so all USRP training samples receive unit weight.

## 4. Multi-criteria selector

The reference selector is implemented in [`../src/selector.py`](../src/selector.py).

All 98 candidate-prior dimensions are standardized using statistics estimated from the training subset before selector fitting.

### Sparse logistic regression

- L1 penalty;
- $C=0.1$;
- SAGA solver;
- maximum iterations: 1200;
- feature score: mean absolute coefficient magnitude across classes.

### ExtraTrees

- 400 trees;
- `class_weight="balanced_subsample"` in the reported experiment;
- feature score: impurity-based feature importance;
- selector random state fixed according to the experiment run;
- remaining tree settings follow the implementation defaults.

### Mutual information

- `sklearn.feature_selection.mutual_info_classif`;
- continuous candidate-prior dimensions and discrete modulation labels;
- `n_neighbors=3`;
- random state fixed according to the experiment run.

### Min-max normalization and equal aggregation

For criterion $q$, let $s_j^{(q)}$ be the raw score of candidate prior $j$. Each criterion is independently normalized by

$$
\widetilde{s}_j^{(q)}
=
\frac{
s_j^{(q)} - \min_l s_l^{(q)}
}{
\max_l s_l^{(q)} - \min_l s_l^{(q)} + \epsilon
}.
$$

The final score is

$$
S_j
=
\frac{1}{3}
\sum_{q \in \{\mathrm{LR},\mathrm{ET},\mathrm{MI}\}}
\widetilde{s}_j^{(q)}.
$$

Candidates are sorted by $S_j$ in descending order and the first $k=24$ dimensions are retained.

Selection is performed independently using the training data of each dataset. Once the Top-24 indices are fixed, LR, ET, MI, and ranking are not executed during online neural-network inference.

## 5. Final Top-24 records and unified categories

The full rank, zero-based index, feature name, and implementation-level category for every selected dimension are stored in the two metadata JSON files linked at the top of this document.

For manuscript-level presentation, implementation categories are merged into the following unified groups:

- `env_stat`, `env_extra` -> **Envelope / amplitude**
- `phase_extra` -> **Phase**
- `inst_freq`, `ifreq_extra` -> **Instantaneous frequency**
- `spectrum_shape`, `spectrum_extra` -> **Spectrum**
- `corr_extra` -> **Correlation**
- `m_power` and the I/Q-balance descriptor family -> **M-power spectrum / I/Q balance**
- `hoc` -> **Higher-order statistics / HOC**

The final rank-ordered zero-based indices are:

### RML2018.01A

```text
52, 1, 58, 47, 5, 68, 48, 51, 55, 0, 3, 69,
44, 40, 88, 42, 46, 95, 22, 96, 49, 28, 29, 43
```

| Unified category | Count |
|---|---:|
| Higher-order statistics / HOC | 8 |
| Envelope / amplitude | 8 |
| Phase | 2 |
| Spectrum | 2 |
| Correlation | 2 |
| M-power spectrum / I/Q balance | 2 |

### Self-built USRP dataset

```text
90, 96, 91, 50, 92, 95, 88, 80, 25, 93, 24, 18,
85, 94, 89, 78, 51, 0, 19, 55, 64, 72, 11, 67
```

| Unified category | Count |
|---|---:|
| Correlation | 8 |
| Spectrum | 5 |
| Instantaneous frequency | 3 |
| Envelope / amplitude | 3 |
| Phase | 2 |
| M-power spectrum / I/Q balance | 2 |
| Higher-order statistics / HOC | 1 |

The two Top-24 sets share six indices: `0, 51, 55, 88, 95, 96`.

## 6. Selector analysis added in revision

### LR-only vs equal-weight aggregation

On RML2018.01A:

| Ranking criterion | Overall accuracy |
|---|---:|
| LR only | $63.39 \pm 0.06\%$ |
| ET only | $63.31 \pm 0.08\%$ |
| MI only | $63.22 \pm 0.09\%$ |
| Equal LR+ET+MI aggregation | $63.40 \pm 0.05\%$ |

Comparing the LR-only ranking with the final equal-weight ranking:

- Top-24 overlap: 14/24;
- Top-24 Jaccard similarity: 0.412;
- Spearman correlation over the complete 98-dimensional ranking: 0.732.

### Training-data resampling stability

A separate selector-stability analysis uses five class-SNR-stratified 80% resamples of the RML selector-training data. The data-sampling seeds are 7, 17, 27, 37, and 47, while selector-internal randomness is held fixed.

Results:

- pairwise Top-24 Jaccard: $0.936 \pm 0.034$;
- minimum: 0.920;
- maximum: 1.000;
- each resampled Top-24 shares 23/24 or 24/24 dimensions with the full-training-set Top-24.

This analysis changes the training-sample composition rather than the five neural-network training seeds used for the main accuracy results.

### Offline selector cost

Measured in the same revision-analysis run:

| Component | Wall-clock time |
|---|---:|
| 98-D deterministic prior extraction | 79.4 s |
| Sparse LR | 183.44 s |
| ExtraTrees | 4.32 s |
| Mutual information | 14.11 s |
| normalization + aggregation + Top-24 sorting | approximately 0.0002 s |
| selector scoring/aggregation total | approximately 202.0 s |

These are one-time offline configuration costs and are not per-sample inference latency.

## 7. Matched gate ablation on RML2018.01A

The revised RML experiment isolates the learned sample-wise gate while keeping the selected priors and projection structure fixed.

| Configuration | Overall accuracy |
|---|---:|
| Direct Concat Top-24 | $63.22 \pm 0.07\%$ |
| Top-24 + same projection, fixed $\alpha=1$ | $63.28 \pm 0.09\%$ |
| Full DPS-CF | $63.40 \pm 0.05\%$ |

The fixed-$\alpha$ and full DPS-CF variants use the same Top-24 prior set, frozen CNN+LSTM backbone, $24 \rightarrow 64 \rightarrow 64$ projection network, classifier, and training protocol. The learned sample-wise gate is the controlled difference between the final two rows.

## 8. External baseline reproduction notes

All external baselines are retrained from scratch under the unified dataset split and evaluation protocol; reported results are not copied from the original papers.

| Method | Implementation basis | Public source | Principal adaptation |
|---|---|---|---|
| 1D-ResNet | ResNet residual-learning structure | ResNet paper | One-dimensional residual implementation for $2\times1024$ I/Q input and dataset-specific classifier output |
| MCLDNN | Original paper and author implementation | https://github.com/wzjialang/MCLDNN | Preserve the multi-channel CNN-LSTM mechanism; adapt input/output interfaces and retrain under the common protocol |
| TLDNN | Original paper and author PyTorch implementation | https://github.com/qyp2000/TLDNN | Preserve the core network; adapt input/output interfaces and retrain under the common protocol |
| HKDD | Original paper and author project | https://github.com/yexijoe/HKDD | Preserve the dual-branch representation and feature-level attention/fusion mechanism; replace the original handcrafted-feature input with the same 98-D candidate-prior pool used by DPS-CF |

The HKDD result therefore corresponds to a unified-prior-pool adaptation rather than an unchanged run of its original 228-dimensional handcrafted-feature input.

## 9. Accuracy statistics

All values below are five-seed mean $\pm$ standard deviation.

| Method | RML overall | RML 0--20 dB | USRP overall |
|---|---:|---:|---:|
| CNN+LSTM | $62.79 \pm 0.08\%$ | $88.23 \pm 0.13\%$ | $80.45 \pm 0.22\%$ |
| 1D-ResNet | $61.49 \pm 0.17\%$ | $86.90 \pm 0.11\%$ | $78.82 \pm 0.31\%$ |
| MCLDNN | $62.63 \pm 0.12\%$ | $88.09 \pm 0.16\%$ | $80.23 \pm 0.26\%$ |
| TLDNN | $62.35 \pm 0.19\%$ | $87.66 \pm 0.14\%$ | $77.74 \pm 0.37\%$ |
| HKDD | $60.96 \pm 0.15\%$ | $85.86 \pm 0.18\%$ | $80.32 \pm 0.29\%$ |
| DPS-CF | $63.40 \pm 0.05\%$ | $89.11 \pm 0.09\%$ | $82.14 \pm 0.18\%$ |

## 10. Complexity and latency scope

The manuscript reports parameters, FLOPs, and batch-1 FP32 neural-network forward latency for a 1024-sample input.

For DPS-CF, the forward-latency measurement assumes that the selected prior vector is already available. It excludes deterministic prior extraction, offline LR/ET/MI fitting, ranking/Top-k selection, and data loading.

The offline selector cost is reported separately above because it is incurred during environment-level configuration rather than per-sample online inference.
