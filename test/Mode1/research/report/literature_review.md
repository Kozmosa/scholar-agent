# Literature Review: Spatio-Temporal Prediction

## Research Topic
From the KDD 2025 papers (DLSTGNN, DSTP) to deep exploration of current research in spatio-temporal prediction, focusing on:
- Adaptive Spatial-Temporal Graph Neural Networks
- Dynamic Graph Learning
- LLM Integration for Time Series
- Hypergraph Neural Networks
- Foundation Models for ST Prediction

---

## Literature Table

### Core Papers (KDD 2025 - Analyzed)

| Paper | Venue | Method | Key Result | Relevance | Source |
|-------|-------|--------|------------|-----------|--------|
| DynAGS (DLSTGNN) | KDD 2025 | Dynamic localization of ASTGNN with time-evolving spatial graphs | 40x communication reduction, 13.5% less error vs AGS | Direct: dynamic graph sparsification | Local |
| STH-SepNet (DSTP) | KDD 2025 | Decoupled LLM + adaptive hypergraph | 21.6% MAE improvement, 28.8% RMSE reduction | Direct: hypergraph + LLM integration | Local |

### LLM-Based Time Series Methods

| Paper | Venue | Method | Key Result | Relevance | Source |
|-------|-------|--------|------------|-----------|--------|
| Time-LLM | ICLR 2024 | Reprogramming LLMs with text prototypes + Prompt-as-Prefix | Superior forecasting, few-shot/zero-shot capability | High: LLM for time series baseline | arXiv:2310.01728 |
| UniCL | arXiv 2024 | Universal contrastive learning for time series foundation models | High performance across multiple domains | High: foundation model approach | arXiv:2405.10597 |

### Foundation Models for ST Prediction

| Paper | Venue | Method | Key Result | Relevance | Source |
|-------|-------|--------|------------|-----------|--------|
| OpenCity | arXiv 2024 | Open ST foundation models for traffic prediction with attention + topology | Strong transfer learning performance | High: ST foundation model | arXiv:2408.10269 |
| ClimaX | arXiv 2023 | Foundation model for weather and climate with diverse variables | Handles heterogeneous environmental data | Medium: domain-specific foundation model | arXiv:2301.10343 |
| ST Foundation Models Vision | arXiv 2025 | Vision paper outlining essential characteristics of STFMs | Conceptual framework for future research | High: research direction | arXiv:2501.09045 |

### Transformer-Based Time Series

| Paper | Venue | Method | Key Result | Relevance | Source |
|-------|-------|--------|------------|-----------|--------|
| iTransformer | ICLR 2024 | Inverted attention on multivariate dimensions | SOTA on real-world datasets | Medium: strong baseline | arXiv:2310.06625 |
| TimesNet | ICLR 2023 | Temporal 2D-variation modeling | Effective pattern recognition | Medium: time series baseline | arXiv:2210.02186 |
| PatchTST | ICLR 2023 | Patch-based transformer for long-term forecasting | Efficient tokenization | Medium: patching technique | arXiv:2211.14730 |

### Graph Neural Network Classics

| Paper | Venue | Method | Key Result | Relevance | Source |
|-------|-------|--------|------------|-----------|--------|
| AGCRN | NeurIPS 2020 | Adaptive graph convolutional recurrent network with NAPL | Foundational ASTGNN architecture | Core: baseline architecture | Citation |
| Graph WaveNet | IJCAI 2019 | Adaptive adjacency matrix via learnable embeddings | Self-learned spatial dependencies | Core: adaptive graph learning | Citation |
| MTGNN | KDD 2020 | Graph learning module with mix-hop propagation | Strong benchmark performance | Core: benchmark method | Citation |

---

## Synthesis: Current Research Landscape

### 1. Evolution of Spatio-Temporal Prediction

The field has evolved through distinct phases:

**Phase 1 (2018-2019)**: Pre-defined graphs with domain knowledge
- STGCN, DCRNN established the GNN framework for traffic prediction
- Heavy reliance on handcrafted spatial structures

**Phase 2 (2020-2021)**: Adaptive graph learning
- Graph WaveNet and AGCRN introduced data-driven graph construction
- Self-learned spatial dependencies through node embeddings
- Challenge: Complete graphs with O(N²) complexity

**Phase 3 (2022-2023)**: Dynamic and efficient modeling
- DGCRN, PDFormer introduced time-evolving graphs
- AGS proposed graph sparsification for efficiency
- Challenge: Static sparsification doesn't capture dynamic dependencies

**Phase 4 (2024-2025)**: Foundation models and LLM integration
- Time-LLM demonstrated LLM reprogramming for time series
- OpenCity introduced ST foundation models for transfer learning
- Current papers (DynAGS, STH-SepNet) represent latest advances

### 2. Key Technical Themes

#### 2.1 Dynamic vs Static Graph Structures

**Consensus**: Spatial dependencies evolve over time due to:
- External events (accidents, weather)
- Temporal patterns (rush hours, seasons)
- System dynamics

**Approaches**:
- **DynAGS**: Dynamic mask + adjacency matrices via cross-attention
- **DGCRN**: Dynamic graph convolution
- **PDFormer**: Propagation delay-aware transformers

**Gap**: No work combines dynamic localization with higher-order hypergraphs.

#### 2.2 LLM Integration Strategies

**Approaches**:
| Strategy | Paper | Mechanism |
|----------|-------|-----------|
| Reprogramming | Time-LLM | Text prototypes + Prompt-as-Prefix |
| Contrastive Learning | UniCL | Spectral data contrastive pre-training |
| Lightweight Adaptation | STH-SepNet | LoRA fine-tuning + decoupled processing |

**Key Finding**: Lightweight models (BERT 110M) can outperform large models (LLAMA 7B) when combined with specialized spatial modules.

#### 2.3 Hypergraph for Higher-Order Interactions

**Motivation**: Traditional graphs capture only pairwise relationships. Traffic networks have multi-node interactions (intersection effects, regional congestion).

**Methods**:
- **STH-SepNet**: KNN-based hyperedge construction, optimal order k=3
- **AdaMSHyper**: Multi-scale hypergraph transformer

**Theoretical Insight**: (k-1)-hop neighborhood corresponds to k-order hyperedges under certain conditions.

#### 2.4 Efficiency-Expressiveness Trade-off

**Communication Efficiency** (Distributed focus):
| Method | Approach | Reduction |
|--------|----------|-----------|
| DynAGS | Dynamic localization | 40x communication |
| AGS | Static localization | Baseline |

**Computational Efficiency** (Centralized focus):
| Method | Approach | Reduction |
|--------|----------|-----------|
| STH-SepNet | Decoupling + lightweight LLM | GPU 24.6G vs TIMELLM |

### 3. Research Gaps and Opportunities

#### Gap 1: Hybrid Dynamic Hypergraph Localization
- DynAGS handles dynamic pairwise graphs
- STH-SepNet handles static hypergraphs
- **Opportunity**: Dynamic localized hypergraphs for distributed higher-order modeling

#### Gap 2: LLM for Distributed ST Prediction
- Current LLM methods focus on centralized deployment
- **Opportunity**: Federated LLM-based ST prediction with communication efficiency

#### Gap 3: Foundation Model Integration
- Neither paper leverages pre-trained ST foundation models (OpenCity, UniST)
- **Opportunity**: Fine-tuning ST foundation models with dynamic localization

#### Gap 4: Cross-Domain Generalization
- Methods primarily tested on traffic data
- Weather (ClimaX) and healthcare domains underexplored
- **Opportunity**: Domain-agnostic dynamic graph learning

### 4. Emerging Trends

1. **ST Foundation Models**: Growing interest in pre-trained models for transfer learning
2. **LLM Integration**: Lightweight models preferred over large ones
3. **Dynamic Structures**: Time-evolving graphs becoming standard
4. **Higher-Order Modeling**: Hypergraphs gaining attention

---

## Recommended Reading Priority

### Must Read (High Relevance)
1. Time-LLM (ICLR 2024) - LLM integration baseline
2. OpenCity (arXiv 2024) - ST foundation model
3. AGCRN (NeurIPS 2020) - Foundational ASTGNN

### Should Read (Medium Relevance)
4. iTransformer (ICLR 2024) - Strong transformer baseline
5. ClimaX (arXiv 2023) - Domain-specific foundation model
6. UniCL (arXiv 2024) - Contrastive learning for time series

### Background Reading
7. Graph WaveNet, MTGNN - Classic benchmarks
8. TimesNet, PatchTST - Time series methods

---

## BibTeX Snippet

```bibtex
@inproceedings{duan2025dynags,
  title={Dynamic Localisation of Spatial-Temporal Graph Neural Network},
  author={Duan, Wenying and Guo, Shujun and Zhou, Zimu and Huang, Wei and Rao, Hong and He, Xiaoxi},
  booktitle={KDD},
  year={2025}
}

@inproceedings{chen2025sthsepnet,
  title={Decoupling Spatio-Temporal Prediction: When Lightweight Large Models Meet Adaptive Hypergraphs},
  author={Chen, Jiawen and Shao, Qi and Chen, Duxin and Yu, Wenwu},
  booktitle={KDD},
  year={2025}
}

@inproceedings{jin2024timellm,
  title={Time-LLM: Time Series Forecasting by Reprogramming Large Language Models},
  author={Jin, Ming and Wang, Shiyu and Ma, Lintao and others},
  booktitle={ICLR},
  year={2024}
}

@article{li2024opencity,
  title={OpenCity: Open Spatio-Temporal Foundation Models for Traffic Prediction},
  author={Li, Zhonghang and Xia, Long and Shi, Lei and others},
  journal={arXiv:2408.10269},
  year={2024}
}

@article{goodge2025stfm,
  title={Spatio-Temporal Foundation Models: Vision, Challenges, and Opportunities},
  author={Goodge, Adam and Ng, Wee Siong and Hooi, Bryan and Ng, See Kiong},
  journal={arXiv:2501.09045},
  year={2025}
}
```

---

*Literature Review Generated: 2026-04-07*
*Sources: Local papers (DLSTGNN, DSTP), arXiv, Web Search*