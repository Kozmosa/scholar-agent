# Key References for Spatio-Temporal Prediction Research

## Foundation Papers

### Graph Neural Networks
1. **Kipf & Welling (2017)**. Semi-supervised Classification with Graph Convolutional Networks. ICLR.
2. **Velickovic et al. (2018)**. Graph Attention Networks. ICLR.
3. **Wu et al. (2020)**. A Comprehensive Survey on Graph Neural Networks. IEEE TNNLS.

### Spatio-Temporal GNNs

#### Classic Methods (2018-2019)
1. **Yu et al. (2018)**. Spatio-Temporal Graph Convolutional Networks: A Deep Learning Framework for Traffic Forecasting. IJCAI. [STGCN]
2. **Li et al. (2018)**. Diffusion Convolutional Recurrent Neural Network: Data-Driven Traffic Forecasting. ICLR. [DCRNN]
3. **Wu et al. (2019)**. Graph WaveNet for Deep Spatial-Temporal Graph Modeling. IJCAI.

#### Adaptive Graph Learning (2020)
1. **Bai et al. (2020)**. Adaptive Graph Convolutional Recurrent Network for Traffic Forecasting. NeurIPS. [AGCRN]
2. **Wu et al. (2020)**. Connecting the Dots: Multivariate Time Series Forecasting with Graph Neural Networks. KDD. [MTGNN]
3. **Zheng et al. (2020)**. GMAN: A Graph Multi-Attention Network for Traffic Prediction. AAAI.

#### Dynamic Graph Models (2021-2023)
1. **Li et al. (2021)**. Dynamic Graph Convolutional Recurrent Network for Traffic Prediction. ACM TKDD. [DGCRN]
2. **Choi et al. (2022)**. Graph Neural Controlled Differential Equations for Traffic Forecasting. AAAI. [STG-NCDE]
3. **Jiang et al. (2023)**. PDFormer: Propagation Delay-Aware Dynamic Long-Range Transformer for Traffic Flow Prediction. AAAI.
4. **Chen et al. (2022)**. TAMP-S2GCNets: Coupling Time-Aware Multipersistence Knowledge Representation with Spatio-Supra Graph Convolutional Networks. ICLR.

### Graph Sparsification
1. **Li et al. (2020)**. SGCN: A Graph Sparsifier Based on Graph Convolutional Networks. PAKDD.
2. **Chen et al. (2021)**. A Unified Lottery Ticket Hypothesis for Graph Neural Networks. ICML. [UGS]
3. **Duan et al. (2023)**. Localised Adaptive Spatial-Temporal Graph Neural Network. KDD. [AGS]

### Time Series Forecasting

#### Transformer-Based
1. **Zhou et al. (2021)**. Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting. AAAI.
2. **Wu et al. (2021)**. Autoformer: Decomposition Transformers with Auto-Correlation for Long-term Series Forecasting. NeurIPS.
3. **Zhou et al. (2022)**. FEDformer: Frequency Enhanced Decomposed Transformer for Long-term Series Forecasting. ICML.
4. **Wu et al. (2023)**. TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis. ICLR.
5. **Nie et al. (2023)**. A Time Series is Worth 64 Words: Long-term Forecasting with Transformers. ICLR. [PatchTST]
6. **Liu et al. (2024)**. iTransformer: Inverted Transformers Are Effective for Time Series Forecasting. ICLR.
7. **Zeng et al. (2023)**. Are Transformers Effective for Time Series Forecasting? AAAI. [DLinear]

### LLM for Time Series
1. **Gruver et al. (2024)**. Large Language Models are Zero-Shot Time Series Forecasters. NeurIPS.
2. **Jin et al. (2024)**. Time-LLM: Time Series Forecasting by Reprogramming Large Language Models. ICLR.
3. **Chang et al. (2023)**. LLM4TS: Two-Stage Fine-Tuning for Time-Series Forecasting with Pre-Trained LLMs. arXiv.
4. **Zhou et al. (2023)**. One Fits All: Power General Time Series Analysis by Pretrained LM. NeurIPS.

### Hypergraph Neural Networks
1. **Huang & Yang (2021)**. UniGNN: A Unified Framework for Graph and Hypergraph Neural Networks. IJCAI.
2. **Shang et al. (2024)**. Ada-MSHyper: Adaptive Multi-Scale Hypergraph Transformer for Time Series Forecasting. NeurIPS.
3. **Yan et al. (2023)**. Spatio-Temporal Hypergraph Learning for Next POI Recommendation. SIGIR.

### Foundation Models for ST Prediction
1. **Yuan et al. (2024)**. UniST: A Prompt-Empowered Universal Model for Urban Spatio-Temporal Prediction. KDD.
2. **Li et al. (2024)**. OpenCity: Open Spatio-Temporal Foundation Models for Traffic Prediction. arXiv.
3. **Li et al. (2024)**. GPT-ST: Generative Pre-Training of Spatio-Temporal Graph Neural Networks. NeurIPS.
4. **Bi et al. (2023)**. Accurate Medium-Range Global Weather Forecasting with 3D Neural Networks. Nature. [Pangu-Weather]
5. **Nguyen et al. (2023)**. ClimaX: A Foundation Model for Weather and Climate. arXiv.
6. **Goodge et al. (2025)**. Spatio-Temporal Foundation Models: Vision, Challenges, and Opportunities. arXiv.

## KDD 2025 Papers (Analyzed)

### DLSTGNN (DynAGS)
- **Full Title**: Dynamic Localisation of Spatial-Temporal Graph Neural Network
- **Authors**: Wenying Duan, Shujun Guo, Zimu Zhou, Wei Huang, Hong Rao, Xiaoxi He
- **DOI**: 10.1145/3690624.3709331
- **Code**: https://github.com/wenyingduan/DynAGS

### DSTP (STH-SepNet)
- **Full Title**: Decoupling Spatio-Temporal Prediction: When Lightweight Large Models Meet Adaptive Hypergraphs
- **Authors**: Jiawen Chen, Qi Shao, Duxin Chen, Wenwu Yu
- **DOI**: 10.1145/3711896.3736904
- **Code**: https://github.com/SEU-WENJIA/ST-SepNet-Lightweight-LLMs-Meet-Adaptive-Hypergraphs

## Benchmark Datasets

### Traffic Flow
- **PEMS**: Caltrans Performance Measurement System
  - PEMS03, PEMS04, PEMS07, PEMS-BAY
- **METR-LA**: Los Angeles traffic speed (207 sensors)
- **LargeST**: Large-scale traffic benchmark (GLA dataset with 3,834 sensors)

### Other Domains
- **Blockchain**: Ethereum token networks (Bytom, Decentraland, Golem)
- **Biosurveillance**: COVID-19 hospitalization (CA, TX)
- **Bike Sharing**: Station inflow/outflow (BIKE datasets)

---

*Last updated: 2026-04-07*