# Spatio-Temporal Prediction Survey Report: Dynamic Graph Learning and LLM Integration

## Report Information
- **Date**: 2026-04-07
- **Source Papers**: KDD 2025 (DLSTGNN, DSTP)
- **Research Focus**: Adaptive Spatial-Temporal Graph Neural Networks, Hypergraph Learning, LLM-based Temporal Modeling

---

## 1. Introduction

### 1.1 Problem Definition

Spatio-temporal prediction is a fundamental task in modern data-driven decision-making with applications across:
- **Urban Traffic Forecasting**: Traffic flow, speed, demand prediction
- **Climate Modeling**: Weather prediction, air quality monitoring
- **Energy Grid Optimization**: Load forecasting, renewable energy scheduling
- **Biosurveillance**: Disease outbreak prediction, hospital resource planning

**Formal Definition**: Given historical observations X_{(t-L+1):t} ∈ R^{L×N×F}, predict future values X_{(t+1):(t+H)} ∈ R^{H×N×F}.

**Key Challenge**: Balancing model expressiveness (capturing complex dependencies) with computational efficiency (scalability to large real-world datasets).

### 1.2 Core Challenges

1. **Dynamic Spatial Dependencies**: Relationships between nodes evolve over time due to external conditions, events, and system dynamics
2. **Long-Range Temporal Dependencies**: Capturing multi-scale periodicity, trends, and sudden distribution shifts
3. **Higher-Order Interactions**: Multiple nodes may interact simultaneously (not just pairwise)
4. **Computational Scalability**: Graph convolutions have O(N²) complexity; complete graphs are prohibitive for large networks
5. **Communication Overhead**: Distributed deployment requires efficient node-to-node data exchange

---

## 2. Literature Review

### 2.1 Evolution of Spatio-Temporal Graph Neural Networks

#### Phase 1: Pre-defined Graphs (2018-2019)
- **STGCN** (Yu et al., IJCAI 2018): First ST-GNN framework combining GCN with 1D CNN
- **DCRNN** (Li et al., ICLR 2018): Diffusion convolution with GRU
- **GTS** (graph topology from predefined metrics or POI similarity)

**Limitation**: Heavy reliance on domain knowledge and fixed graph quality

#### Phase 2: Adaptive Graph Learning (2019-2020)
- **Graph WaveNet** (Wu et al., IJCAI 2019): Adaptive adjacency matrix via learnable node embeddings
- **AGCRN** (Bai et al., NeurIPS 2020): Node Adaptive Parameter Learning (NAPL-AGCN)
- **MTGNN** (Wu et al., KDD 2020): Graph learning module with mix-hop propagation

**Key Innovation**: Self-learned spatial dependencies through data-driven graph construction

#### Phase 3: Dynamic Graph Modeling (2021-2023)
- **DGCRN** (Li et al., 2021): Dynamic graph convolutional recurrent network
- **DMSTGCN** (Han et al., KDD 2021): Dynamic and multi-faceted ST deep learning
- **PDFormer** (Jiang et al., AAAI 2023): Propagation delay-aware dynamic transformer

**Challenge**: Complete graphs have high computational overhead; dynamic updates exacerbate communication costs

#### Phase 4: Graph Sparsification & Localization (2023)
- **AGS** (Duan et al., KDD 2023): Localised Adaptive Spatial-Temporal GNN
  - Pruning spatial graph to reduce data exchange
  - Static mask matrix approach
  - Foundation for distributed deployment efficiency

#### Phase 5: Foundation Models & LLM Integration (2023-2025)
- **Time-LLM** (Jin et al., ICLR 2024): Reprogramming LLMs for time series forecasting
- **GPT-ST** (Li et al., NeurIPS 2024): Generative pre-training of ST-GNNs
- **UniST** (Yuan et al., KDD 2024): Universal model for urban ST prediction
- **OpenCity** (Li et al., 2024): Open ST foundation models for traffic

### 2.2 Time Series Forecasting Evolution

#### Transformer-Based Methods
| Model | Key Innovation | Year | Conference |
|-------|----------------|------|------------|
| Informer | Efficient attention for long sequences | 2021 | AAAI |
| Autoformer | Auto-correlation mechanism | 2021 | NeurIPS |
| FEDformer | Frequency enhanced decomposition | 2022 | ICML |
| PatchTST | Patch-based attention | 2023 | ICLR |
| iTransformer | Inverted transformer for multivariate | 2024 | ICLR |
| TimesNet | 2D temporal variation modeling | 2023 | ICLR |

#### LLM-Based Approaches
| Model | Approach | Backbone |
|-------|----------|----------|
| LLM4TS | PEFT for time-series | BERT |
| Time-LLM | Prompt-based reprogramming | GPT-2 |
| One Fits All | Frozen LLM with linear probing | Various |
| UniCL | Contrastive embedding | - |

### 2.3 Hypergraph Neural Networks

**Definition**: A hypergraph H(V,E) has hypernodes V and hyperedges E, where each hyperedge connects multiple nodes simultaneously.

**Applications in ST Prediction**:
- **STHGCN** (Yan et al., 2023): Spatio-temporal hypergraph learning
- **AdaMSHyper** (Shang et al., NeurIPS 2024): Adaptive multi-scale hypergraph transformer

**Key Advantage**: Captures higher-order interactions that pairwise graphs cannot represent.

---

## 3. Paper Analysis: DLSTGNN (DynAGS)

### 3.1 Core Innovation

**Title**: Dynamic Localisation of Spatial-Temporal Graph Neural Network

**Key Contribution**: Addresses the limitation of AGS (static mask) by introducing **dynamic spatial dependency modeling**.

### 3.2 Methodology

#### Dynamic Graph Generator (DGG)
```
Input: Residual historical data X_res, Current observation X_t
Process:
1. Down-sample via AvgPool1D (kernel k, stride k)
2. Patch non-overlapping segments (length T_s)
3. Cross-attention: Query=X_t·W_v, Key=Value=X_patch·W_p + e_pos
Output: Node representation H^t for graph generation
```

#### Dynamic Mask Generation
- Hard concrete distribution for binary gates
- Node-independent decision making
- No prior data exchange required

#### Dynamic Adaptive Graph
```
E^t = E + H^t·W_H  (time-evolving embedding)
α_{i,j}^t = exp(e_i^t · e_j^t^T) / Σ_k exp(e_i^t · e_k^t^T)  (attention-based weights)
```

### 3.3 Results

| Localization | DynAGS vs AGS | Communication Reduction |
|--------------|---------------|------------------------|
| 99.5% vs 80% | Comparable/superior accuracy | ~40 times reduction |
| Same sparsity | Up to 13.5% less error | - |

**Datasets**: PEMS03/04/07, GLA, Bytom/Decentral/Golem, CA/TX

### 3.4 Key Insights

1. **Spatial dependencies are intrinsically time-dependent**: Static masks overlook this, leading to sub-optimal generalization
2. **Localization can have regularization effect**: Accuracy doesn't always decrease with increased sparsity
3. **Personalized localization**: Different nodes can have different sparsity configurations without affecting each other

---

## 4. Paper Analysis: DSTP (STH-SepNet)

### 4.1 Core Innovation

**Title**: Decoupling Spatio-Temporal Prediction: When Lightweight Large Models Meet Adaptive Hypergraphs

**Key Contribution**: **Decoupling strategy** separating temporal (LLM) and spatial (hypergraph) modeling.

### 4.2 Architecture

```
STH-SepNet:
├── Global Trend Module (Temporal)
│   ├── Average Pooling (local aggregation)
│   ├── Patching (time series tokens)
│   └── Lightweight LLM (BERT/GPT/LLAMA)
├── Hypergraph Spatio-Temporal Module (Spatial)
│   ├── Mix-Prop (multi-layer propagation)
│   ├── Adaptive Graph Convolution (GCN)
│   └── Adaptive Hypergraph Convolution (HGCN)
└── Gated Fusion Module
    └── σ(FFN([O_LLM, O_Hypergraph]))
```

### 4.3 Adaptive Hypergraph Construction

**Algorithm**:
1. Generate node embeddings via FFN: F_3 = tanh(α·FFN(E_3))
2. KNN on F_3 to find k nearest neighbors
3. Form hyperedge: e_i = {v_i} ∪ N(v_i)
4. Build incident matrix: H_adp ∈ R^{n×m}

**Order Analysis** (empirical):
- k=2: pairwise (insufficient)
- k=3: optimal (captures underlying dependencies)
- k>3: overfitting

### 4.4 Results

| Dataset | STH-SepNet (BERT) | Best Non-LLM | Improvement |
|---------|-------------------|--------------|-------------|
| PEMS03 MAE | 21.03 | 26.84 | 21.6% |
| BIKE-Outflow MAE | 5.33 | 5.56 (TimesNet) | 4.1% |
| METR-LA MAE | 9.42 | 9.98 (MTGNN) | 5.6% |

**Key Findings**:
- Lightweight LLMs (BERT 110M) can outperform larger models (LLAMA 7B)
- Adaptive hypergraph > static graph > no spatial structure
- Decoupling reduces GPU consumption (24.6G vs TIMELLM)

---

## 5. Comparative Analysis

### 5.1 Methodological Comparison

| Aspect | DynAGS (DLSTGNN) | STH-SepNet (DSTP) |
|--------|------------------|-------------------|
| **Core Approach** | Dynamic localization | Decoupling + Hypergraph |
| **Temporal Module** | Cross-attention (DGG) | Lightweight LLM |
| **Spatial Module** | Dynamic sparse graph | Adaptive hypergraph |
| **Efficiency Strategy** | Communication reduction | Decoupled processing |
| **Higher-Order** | No (pairwise graph) | Yes (hyperedges) |
| **LLM Integration** | No | Yes |
| **Distributed Focus** | Strong | Moderate |

### 5.2 Strengths and Limitations

#### DynAGS
**Strengths**:
- Excellent for distributed deployment
- Significant communication cost reduction
- Personalized localization flexibility
- Applicable to multiple backbone architectures (AGCRN, STG-NCDE)

**Limitations**:
- Does not address higher-order interactions
- Added complexity for dynamic mask generation
- Focuses on pairwise spatial relationships

#### STH-SepNet
**Strengths**:
- Higher-order interaction modeling via hypergraphs
- LLM brings rich temporal pattern understanding
- Lightweight models achieve competitive performance
- Decoupling reduces computational overhead

**Limitations**:
- Assumes clean temporal-spatial decoupling
- Real-time hyperedge generation may have latency issues
- Less focus on distributed deployment efficiency

### 5.3 Complementary Perspectives

Both papers address **efficiency vs expressiveness** trade-off but from different angles:

- **DynAGS**: Efficiency through **sparsity and localization** (communication-centric)
- **STH-SepNet**: Efficiency through **decoupling and lightweight models** (computation-centric)

**Potential Combination**:
- Apply DynAGS dynamic localization to STH-SepNet's hypergraph structure
- Use LLM temporal features in DynAGS's DGG for better historical integration

---

## 6. Research Trends and Future Directions

### 6.1 Current Trends

1. **Foundation Models for ST Prediction**
   - Pre-training on large-scale ST datasets
   - Transfer learning across domains (traffic, weather, energy)
   - UniST, OpenCity, ClimaX as early examples

2. **LLM Integration**
   - Lightweight models preferred over large ones
   - Prompt-based reprogramming (Time-LLM approach)
   - LoRA fine-tuning for domain adaptation

3. **Dynamic Graph Structures**
   - Time-evolving adjacency matrices
   - Adaptive topology learning
   - Event-driven graph updates

4. **Hypergraph Learning**
   - Higher-order dependency modeling
   - Multi-node interaction representation
   - KNN-based hyperedge construction

### 6.2 Research Gaps

1. **Hybrid Dynamic Hypergraph Localization**: No existing work combines DynAGS-style localization with hypergraph higher-order modeling

2. **LLM + Distributed Efficiency**: Current LLM-based ST models focus on centralized deployment; distributed scenarios unexplored

3. **Foundation Model Integration**: Neither DynAGS nor STH-SepNet leverages pre-trained ST foundation models

4. **Real-world Deployment**: Simulated distributed experiments; actual edge deployment challenges (latency, synchronization) not addressed

5. **Cross-domain Transfer**: Methods tested primarily on traffic; generalization to other domains (weather, healthcare) limited

### 6.3 Future Research Directions

#### Short-term (1-2 years)
1. Combine DynAGS localization with STH-SepNet hypergraphs
2. Develop distributed LLM-based ST prediction frameworks
3. Create efficient hypergraph localization techniques

#### Medium-term (3-5 years)
1. Foundation models that learn both temporal and spatial patterns from large ST corpora
2. Event-aware dynamic graph updates (traffic accidents, weather events)
3. Federated learning for ST prediction with communication efficiency

#### Long-term (5+ years)
1. Unified ST foundation models applicable across all domains
2. Real-time adaptive prediction systems for autonomous systems
3. Integration with digital twin technologies

---

## 7. Key References Summary

### Classic ST-GNN Papers
| Paper | Year | Conference | Key Contribution |
|-------|------|------------|------------------|
| STGCN | 2018 | IJCAI | First ST-GNN framework |
| DCRNN | 2018 | ICLR | Diffusion convolution |
| Graph WaveNet | 2019 | IJCAI | Adaptive adjacency matrix |
| AGCRN | 2020 | NeurIPS | NAPL-AGCN |
| MTGNN | 2020 | KDD | Graph learning module |
| GMAN | 2020 | AAAI | Multi-attention network |

### Dynamic/Advanced ST Methods
| Paper | Year | Conference | Key Contribution |
|-------|------|------------|------------------|
| DGCRN | 2021 | TKDD | Dynamic graph convolution |
| STG-NCDE | 2022 | AAAI | Neural controlled differential equations |
| AGS | 2023 | KDD | Localized ASTGNN |
| STAEformer | 2023 | CIKM | Adaptive embedding transformer |
| DynAGS | 2025 | KDD | Dynamic localization (this paper) |

### LLM/Foundation Model Approaches
| Paper | Year | Conference | Key Contribution |
|-------|------|------------|------------------|
| Time-LLM | 2024 | ICLR | Reprogramming LLMs |
| GPT-ST | 2024 | NeurIPS | Generative pre-training |
| UniST | 2024 | KDD | Universal ST model |
| ClimaX | 2023 | arXiv | Weather foundation model |
| STH-SepNet | 2025 | KDD | Decoupling + Hypergraph (this paper) |

### Hypergraph Methods
| Paper | Year | Conference | Key Contribution |
|-------|------|------------|------------------|
| UniGNN | 2021 | IJCAI | Unified framework |
| AdaMSHyper | 2024 | NeurIPS | Multi-scale hypergraph transformer |
| STH-SepNet | 2025 | KDD | Adaptive hypergraph for ST |

---

## 8. Conclusion

This survey analyzes two cutting-edge KDD 2025 papers addressing spatio-temporal prediction efficiency:

1. **DynAGS (DLSTGNN)**: Dynamic localization for communication-efficient distributed deployment
2. **STH-SepNet (DSTP)**: Decoupled LLM-hypergraph architecture for computation-efficient centralized prediction

Both represent significant advances in addressing the expressiveness-efficiency trade-off, though from different perspectives. The field is trending toward:
- Foundation models with large-scale pre-training
- LLM integration for temporal modeling
- Dynamic and adaptive graph structures
- Higher-order interaction modeling via hypergraphs

Key research gaps remain in combining localization with higher-order modeling, extending LLM-based methods to distributed scenarios, and creating unified foundation models for cross-domain ST prediction.

---

## Appendix: Benchmark Datasets

### Traffic Datasets
| Dataset | Nodes | Time Range | Aggregation | Common Split |
|---------|-------|------------|-------------|--------------|
| PEMS03 | 358 | Sep-Nov 2018 | 5-min | 6:2:2 |
| PEMS04 | 307 | Jan-Feb 2018 | 5-min | 6:2:2 |
| PEMS07 | 883 | Jul-Aug 2017 | 5-min | 6:2:2 |
| GLA | 3,834 | Jan-Dec 2019 | 15-min | - |
| METR-LA | 207 | Mar-Jun 2012 | 5-min | 7:1:2 |
| BJ500 | - | - | - | - |

### Other Domains
| Domain | Dataset | Nodes | Time Interval |
|---------|---------|-------|---------------|
| Blockchain | Bytom/Decentral/Golem | 100 | Daily |
| Biosurveillance | CA/TX COVID | 55/251 | Daily |
| Bike Sharing | BIKE-Inflow/Outflow | - | - |

---

*Report generated: 2026-04-07*
*Sources: KDD 2025 papers (DLSTGNN, DSTP), arXiv, conference proceedings*