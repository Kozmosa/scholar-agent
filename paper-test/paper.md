# End-Edge-Cloud Collaboration-Based False Data Injection Attack Detection in Distribution Networks

Houjun Li , Chunxia Dou $\textcircled{1}$ , Senior Member, IEEE, Dong Yue $\textcircled{1}$ , Fellow, IEEE, Gerhard P. Hancke $\textcircled{1}$ , Life Fellow, IEEE, Zeng Zeng, Wei Guo $\textcircled{1}$ , and Lei Xu $\textcircled { 1 0 }$ 

Abstract—False data injection attack (FDIA) can pose a severe threat to the distribution networks (DN), and the accurate detection of FDIA plays a key role in the safe and reliable operation of the DN. In this article, an end-edge-cloud collaboration-based detection framework is proposed to detect FDIA in the DN. First, in order to effectively preserve the privacy of different stakeholders in the DN and solve the problem of data island, a federatedlearning-based edge-cloud collaboration mechanism is designed according to the proposed end-edge-cloud collaboration framework to jointly train the local FDIA detection models and eventually build a comprehensive FDIA detection model. Then, considering the temporal–spatial correlation of measurement data, a local data-driven FDIA detection model is proposed based on a novel temporal–spatial graph convolutional network, which can extract temporal–spatial features of the measurement data and improve the FDIA detection performance. In general, compared with the traditional centralized FDIA detection methods, the proposed method can make full use of the computational capacity of distributed edge devices and reduce the pressure of computation on the control center. 

Manuscript received 24 March 2023; accepted 24 May 2023. Date of publication 31 May 2023; date of current version 19 January 2024. This work was supported in part by the Jiangsu Provincial Key Research and Development Program under Grant BE2020001-4, in part by the Postgraduate Research and Practice Innovation Program of Jiangsu Province under Grant KYCX22_1014, in part by the Natural Science Foundation of Jiangsu Province under Grant BK20210589, and in part by the National Natural Science Foundation of China under Grant 62293500 and Grant 62293504. Paper no. TII-23-1007. (Corresponding authors: Chunxia Dou; Dong Yue.) 

Houjun Li, Chunxia Dou, and Lei Xu are with the Institute of Advanced Technology for Carbon Neutrality, Nanjing University of Posts and Telecommunications, Nanjing 210023, China (e-mail: lihoujunertou@ 163.com; cxdou@ysu.edu.cn; xulei_688@163.com). 

Dong Yue is with the College of Automation and Artificial Intelligence, Nanjing University of Posts and Telecommunications, Nanjing 210023, China, and also with the Institute of Advanced Technology for Carbon Neutrality, Nanjing University of Posts and Telecommunications, Nanjing 210023, China (e-mail: yued@njupt.edu.cn). 

Gerhard P. Hancke is with the College of Automation and Artificial Intelligence, Nanjing University of Posts and Telecommunications, Nanjing 210023, China (e-mail: g.hancke@ieee.org). 

Zeng Zeng is with the State Grid Jiangsu Electric Power Company, Ltd., Information Communication Branch, Nanjing 210003, China (e-mail: zengking913@126.com). 

Wei Guo is with the State Grid Hebei Economic Research Institute, Shijiazhuang 050000, China (e-mail: guoweincepu@126.com). 

Color versions of one or more figures in this article are available at https://doi.org/10.1109/TII.2023.3281664. 

Digital Object Identifier 10.1109/TII.2023.3281664 

Finally, simulation results based on the modified IEEE 14-bus and IEEE 118-bus distribution systems indicate that the proposed method can effectively improve the accuracy of FDIA detection compared with other methods. 

Index Terms—Attack detection, distribution networks (DNs), end-edge-cloud collaboration, false data injection attack (FDIA), federated learning (FL), graph convolutional network (GCN). 

# I. INTRODUCTION

W ITH the integration of intelligent devices and advancedcommunication technologies, the distribution networks (DN) are developing towards cyber-physical distribution systems in recent years [1]. The cyber-physical distribution systems consist of numerous smart sensors, edge devices, and communication devices, which can exchange information with control centers for achieving the reliable operation of the DN [2]. However, these devices create vulnerabilities in the DN that adversaries can invade. Adversaries can launch cyberattacks such as replay attack, denial-of-service (DoS) attack, and false data injection attack (FDIA) by compromising the communication system or attacking the measurement devices that lack tamper-proof hardware [3]. These potential cyberattacks could lead to large-scale failure of the DN. For example, Ukraine had suffered from severe economic damage because of the power outages caused by cyberattacks in 2015 [4]. 

Among these cyberattacks, FDIA is considered as one of the most threatening attacks. It can compromise the system state by changing the measurement data without being detected by the traditional bad data detection mechanism [5]. And the system state will deviate from its actual value, which will cause the control center of the DN to make wrong decisions and affect the reliable operation of the DN [6]. Therefore, it is crucial to detect FDIA rapidly to ensure the normal operation of the DN. 

Research on the detection of FDIA can be divided into two categories, i.e., model-based methods [7], [8], [9], and data-driven methods [10], [11], [12], [13], [14]. For example, Xiahou et al. [7] present an observer-based decentralized scheme to detect FDIA for the interconnected power system. Considering the physical state of the power system and the unknown disturbance, Wang et al. [8] propose an attack detection method based on interval observer, which can be scaled to large-scale systems. Yan et al. [9] develop a dynamic reduced-order observer-based FDIA detection method, which can enhance the robustness of the detection model. In general, model-based methods require the system model of the power 

system and related system parameters to detect FDIA. Nevertheless, slight uncertainty of system model parameters can affect the performance of model-based methods [15]. In addition, the amount of measurement data will become larger and the system model will become more complex with a large amount of distributed sources connected to the DN. These eventually result in the features of FDIA being submerged in the massive amount of information. Moreover, it is difficult for model-based methods to model the large-scale system to mine the features of the FDIA. In comparison, data-driven methods are independent of the system model and can cope with massive data well due to its excellent data processing ability and nonlinear expression ability. With the measurement data, the data-driven methods can realize the detection of FDIA. On the basis of this condition, this article utilizes data-driven methods to detect FDIA. 

Many notable works on detecting FDIA using data-driven methods have been reported. For instance, Chen et al. [10] design a FDIA detection scheme based on the deep autoencoding Gaussian mixture model. In order to reduce the dimensionality of the measurement data, Yang et al. [11] combine the autoencoder and extreme learning machine to detect the unobservable FDIA. Considering the temporal correlation of the system state, Dou et al. [12] use variational mode decomposition and extreme learning machine to detect FDIA. On the other hand, taking account of the physical topological association of buses in a power system, Drayer et al. [13] propose a novel attack detection method based on the concept of the graph signal processing. Moreover, Boyaci et al. [14] first use the graph neural network (GNN) to extract the spatial features of measurement data and then carry out attack detection. However, there are still some weaknesses in the above methods. Nowadays, there is a strong spatial–temporal correlation between the measurement data of the buses in the DN [16] but the above methods only extract the temporal or spatial features of the measurement data independently and do not consider the temporal–spatial correlation of the measurement data. These make the above FDIA detection methods have certain limitations. Furthermore, it is difficult to effectively extract the temporal–spatial correlation features of the measurement data for detecting FDIA. For this reason, it is crucial to consider the temporal–spatial correlation property of the measurement data while designing the FDIA detection model. 

Besides, the above methods are basically centralized machine learning approaches. These methods require massive historical data generated by smart sensors. However, transmitting these data to the control center for centrally training the FDIA detection model may cause the leakage of users’ privacy, and this issue has not been considered in previous work. Furthermore, with the development of the electricity market and the access of large-scale distributed resources to the DN, different areas of the DN may be controlled by different stakeholders. A single stakeholder does not have the authority to access the entire data of the DN and cannot exchange private data with other stakeholders [17]. As a result, the measurement data of multistakeholders exists in the form of isolated islands, and each stakeholder can only use the local measurement data under its control to train the local FDIA detection model. In this situation, once the attacker launches FDIA based on the global system model and parameters of the entire DN, the detection model trained based on local measurement data is bound to perform poorly. Based on the above observation, it is necessary to take the problems of data island and users’ privacy into account in the design of the attack detection model. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/a1a40df07f5d8f1bdaa9758f8135e09cdfb32086be8aa2e8d2e53fee4c0ff903.jpg)



Fig. 1. Description of end-edge-cloud architecture.


Federated learning (FL) can effectively address the problem of data island and preserve users’ privacy by allowing different stakeholders jointly train deep learning models without sharing their private measurement data with other stakeholders [18]. During the training process, each edge device (i.e., each stakeholder) trains the corresponding local model using its private measurement data. Then, the cloud center aggregates the parameters of the local model uploaded by each edge device to form a global model and distributes it back to each edge device for the next round of training. The training process is repeated until a comprehensive model is obtained. The measurement data are kept on the edge devices rather than uploaded to the cloud center during the training process, which can effectively preserve data privacy. In addition, FL can build a comprehensive global model without sharing measurement data, which solves the problem of data island. Moreover, FL has been widely applied in power systems, including fault diagnosis [19] and solar irradiance prediction [20]. In view of the above, this article uses FL to solve the problem of data island and preserve the data privacy in the design of the attack detection model. 

On the other hand, the framework based on end-edge-cloud collaboration is increasingly used in control decision of the DN in which edge devices and the cloud center play an important role [21], [22], [23]. Moreover, the previous work basically detects FDIA just from sensor level (end side) or control center level (cloud side) without considering the temporal–spatial correlation of measurement data, which makes these methods have certain limitations. Accordingly, it is reasonable to develop a new framework based on end-edge-cloud collaboration to improve the accuracy of FDIA detection. 

In view of the above, an end-edge-cloud collaboration-based framework is proposed to detect FDIA for the first time in the DN in this article. The end-edge-cloud architecture is illustrated in Fig. 1. First, an edge-cloud collaboration mechanism based on FL is proposed to realize joint training of the local FDIA detection model deployed on the edge side. Furthermore, on the edge side, measurement data are collected and a novel temporal– spatial graph convolutional network (TSGCN) is designed to extract temporal–spatial features of measurement data simultaneously. The main contributions are summarized as follows. 

1) An end-edge-cloud collaboration-based FDIA detection framework is proposed to solve the problem of FDIA 

detection in DN for the first time. And it devotes to making full use of the computational capacity of distributed edge devices to reduce the pressure of computation in the control center. In this sense, the proposed detection framework can better support the detection of FDIA in large-scale DN by cooperating the control center and the edge devices. 

2) The edge-cloud collaboration mechanism based on FL is proposed according to the end-edge-cloud collaboration framework. By keeping the private measurement data of each edge device locally, this mechanism can use the private measurement data among multistakeholders to collaboratively train the FDIA detection model and eventually aggregate a comprehensive FDIA detection model, which can effectively preserve data privacy and solve the problem of data island. 

3) A novel data-driven FDIA detection model based on TSGCN is designed on the edge side. The proposed neural network can extract temporal–spatial features from the measurement data of the buses in the DN, which can help improve the FDIA detection performance and better provide attack awareness capabilities for the DN. To the best of the authors’ knowledge, this is the first time to apply TSGCN to the detection of FDIA. 

The rest of this article is organized as follows. Section II gives the introduction of the FDIA and the adverse impact. Section III introduces the framework of the FDIA detection model from the perspective of end-edge-cloud collaboration and explains edgecloud collaboration mechanism based on FL. In Section IV, we introduce the local FDIA detection model deployed on the edge side based on TSGCN. Afterward, Section V explains the performance of the proposed FDIA detection method by the simulation results. Finally, Section VI concludes this article. 

# II. BACKGROUND

We first briefly introduce the stealthy characteristic of the FDIA in DN and analyze how the FDIA evades the bad data detection mechanism. Finally, the adverse impact of the FDIA is explained. 

# A. Characteristics of FDIA in DNs

As stated in [24], the attacker can tamper measurement data $z$ by injecting attack vector $a$ without being detected by the bad data detection mechanism. 

The attack vector $a$ injected into the measurement data $z$ can be solved by the following optimization: 

$$
\begin{array}{l} \max  _ {a} \sum_ {i \in \{\mathcal {M} \}} a (i) \\ \text {s . t .} \left\{ \begin{array}{l} a (i) = 0 \quad \forall i \in \{\mathcal {S M} \} \\ \left\| \left(I - J \left(J ^ {T} R ^ {- 1} J\right) ^ {- 1} J ^ {T} R ^ {- 1}\right) a \right\| \leq \varepsilon \end{array} \right. \tag {1} \\ \end{array}
$$

where $a$ is attack vector, $a ( i )$ denotes the ith element of attack vector $a$ , $I$ ( )is the identity matrix, $R$ is a diagonal matrix that represents the covariance matrix of the measurement errors, $J$ is the Jacobian matrix, which is represented as $J = \partial j / \partial \kappa$ in which $j$ =represents the relationship between the system state $\kappa$ and the measurement data $z$ , $\mathcal { M }$ denotes the target attack area of the attacker, $_ { s { \mathcal { M } } }$ denotes the safe measurements, which cannot 

be compromised, $\varepsilon$ is the threshold designed by the attacker. The smaller the value of $\varepsilon$ , the less likely it is to be detected by the bad data detection mechanism. 

The objective of the optimization (1) is to maximize the value of attack vector $a$ . The first constraint of (1) ensures that all safe measurement data will not be attacked by attackers. The second inequality constraint of (1) ensures that the attack vector $a$ will not be detected by the bad data detection mechanism. To be more specific, define $J ( J ^ { T } R ^ { - 1 } J ) ^ { - 1 } J ^ { T } R ^ { - 1 }$ as $\Pi$ , we have $\| ( I - \Pi ) \bar { a } \| \leq \varepsilon \leq \tau - r$ (, where $\tau$ ) Πis the threshold for the bad ( Π)data detection mechanism and $r$ is the residual of the normal measurement data. The residual $r$ can be expressed as $r = z -$ $j ( \hat { \kappa } )$ , where $\hat { \kappa }$ =is the estimated system state. Then, according to (ˆ) ˆthe literature [25], we get 

$$
\begin{array}{l} \tau \geq r + \| (I - \Pi) a \| \\ = \| (I - \Pi) z \| + \| (I - \Pi) a \| \\ \geq \left\| (I - \Pi) (z + a) \right\| \\ \geq \left\| z _ {a} - j \left(\hat {\kappa} _ {a}\right) \right\| \tag {2} \\ \end{array}
$$

where $z _ { a }$ is the tampered measurement data, ${ \hat { \kappa } } _ { a }$ is the estimated ˆtampered system state. From (2), the attack vector constructed according to (1) can bypass the detection of the bad data detection mechanism. 

# B. Impacts of FDIA

1) Impact on Stable Operation: A well-designed FDIA can change the system state without being detected by the bad data detection mechanism. As a result, the control center of the DN will make wrong decisions with the tampered system state, thus affecting the reliable and stable operation of the DN. 

2) Impact on Electricity Market: By changing the measurement data received by the control center, the attacker can modify the electricity price as they expect. Because the attackers can participate in the electricity market through virtual bidding, the attackers need to sell (buy) as much energy in the real-time market as they buy (sell) in the day-ahead market [26]. Therefore, the attacker can achieve profits by buying low and selling high. 

# III. END-EDGE-CLOUD COLLABORATION-BASED FDIA DETECTION FRAMEWORK

Considering the problem of data island and users’ privacy preservation, the end-edge-cloud collaboration-based FDIA detection framework is introduced in this section. First, the architecture of the FDIA detection framework is introduced, and then, the edge-cloud collaboration mechanism based on FL is introduced. Finally, the implementation of end-edge-cloud collaboration-based FDIA detection framework is explained. 

# A. Architecture of FDIA Detection Framework

The architecture of the end-edge-cloud collaboration-based FDIA detection framework is shown in Fig. 2. The proposed framework includes the following three main components. 

1) Regional DN (End side): Different regions of the DN belong to different operating stakeholders (i.e., energy company). Denote $\mathbb { D } = \{ 1 , \dots , d , \dots , D \}$ as the set of =different areas. Smart sensors in each area collect the raw 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/69b8cb8ca63129ab0dd5dc037200d2f5a5a5f8a328a495c1de01c2eac20b13d5.jpg)



Fig. 2. Architecture of the end-edge-cloud collaboration-based FDIA detection framework. $\textcircled{1}$ : The cloud center initializes the global detection model. $\textcircled{2}$ : The cloud center sends global detection model parameters to edge devices. $\textcircled{3}$ : The edge devices collect raw data from smart sensors. $\textcircled{4}$ : The edge devices train the local detection model. $\textcircled{5}$ : The edge devices upload the local detection model parameters to the cloud center. $\textcircled{6}$ : The cloud center aggregates the local detection model and updates the global detection model.


measurement data and then upload the data to the corresponding edge device for local FDIA detection model training. 

2) Edge devices (Edge side): They are computing and storage devices owned by different stakeholders. Denote $\mathbb { M } = \{ 1 , \dots , m , \dots , M \}$ as the set of edge devices. The =edge devices are connected to the smart sensors through the wireless network. Moreover, they are connected to the cloud center for the exchange of the parameters of the FDIA detection model. Accordingly, these edge devices receive the measurement data collected by smart sensors and train the local FDIA detection model after receiving the parameters of the latest global FDIA detection model from the cloud center. Then, the edge devices upload the local FDIA detection model parameters to the cloud center. 

3) Cloud center (Cloud side): The cloud center is responsible for building a comprehensive FDIA detection model by aggregating different local detection model parameters deployed on different edge devices. And finally, the cloud center would broadcast the updated global FDIA detection model parameters to all edge devices for the next round of training. Multiple rounds of interactions between the cloud center and edge devices are demanded in order to obtain a final “perfect” FDIA detection model. 

# B. FL-Based Edge-Cloud Collaboration Mechanism

As stated in Section III-A, the edge devices and cloud center need to interact continuously to obtain a perfect FDIA detection model, which requires an edge-cloud collaboration mechanism. FL enables the edge-cloud collaboration. Edge devices that control different areas can interact with the cloud center based on FL to realize the edge-cloud collaboration. 

The complete workflow of the edge-cloud collaboration mechanism is shown in Fig. 3. It includes six main steps, which are given as follows (see also Algorithm 1 for the workflow). 

$\textcircled{1}$ Initialize the global model: As a model aggregator, the cloud center first initializes the global FDIA detection model parameters such as initial weights $\omega _ { 0 }$ , loss function $F$ , and the learning rate $\eta$ . In order to learn the temporal 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/d4e19078adf47e470b7fb2f10f952df6e4e70b12ff73a2a74e924ec17488aa40.jpg)



Fig. 3. Complete workflow of the edge-cloud collaboration mechanism.


and spatial features of the measurement data, the TSGCN is employed as the attack detection model in this article. 

$\textcircled{2}$  Send global parameters to edge devices: The cloud center sends the latest global attack detection model parameters to each edge device, i.e., $\omega _ { c , 0 } ^ { m } \gets \omega _ { c }$ , where $\omega _ { c }$ is the global detection model weights computed by cloud center in the cth interaction and $\omega _ { c , 0 } ^ { m }$ is the initial local detection model weight of mth edge device in the cth interaction. 

$\textcircled{3}$ Collect the training data: The edge devices collect the raw measurement data from smart sensors in the corresponding area of DN. The measurement data include the active injection power and reactive injection power of each bus. 

$\textcircled{4}$ Train the local model: After receiving the global detection model, each edge device trains the local detection model locally with its own raw measurement data resource. The edge devices update the corresponding local FDIA detection model weight $\omega _ { c , e } ^ { m }$ as follows: 

$$
\omega_ {c, e} ^ {m} = \omega_ {c, e - 1} ^ {m} - \eta \nabla F _ {m} \left(\omega_ {c, e - 1} ^ {m}\right) \tag {3}
$$

where $\omega _ { c , e } ^ { m }$ is the weight of local FDIA detection model of mth edge device at the eth epoch in the cth interaction, $\nabla F _ { m } ( \omega _ { c , e - 1 } ^ { m } )$ is the gradient of the mth edge device with (respect to $\omega _ { c , e - 1 } ^ { m }$ , $\eta$ is the learning rate. The average loss $F _ { m } ( \omega _ { c , e - 1 } ^ { m } )$ of local detection model can be expressed as 

$$
F _ {m} \left(\omega_ {c, e - 1} ^ {m}\right) = \frac {1}{n _ {m}} \sum_ {i = 1} ^ {n _ {m}} \mathcal {L} \left(u _ {i}, y _ {i}; \omega_ {c, e - 1} ^ {m}\right) \tag {4}
$$

where $n _ { m }$ is the amount of raw data that mth edge device possesses, $\mathcal { L } ( u _ { i } , y _ { i } ; \omega _ { c , e - 1 } ^ { m } )$ denotes the loss of local ( ; )FDIA detection model using model parameter $\omega _ { c , e - 1 } ^ { m }$ applied to sample $( u _ { i } , y _ { i } )$ , $u _ { i }$ and $y _ { i }$ are defined as the ( )measurement data and the binary labels of a sample, respectively. 

$\textcircled{5}$ Upload model parameters to the cloud center: After the local attack detection model of each edge device is trained, each edge device will upload the local model parameters $\omega _ { c , E } ^ { m }$ to the cloud center for the model aggregation. The local TSGCN-based attack detection model on the edge side is described in Section IV. 

$\textcircled{6}$ Aggregate parameters: After each edge device sends the local attack detection model parameters $\omega _ { c , E } ^ { m } , m \in$ $\{ 1 , \dots , M \}$ to the cloud center, the cloud center aggregates the uploaded parameters and updates the global 


Algorithm 1: Edge-Cloud Collaboration Mechanism Based on FL.


Input: numbers of interaction round $C$ , local dataset of all edge devices $\{\mathcal{D}_m\mid m\in \mathbb{M}\}$ , number of epoch for local model training $E$ Output: a comprehensive FDIA detection model   
1 Initialization:   
2 a).the global model weights $\omega_0$ 3 b).the learning rate $\eta$ 4 c).the loss function $F$ 5 Procedure:   
6 for $c\leq C$ do   
7 Edge Device:   
8 for $m\in \mathbb{M}$ do   
9 $\omega_{c,0}^{m}\gets \omega_{c}$ for each local epoch $e\leq E$ do Local TSGCN-based FDIA detection model training: $\omega_{c,e}^{m}\gets \omega_{c,e - 1}^{m} - \eta \nabla F_{m}\left(\omega_{c,e - 1}^{m}\right)$ end Local FDIA detection model weights are uploaded to cloud centre   
17 end Cloud Server:   
19 $\omega_{c + 1}\gets \sum_{m = 1}^{M}\frac{n_m}{N}\omega_{c,E}^m$ The cloud centre sends the global FDIA detection model weights to all edge devices   
22 $c\gets c + 1$ 23 end   
24 return: a comprehensive FDIA detection model 

attack detection model parameters $\omega _ { c + 1 }$ as follows [27]: 

$$
\omega_ {c + 1} = \sum_ {m = 1} ^ {M} \frac {n _ {m}}{N} \omega_ {c, E} ^ {m} \tag {5}
$$

where $n _ { m }$ is the amount of raw measurement data that mth edge device possesses, $M$ denotes the total number of edge devices, $N$ is the total amount of measurement data that all edge devices have, $\omega _ { c + 1 }$ is the global FDIA detection model weight in the $( c + 1 ) \mathrm { t h }$ interaction, and ( + )it will be distributed back to each edge device for the next round of training. 

In order to find the optimal global attack detection model, the FL has to minimize the global function $F ( \omega _ { c } )$ 

$$
\min  _ {\omega} F \left(\omega_ {c}\right) := \sum_ {m = 1} ^ {M} \frac {n _ {m}}{N} F _ {m} \left(\omega_ {c}\right) \tag {6}
$$

where $F _ { m } ( \omega _ { c } )$ denotes the loss of local FDIA detection model ( )of the mth edge device with respect to global model parameter $\omega _ { c }$ . After several rounds of iterations between the cloud center and edge devices, a comprehensive attack detection model can finally be obtained. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/f05069e39932c97104dc7b095056e77b0483750a9620817c46675bbdd11de6fd.jpg)



Fig. 4. Implementation procedure of the proposed FDIA detection framework.


# C. Implementation of End-Edge-Cloud Collaboration-Based FDIA Detection Framework

The implementation procedure of the proposed FDIA detection framework is shown in Fig. 4. It includes the following two stages (i.e., model training and real-time detection). 

1) Model training (the blue part in Fig. 4): With the collected measurement data, the training process of the FDIA detection model is carried out on the cloud center and the edge devices through the edge-cloud collaboration mechanism described in Section III-B. Then, a comprehensive FDIA detection model can be obtained, which is used as the real-time FDIA detection model in each edge device. 

2) Real-time detection (the yellow part in Fig. 4): With the comprehensive FDIA detection model deployed on the edge devices, each edge device can perform FDIA detection on the collected real-time measurement data and determine whether FDIA exists in its control area. 

Remark 1: The comprehensive FDIA detection model is a data-driven model because the input of the comprehensive FDIA detection model is only the active injection power and reactive injection power of each bus. Specifically, the detection model only needs measurement data to determine whether there is FDIA in the DN, which indicates that the FDIA detection model is data-driven. 

# IV. FDIA DETECTION MODEL USING TSGCN ON EDGE SIDE

In this section, the TSGCN-based local FDIA detection model deployed on the edge side is introduced. First, the temporal features are extracted using long-short term memory (LSTM). Then, the spatial features extraction based on graph convolutional network (GCN) is described in detail. At last, the overall local FDIA detection model deployed on the edge side is presented. 

The structure of the proposed local FDIA detection model deployed on the edge device is shown in Fig. 5. It consists of one input layer, one LSTM layer, two GCN layers, one dense layer, and one output layer. Two channel input $[ P , Q ]$ is represented as $X ^ { 0 } \in \mathbb { R } ^ { 2 * T * s }$ , where $P$ and $Q$ [ ]are the active injection power and reactive injection power, respectively. $T$ denotes the time 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/a7fbc26ff917a0ea2fb3f2336082f87fbf5ac7273c3972a9badd15f7db1d1f62.jpg)



Fig. 5. Structure of the proposed TSGCN-based FDIA detection model on the edge side.


window size and $s$ represents the bus numbers owned by the corresponding edge device. $X ^ { l }$ denotes the output of hidden layer l, and $Y$ denotes the output of TSGCN. 

# A. Extracting Temporal Features of Measurement Data Using LSTM

First, the measurement data $X ^ { 0 }$ in the input layer are fed into the LSTM network to extract the temporal features on each bus over time. LSTM is a special recurrent neural network (RNN), which can perform better than ordinary RNN in longer sequences [28]. 

The structure of LSTM is shown in Fig. 6. It consists of memory cells with self-connection, which can enable the learning of long-term temporal information. As shown in Fig. 6, the memory cell contains the input, forget, and output gate. The output of the memory cell at time step $t - 1$ will be used as the input of the memory cell at time step t. Specifically, given the previous hidden state $h _ { t - 1 }$ and the new input $x _ { t }$ at time step $t$ , we can get the forget gate $f _ { t }$ 

$$
f _ {t} = \sigma \left(W _ {f} \left[ h _ {t - 1}; x _ {t} \right] + b _ {f}\right) \tag {7}
$$

where $W _ { f }$ is the weighted matrices and $b _ { f }$ is the bias vector, $[ h _ { t - 1 } ; x _ { t } ]$ is a longer vector connected by $h _ { t - 1 }$ and xt, σ denotes [ ; ]the nonlinear activation function sigmoid. The closer $f _ { t }$ is to 0, the less information is retained about the last memory cell state $\nu _ { t - 1 }$ . Then, the input gate $i _ { t }$ is calculated with $x _ { t }$ and $h _ { t - 1 }$ , which can be expressed as 

$$
i _ {t} = \sigma \left(W _ {i} \left[ h _ {t - 1}; x _ {t} \right] + b _ {i}\right) \tag {8}
$$

where $W _ { i }$ is the weighted matrices and $b _ { i }$ is the bias vector. At the same time, the memory cell generates a candidate cell state $\tilde { \nu _ { t } }$ using $h _ { t - 1 }$ and $x _ { t }$ , as $\tilde { \nu } _ { t } = \mathrm { t a n h } ( W _ { \nu } [ h _ { t - 1 } ; x _ { t } ] + b _ { \nu } )$ . Then, ˜ ˜the new memory cell state $\nu _ { t }$ ( [ ; ] + )can be computed by adding the candidate cell state $\tilde { \nu _ { t } }$ and partially forgetting the last memory cell state $\nu _ { t - 1 }$ 

$$
\nu_ {t} = f _ {t} \otimes \nu_ {t - 1} + i _ {t} \otimes \tilde {\nu} _ {t} \tag {9}
$$

where $\otimes$ is the entrywise product. Finally, the output gate $o _ { t }$ can be obtained as 

$$
o _ {t} = \sigma \left(W _ {o} \left[ h _ {t - 1}; x _ {t} \right] + b _ {o}\right) \tag {10}
$$

where $W _ { o }$ is the weighted matrices and $b _ { o }$ is the bias vector. With the output gate $o _ { t }$ and the new memory cell state $\nu _ { t }$ , the new hidden state $h _ { t }$ (i.e., the final output of the memory cell which denotes the temporal features) is defined as 

$$
h _ {t} = o _ {t} \otimes \tanh  (\nu_ {t}). \tag {11}
$$

The input $X ^ { 0 }$ of the LSTM can be expressed as $X ^ { 0 } = [ x _ { 1 }$ $x _ { 2 } , \ldots , x _ { T } ]$ . According to (7)–(11), each $x _ { t }$ = [corresponds to 

one $h _ { t }$ . Thus, the output $X ^ { 1 }$ of the LSTM network (i.e., the temporal features of the input data $X ^ { 0 }$ ) is denoted as $X ^ { 1 } = [ h _ { 1 }$ $h _ { 2 } , \ldots , h _ { T } ]$ . 

# B. Extracting Spatial Features of Measurement Data Using GCN

After extracting temporal features using LSTM, the output $X ^ { 1 }$ of the LSTM is fed into GCN for spatial feature extraction. 

First, we organize the DN as an undirected, connected weighted graph $G$ , which is represented as $G = ( V , \Phi , A )$ . $\Phi$ = ( Φ ) Φdenotes a finite set of branches, representing transmission lines in DN. $V$ denotes the vertices of the graph, representing the buses in DN. $A$ is a weighted adjacency matrix, representing the line admittances in DN. We use the modulus of the bus admittance matrix $B _ { \mathrm { b u s } }$ (i.e., $| B _ { \mathrm { b u s } } | )$ of the corresponding DN to represent the weighted adjacency matrix $A$ . 

Similar to the classical Fourier transform, GCN applies a convolution operation to input signals. According to the literature [29], the graph convolution can be written as 

$$
\rho = \sum_ {k = 0} ^ {K - 1} \zeta_ {k} \psi_ {k} (\tilde {L}) \mu \tag {12}
$$

where $\mu$ and $\rho$ denote the input and the output of the graph convolution, respectively, $K$ denotes the kernel size of the graph convolution, i.e., the maximum radius of the convolution from the central bus, $\zeta _ { k }$ denotes the polynomial coefficient of order $k , \tilde { L }$ can be expressed as $\tilde { L } = 2 L / \lambda _ { \mathrm { m a x } } - I _ { n } , L$ is the Laplacian =matrix, which can be denoted as $L = I _ { n } - \Lambda ^ { - 1 / 2 } A \Lambda ^ { - 1 / 2 }$ , $\Lambda$ =represents the diagonal degree matrix with $\begin{array} { r } { \Lambda _ { i i } = \sum _ { j } A _ { i j } } \\ { . } \end{array}$ , $I _ { n }$ is an identity matrix, $\lambda _ { \mathrm { m a x } }$ Λ =denotes the largest eigenvalue of the Laplacian matrix $L$ , and $\psi _ { k } ( \tilde { L } )$ is the Chebyshev polynomial of order $k$ . 

Kipf and Welling [30] limit the $K$ to 1 and assume that $\lambda _ { \operatorname* { m a x } } \approx$ 2 for the purpose of making the parameters of the neural network more adaptable to the change in scale during training. Then, a deeper GCN model is built to extract spatial features. Equation (12) can be simplified to 

$$
\rho = \theta \left(I _ {n} + \Lambda^ {- \frac {1}{2}} A \Lambda^ {- \frac {1}{2}}\right) \mu = \theta \left(\tilde {\Lambda} ^ {- \frac {1}{2}} \tilde {A} \tilde {\Lambda} ^ {- \frac {1}{2}}\right) \mu \tag {13}
$$

where $\theta$ denotes the filter parameters, $\begin{array} { r } { \tilde { \Lambda } _ { i i } = \sum _ { j } \tilde { A } _ { i j } } \end{array}$ , ${ \tilde { A } } = A +$ $I _ { n }$ Λ = = +, respectively. By using (13), the graph convolution operation extracts spatial information from the first-order neighbors of each bus in DN. 

In this article, the TSGCN consists of two GCN layers. The output $X ^ { 1 }$ of the LSTM layer is fed into the first GCN layer, then we can get the output $X ^ { 2 }$ of the first GCN layer as 

$$
X ^ {2} = \tanh  \left(\theta^ {1} \left(\tilde {\Lambda} ^ {- \frac {1}{2}} \tilde {A} \tilde {\Lambda} ^ {- \frac {1}{2}}\right) X ^ {1}\right) \tag {14}
$$

where $\theta ^ { 1 }$ denotes the filter parameters of the first GCN layer. The graph convolution module uses the tanh function as the activation function which is defined as ta $\mathfrak { h } ( x ) = e ^ { x } - e ^ { - x } / e ^ { x } + e ^ { - x }$ . Similarly, the output $X ^ { 2 }$ ( ) = +of the first GCN layer is fed into the second GCN layer, and then, the output of the second GCN layer can be obtained as 

$$
X ^ {3} = \tanh  \left(\theta^ {2} \left(\tilde {\Lambda} ^ {- \frac {1}{2}} \tilde {A} \tilde {\Lambda} ^ {- \frac {1}{2}}\right) X ^ {2}\right). \tag {15}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/7255a2e0f21d85ca432690a76654dc7619cc13ef856227516b2768c2cbe22b7d.jpg)



Fig. 6. Structure of LSTM.



TABLE I ARCHITECTURE PARAMETERS OF FDIA DETECTION MODEL ON THE EDGE SIDE


<table><tr><td>Layer</td><td>LSTM</td><td>GCN 1</td><td>GCN 2</td><td>Dense</td></tr><tr><td>Input</td><td>2*296*s</td><td>296*s</td><td>128*s</td><td>32*s</td></tr><tr><td>Number of hidden units</td><td>1</td><td>128</td><td>32</td><td>2</td></tr><tr><td>Activation</td><td>tanh</td><td>tanh</td><td>tanh</td><td>sigmoid</td></tr><tr><td>Output</td><td>1*296*s</td><td>128*s</td><td>32*s</td><td>2</td></tr></table>

Based on (14) and (15), GCN implements spatial feature extraction on the temporal features $X ^ { 1 }$ and finally obtains temporal–spatial features $X ^ { 3 }$ . 

# C. Overall Structure of the FDIA Detection Model Based on TSGCN

The structure of the proposed TSGCN-based FDIA detection model is shown in Fig. 5. The parameters of each hidden layer in TSGCN are shown in Table I. The FDIA detection model proposed in this article includes six layers (four hidden layers). 

1) One Input Layer: The input data $X ^ { 0 }$ include the active injection power $P$ and reactive injection power $Q$ of each bus in the control area of each edge device. The dimension of $X ^ { 0 }$ is $2 * T * s$ . In this article, the time window $T$ is set to 296. 

2) One LSTM Layer (Hidden Layer): The LSTM layer includes 1 hidden units. The LSTM layer allows us to extract the temporal features of the input data $X ^ { 0 }$ using (7)–(11). The dimension of the output $X ^ { 1 }$ of the LSTM layer is $1 * 2 9 6 * s$ . 

3) Two GCN Layers (Hidden Layer): The number of hidden units in the two GCN layers is 128 and 32, respectively. With the GCN layers, we can achieve the extraction of spatial features based on (14) and (15) and, finally, get temporal–spatial features $X ^ { 3 }$ . The dimension of $X ^ { 3 }$ is $3 2 * s$ . 

4) One Dense Layer (Hidden Layer): With the temporal– spatial features $X ^ { 3 }$ , the output $X ^ { 4 }$ of the dense layer is represented by $X ^ { 4 } = \sigma ( W ^ { 4 } X ^ { 3 } + b ^ { 4 } )$ in which $b ^ { 4 }$ is the bias term, $W ^ { 4 }$ = (is the weights and $\sigma$ + )is the nonlinear sigmoid activation function: $\sigma ( x ) \bar { = } 1 / ( 1 + e ^ { - x } )$ . The dimension of $X ^ { 4 }$ is 2. 

5) ( ) = ( + ) One Output Layer: The output $Y = \operatorname* { m a x } ( X ^ { 4 } )$ can indi-= (cate whether the buses in DN have been attacked. 

Because the goal of the TSGCN-based FDIA detection model in this article is to determine whether the FDIA exists in the DN, the loss function (4) is defined as the cross-entropy loss function 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/b21c605002fe76feae70f20772624faf9673f7c7fbeee58da5c3efb8f4f12ed8.jpg)



Fig. 7. IEEE 14-bus distribution system with 3 PVs, 2 WTs, and 11 loads for simulations.


and it can be written as 

$$
F _ {m} \left(\omega_ {c}\right) = \frac {1}{n _ {m}} \sum_ {i = 1} ^ {n _ {m}} \left[ \left(1 - y _ {i}\right) \log \left(1 - \tilde {y} _ {i}\right) + y _ {i} \log \left(\tilde {y} _ {i}\right) \right] \tag {16}
$$

where $\tilde { y _ { i } }$ is the output of the proposed FDIA detection model ˜for sample $i$ and $y _ { i }$ is the actual value for sample $i$ that indicates whether the DN is attacked. 

# V. SIMULATION

In this section, the effectiveness of the proposed method is validated on the modified IEEE 14-bus and IEEE 118-bus distribution systems. The modified IEEE 14-bus distribution system is shown in Fig. 7, which includes 3 PVs, 2 WTs, and 11 loads. All simulations are conducted in MATLAB 2021a, Pycharm 2019, Python 3.7, Pytorch 10.1, and Matpower 7.1 on a PC with AMD R7 5800X CPU, NVIDIA 3080Ti GPU and 32 GB of RAM. 

# A. Dataset Generation and Configuration

With regard to the generation of normal measurement data, we first use the 5-min real-time load and generation data from Elia [31] in 2018 to represent the active output of the distributed resources and load demand in the modified IEEE 14-bus and IEEE 118-bus distribution systems. Second, we run the power flow program based on Matpower [32] to obtain the system states (i.e., voltage amplitude and voltage phase angle) and the measurement data (i.e., active injection power and reactive injection power) of each bus. Finally, we combine the measurement data at time $t$ with the measurement data at 295 times before time t to form a sample. Furthermore, in this article, we assume that there are 2 and 4 stakeholders for the modified IEEE 14-bus 


TABLE II DETAILED NUMBER OF BUSES AND THE DATA DIMENSION OWNED BY EACH STAKEHOLDER


<table><tr><td>Test System</td><td>Owner ID</td><td>Bus Number</td><td>Data dimension</td></tr><tr><td rowspan="3">IEEE 14-bus</td><td>0</td><td>4</td><td>2*296*4</td></tr><tr><td>1</td><td>10</td><td>2*296*10</td></tr><tr><td>Centralized</td><td>14</td><td>/</td></tr><tr><td rowspan="5">IEEE 118-bus</td><td>0</td><td>26</td><td>2*296*26</td></tr><tr><td>1</td><td>35</td><td>2*296*35</td></tr><tr><td>2</td><td>38</td><td>2*296*38</td></tr><tr><td>3</td><td>19</td><td>2*296*19</td></tr><tr><td>Centralized</td><td>118</td><td>/</td></tr></table>


TABLE III DEFINITION OF TP, FP, TN, AND FN


<table><tr><td></td><td>Attacked Data</td><td>Normal Data</td></tr><tr><td>detected as attack data</td><td>TP</td><td>FP</td></tr><tr><td>detected as normal data</td><td>FN</td><td>TN</td></tr></table>

and IEEE 118-bus distribution systems, respectively. Taking the modified IEEE 14-bus distribution system as an example, as shown in Fig. 7, buses 2, 5, 6, and 7 belong to stakeholder $^ { 1 , }$ and buses 1, 3, 4, 8, 9, 10, 11, 12, 13, and 14 belong to stakeholder 2. Thus, the dimension of data in each sample owned by stakeholder 1 is $2 * 2 9 6 * 4$ , where 2 means that each bus has two measurements, 4 represents the number of buses belonging to stakeholder 1, and 296 is the time window size. The dimension of data in each sample owned by stakeholder 2 is $2 * 2 9 6 * 1 0$ . Likewise, the IEEE 118-bus distribution system is governed by four stakeholders. The detailed number of buses and the data dimension owned by each stakeholder is shown in Table II. 

As for the generation of the FDIA dataset, the attack vector a can be obtained based on (1). With the attack vector $a$ , we can get the tampered measurement data $z _ { a }$ by adding $a$ to the normal measurement data (i.e., $z _ { a } = z + a )$ . The dimension of = +the FDIA dataset is the same as that of the normal dataset. 

Each stakeholder takes 106 220 samples from the normal dataset and FDIA dataset, respectively, to form their respective final dataset. The final entire dataset of each stakeholder consists of 212 440 samples. Each sample is composed of the active injection power and reactive injection power of each bus controlled by the corresponding stakeholder and binary labels to indicate whether the DN is attacked. We split the dataset of each stakeholder into two sections: 1) $70 \%$ for training and 2) $30 \%$ for testing the proposed detection model. 

# B. Experimental Setup

1) Model Parameters: The detailed structure of the local FDIA detection model has been explained in Section IV-C. The initial learning rate $\eta$ is set to 0.001 with a decay rate of 3e-4. The length $T$ of the time window for the input of LSTM is 296. The local attack detection model is trained for 10 epochs $E = 1 0$ ) =during each interaction. The number of interactions between cloud center and edge devices is set to 100. The loss function is chosen as the cross-entropy loss and the Adam optimizer is used as the optimizer for the update of the local FDIA detection model on the edge side. 


TABLE IV FDIA DETECTION RESULTS ON MODIFIED IEEE 14-BUS DISTRIBUTION SYSTEM WITH $\varepsilon = 0 . 2$


<table><tr><td>Training mode</td><td>accuracy</td><td>precision</td><td>recall</td><td>F1-score</td></tr><tr><td>Local</td><td>98.55%</td><td>100%</td><td>96.62%</td><td>98.28%</td></tr><tr><td>Proposed</td><td>99.87%</td><td>100%</td><td>99.69%</td><td>99.85%</td></tr><tr><td>Centralized</td><td>99.97%</td><td>100%</td><td>99.92%</td><td>99.96%</td></tr></table>


Bold values indicate the best performance. 



TABLE V FDIA DETECTION RESULTS ON MODIFIED IEEE 118-BUS DISTRIBUTION SYSTEM WITH $\varepsilon = 0 . 2$


<table><tr><td>Training mode</td><td>accuracy</td><td>precision</td><td>recall</td><td>F1-score</td></tr><tr><td>Local</td><td>95.78%</td><td>98.08%</td><td>90.88%</td><td>94.34%</td></tr><tr><td>Proposed</td><td>98.78%</td><td>99.19%</td><td>97.04%</td><td>98.10%</td></tr><tr><td>Centralized</td><td>98.84%</td><td>98.11%</td><td>98.39%</td><td>98.25%</td></tr></table>


Bold values indicate the best performance. 


2) Evaluation Metrics: In this article, we use four evaluation indicators to evaluate the performance of the proposed FDIA detection method. The four evaluation indicators are defined as follows: accuracy $= \mathrm { T P + T N / F P + F N + T P + T N } ,$ $= \mathrm { T P + T N }$ precision $=$ $\mathrm { T P / F P + T P }$ =, recall $= \mathrm { T P } / \mathrm { F N + T P }$ =, and F1-score  2TP/ $2 \mathrm { T P } + \mathrm { F N } + \mathrm { F P }$ = =, where TP, TN, FP, and FN are defined in +Table III. 

# C. Experiment Results

1) Performance Comparison With Local and Centralized Detection Model: In order to prove the validity of the proposed edge-cloud collaboration mechanism, we first conduct the experiments to compare the performance of the proposed FDIA detection method with the local detection model and the centralized detection model. The local detection model is locally built on the edge side and only uses the local measurement data for training without interaction with other edge devices and cloud center. The centralized FDIA detection model is built on the cloud center and can use all the measurement data of the DN for training. Tables IV and V show the numerical results for the modified IEEE 14-bus and IEEE 118-bus distribution systems, respectively. It can be seen from Table IV that the proposed method basically outperforms the local FDIA detection model in all evaluation indicators except the precision. The other indicators increased by $1 . 3 2 \%$ , $3 . 0 7 \%$ , and $1 . 5 7 \%$ , respectively. The reason % % %is that the attackers design FDIA based on the global system model and parameters of the entire DN while the local FDIA detector can only use local measurement data for model training and cannot get the global information. The numerical results verify that the proposed method can achieve the aggregation of the local FDIA detection of different stakeholders without data sharing and, finally, obtain a comprehensive FDIA detection model, which has better detection performance than the local detection model. 

Besides, compared with the $9 9 . 9 7 \%$ accuracy, $1 0 0 \%$ precision, $9 9 . 9 2 \%$ recall, and $9 9 . 9 6 \%$ % %, F1-score in the centralized % %FDIA detection model, the proposed method can obtain $9 9 . 8 7 \%$ accuracy, $1 0 0 \%$ precision, $9 9 . 6 9 \%$ recall, and $9 9 . 8 5 \%$ %F1-score. % % %Similarly, from Table V, the accuracy, recall, and F1-score all show the same properties as above. It indicates that the proposed detection method suffers a small performance loss in exchange for privacy preservation of stakeholders and users in FDIA 


TABLE VI FDIA DETECTION RESULTS ON MODIFIED IEEE 118-BUS DISTRIBUTION SYSTEM WITH VARIABLE ε


<table><tr><td>ε</td><td>accuracy</td><td>precision</td><td>recall</td><td>F1-score</td></tr><tr><td>0.05</td><td>94.38%</td><td>92.58%</td><td>90.34%</td><td>91.45%</td></tr><tr><td>0.1</td><td>97.21%</td><td>99.24%</td><td>92.21%</td><td>95.60%</td></tr><tr><td>0.2</td><td>98.78%</td><td>99.19%</td><td>97.04%</td><td>98.10%</td></tr><tr><td>0.5</td><td>99.73%</td><td>99.84%</td><td>99.34%</td><td>99.59%</td></tr></table>


Bold values indicate the best performance. 


detection model training. Specifically, as stated in Section I, the proposed method conducts joint training of local FDIA detection model without sharing the local measurement data on the edge devices through the FL-based edge-cloud collaboration mechanism, which can protect the privacy of measurement data. On the other hand, the centralized method has to upload all measurement data to the cloud center for the training of the FDIA detection model. Although the centralized detection model achieves the best detection performance, it cannot effectively protect the data privacy of stakeholders and users. In addition, in real-world situations, it is difficult to aggregate all measurement data in cloud center, which means that a centralized attack detection model is difficult to obtain. This shows that the proposed method has good applicability and can achieve performance close to the centralized FDIA detection model. 

Furthermore, it can be seen from Table V that our proposed method is not only applicable to small-scale systems but also applicable to large-scale systems. 

2) Performance Comparison With Variable ε: As mentioned in Section II-A, the smaller the value of $\varepsilon$ , the less likely it is to be detected by the bad data detection mechanism. In this part, we carry out the experiments to evaluate the performance of the proposed method with different thresholds $\varepsilon$ . Four groups of experiments are conducted, where different thresholds $\varepsilon = 0 . 0 5$ , =0.1, 0.2, and 0.5 are, respectively, considered. The results are presented in Table VI. It depicts the variation of the evaluation metrics of the proposed FDIA detection method on the IEEE 118-bus distribution system when the threshold $\varepsilon$ varies from 0.05 to 0.5. From Table VI, we can observe that the proposed method achieves good performance when the threshold is large. The detection accuracy, precision, recall, and F1-score grow from $9 4 . 3 8 \%$ , $9 2 . 5 8 \%$ , $9 0 . 3 4 \%$ , and $9 1 . 4 5 \%$ to $9 9 . 7 3 \%$ , $9 9 . 8 4 \%$ , $9 9 . 3 4 \%$ %, and $9 9 . 5 9 \%$ % % %with the increase of the threshold $\varepsilon$ %. The % %reason is that when the threshold $\varepsilon$ is small, the corresponding attack vector $a$ is small, which causes the tampered measurement data to be not much different from its actual value. This would result in an increase in FP and FN, which influences the performance of the proposed detection method. 

Furthermore, the convergence performances for the threshold value of 0.05, 0.1, 0.2, and 0.5 are shown in Fig. 8. It indicates that the proposed method can converge to the best performance after a certain number of iterations. From Fig. 8, we can see that when the threshold $\varepsilon = 0 . 5$ , the convergence rate is the fastest. =It also proves that the larger attack vectors caused by the larger threshold are easier to be detected by the proposed method. 

In addition, we conduct experiments at the threshold values of 0.01, 0.03, 0.15, 0.4, 0.5, and 0.6, and the experimental results are shown in Fig. 9. It shows that when the threshold $\varepsilon$ reaches 0.7, the accuracy and other evaluation metrics of the FDIA detection method proposed in this article all reach $1 0 0 \%$ , which shows that %the best scenario that the proposed method can tolerate is 0.7, 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/21b87fea565b557563deabf3055ce70e0666c0dc4a15c3af05dc4485c6f46b8d.jpg)



(a)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/36189f028532ab852965f7478099c37cfd3dc6ca081edc8168626b054ee11f98.jpg)



(b)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/2927d0d199f6b66fc22da323c7976142170bd2cf9f0cd93eb72ecfa838885142.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/b9a707db25b7107009579c99f23feafb3138ed9ee767d116d9d0fabfc7c13832.jpg)



(d)



Fig. 8. FDIA detection results on modified IEEE 118-bus distribution system with variable $\varepsilon$ . (a) Accuracy. (b) Precision. (c) Recall. (d) F1- score.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/b6b6ee8ac505e101e4d42abe8445e883ad26792210f47ead367e896d8d792155.jpg)



Fig. 9. FDIA detection results on modified IEEE 118-bus distribution system with variable ε.


and as long as the threshold exceeds 0.7, the proposed method can completely detect the FDIA. However, it is difficult to define the worst scenario that the proposed method can tolerate because the performance of the proposed method will inevitably decrease as the threshold value decreases, and there is no limit to the degree of decrease. Although the proposed method cannot detect 


TABLE VII COMPARISON OF PERFORMANCE AND COMPUTATIONAL EFFICIENCY WITH THE EXISTING METHODS


<table><tr><td rowspan="2">Reference</td><td colspan="5">IEEE 14-bus</td><td colspan="5">IEEE 118-bus</td></tr><tr><td>accuracy</td><td>precision</td><td>recall</td><td>F1-score</td><td>Computational efficiency</td><td>accuracy</td><td>precision</td><td>recall</td><td>F1-score</td><td>Computational efficiency</td></tr><tr><td>[14]</td><td>96.15%</td><td>91.30%</td><td>97.57%</td><td>94.33%</td><td>569.98s</td><td>97.25%</td><td>94.29%</td><td>96.96%</td><td>95.61%</td><td>6212.38s</td></tr><tr><td>[33]</td><td>98.61%</td><td>99.19%</td><td>96.42%</td><td>97.79%</td><td>701.25s</td><td>96.00%</td><td>93.82%</td><td>94.10%</td><td>93.96%</td><td>8100.67s</td></tr><tr><td>Proposed</td><td>99.87%</td><td>100%</td><td>99.69%</td><td>99.85%</td><td>366.25s</td><td>98.78%</td><td>99.19%</td><td>97.04%</td><td>98.10%</td><td>5761.59s</td></tr></table>


Bold values indicate the best performance. 


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/1f26f8f1ab1c98c657b567fed8f618708428194ee0a123eb22ba88e63df732f9.jpg)



Fig. 10. FDIA detection results on modified IEEE 118-bus distribution system with $\varepsilon = 0 . 5$ using different deep learning algorithms.


FDIA well when the threshold $\varepsilon$ is small, the corresponding lowintensity FDIA will not have large impact on DN. Conversely, the proposed method can effectively detect the high-intensity FDIA because the large change in measurement data can be easily captured. 

3) Performance Comparison With Local Different Detection Model: To further validate the performance of TSGCN in our proposed method, three other deep learning algorithms such as LSTM, convolutional neural network (CNN), and GCN are compared in this part. Each deep learning algorithm is trained under the framework of FL. We set the threshold $\varepsilon = 0 . 5$ . Fig. 10 =shows the results about the performance of different deep learning algorithms. It can be easily seen that the proposed method outperforms all the other methods on all evaluation metrics. The performance of Fed-CNN is the worst, with accuracy, precision, recall, and F1-score being $9 1 . 7 7 \%$ , $9 2 . 4 3 \%$ , $9 1 . 0 0 \%$ , and $9 1 . 7 1 \%$ % % %, respectively. Similarly, the performance of Fed-LSTM %and Fed-GCN are not as good as the proposed method, because these two methods only extract temporal or spatial features of the measurement data. On the contrary, the proposed method can fuse temporal–spatial features of measurement data and obtain the best detection performance. 

Besides, the convergence performances are shown in Fig. 11. As shown in Fig. 11, although the convergence speed of Fed-CNN is fast, its overall performance is poor and cannot detect FDIA accurately. The convergence speed of the proposed method comes after Fed-CNN and can finally achieve better performance than the other methods in the attack detection task. 

4) Performance Comparison With the Existing Works: In this part, for the purpose of proving the superiority of the proposed method, the GNN-based FDIA detector [14] and deep CNN-based FDIA detector [33] are compared with the proposed method. A comparison test is carried out on the modified IEEE 

14-bus and IEEE 118-bus distribution systems with $\varepsilon = 0 . 2$ . As =shown in Table VII, it can be observed that the proposed FDIA detection method can achieve the best detection performance compared with the existing methods. The main reason is that the proposed method can extract the temporal–spatial correlation features of the measurement data while the existing works do not consider the temporal–spatial correlation of measurement data. 

In addition, we compare the computational efficiency with the existing methods. It can be observed from Table VII that the computation time (i.e., data processing time and training time) of our proposed detection method on the modified IEEE 14-bus and IEEE 118-bus distribution systems is 366.25 s and 5761.59 s, respectively, while the computation time of other existing methods are 569.98 s, 6212.38 s, and 701.25 s, 8100.67 s. Thanks to the proposed end-edge-cloud collaboration architecture, which can make full use of the computational capacity of distributed edge devices, the proposed method can reduce the computational burden of cloud center and train the FDIA detection model both quickly and well. 

5) Robustness of the Proposed FDIA Detection Method: In this part, in order to verify the robustness of the proposed method to measurement noise, we add different levels of Gaussian noise to the measurement data. The added Gaussian noise is distributed with $( 0 , \beta )$ and $\beta$ varies from 0 to 0.2. The detection accuracy ( )of the proposed detection method and the existing methods under the influence of different levels of measurement noise is shown in Fig. 12. It can be seen from the figure that with the increase of noise level, the accuracy of the FDIA detection model also decreases. This is because as the noise level increases, the normal measurement data also deviates more and more from its true value, making the detection method difficult to distinguish between the tampered measurement data and the normal measurement data. In addition, it is easy to see from Fig. 12 that the performance of our proposed method is superior to other existing methods in the presence of noise. So, it can be said that the proposed FDIA detection method has strong robustness. 

# VI. CONCLUSION

In this article, for the purpose of ensuring the reliable operation of the DN, an end-edge-cloud collaboration-based framework is proposed to solve the problem of FDIA detection for the first time. Furthermore, an edge-cloud collaboration mechanism based on FL is proposed from the end-edge-cloud collaboration-based perspective, which can solve the problem of data island and preserve the privacy of users. Taking into account the temporal and spatial correlation of measurement data, we develop a novel TSGCN-based attack detection model. It can exploit both temporal and spatial features of measurement data. Simulation results on the modified IEEE 14-bus and IEEE 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/660d22620290399b4df85e207010e87976d238e0320aa1c5c4b3f1bdd69756dd.jpg)



(a)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/f6321fbfb49c428864f00bcc857e8dc395928127fa4f98a00238594308e69d2e.jpg)



(b)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/4762bd9ee63c84c613f9f5d3ec7b81ba8e7eb9e0aa79d301b1b357e2e875a898.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/cb435d6b9c65b1e832315fee3ba1bdc04b4a3ba19e12954c5c5f2b431bf6fb1f.jpg)



Fig. 11. FDIA detection results on modified IEEE 118-bus DN with $\varepsilon = 0 . 5$ using different model. (a) Accuracy. (b) Precision. (c) Recall. (d) F1-score.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/6f76ce9db3c9aa453dcd0939b398b6c322deb9a5a5cdb75ecfec3d39227bfd1c.jpg)



Fig. 12. Comparison of performance with the existing methods under different noise level.


118-bus distribution systems verify the high performance of the proposed method compared with some benchmark methods. In future work, we will focus on the localization of FDIA in DN. 

# REFERENCES



[1] W. Liu, Q. Gong, H. Han, Z. Wang, and L. Wang, “Reliability modeling and evaluation of active cyber physical distribution system,” IEEE Trans. Power Syst., vol. 33, no. 6, pp. 7096–7108, Nov. 2018. 





[2] P. L. Bhattar, N. M. Pindoriya, and A. Sharma, “A combined survey on distribution system state estimation and false data injection in cyber-physical power distribution networks,” IET Cyber-Phys. Syst.: Theory Appl., vol. 6, no. 2, pp. 41–62, 2021. 





[3] C.-W. Ten, G. Manimaran, and C.-C. Liu, “Cybersecurity for critical infrastructures: Attack and defense modeling,” IEEE Trans. Syst., Man, Cybern.—Part A: Syst. Humans, vol. 40, no. 4, pp. 853–865, Jul. 2010. 





[4] G. Liang, S. R. Weller, J. Zhao, F. Luo, and Z. Y. Dong, “The 2015 Ukraine blackout: Implications for false data injection attacks,” IEEE Trans. Power Syst., vol. 32, no. 4, pp. 3317–3318, Jul. 2017. 





[5] Y. Liu, P. Ning, and M. K. Reiter, “False data injection attacks against state estimation in electric power grids,” ACM Trans. Inf. Syst. Secur., vol. 14, no. 1, pp. 1–33, 2011. 





[6] L. Xie, Y. Mo, and B. Sinopoli, “Integrity data attacks in power market operations,” IEEE Trans. Smart Grid, vol. 2, no. 4, pp. 659–666, Dec. 2011. 





[7] K. Xiahou, Y. Liu, and Q. H. Wu, “Decentralized detection and mitigation of multiple false data injection attacks in multiarea power systems,” IEEE J. Emerg. Sel. Topics Ind. Electron., vol. 3, no. 1, pp. 101–112, Jan. 2022. 





[8] X. Wang, X. Luo, M. Zhang, Z. Jiang, and X. Guan, “Detection and isolation of false data injection attacks in smart grid via unknown input interval observer,” IEEE Internet Things J., vol. 7, no. 4, pp. 3214–3229, Apr. 2020. 





[9] J. J. Yan, G.-H. Yang, and Y. Wang, “Dynamic reduced-order observerbased detection of false data injection attacks with application to smart grid systems,” IEEE Trans. Ind. Informat., vol. 18, no. 10, pp. 6712–6722, Oct. 2022. 





[10] C. Chen et al., “Data-driven detection of stealthy false data injection attack against power system state estimation,” IEEE Trans. Ind. Informat., vol. 18, no. 12, pp. 8467–8476, Dec. 2022. 





[11] L. Yang, Y. Li, and Z. Li, “Improved-elm method for detecting false data attack in smart grid,” Int. J. Elect. Power Energy Syst., vol. 91, pp. 183–191, 2017. 





[12] C. Dou, D. Wu, D. Yue, B. Jin, and S. Xu, “A hybrid method for false data injection attack detection in smart grid based on variational mode decomposition and OS-ELM,” CSEE J. Power Energy Syst., vol. 8, no. 6, pp. 1697–1707, Nov. 2022. 





[13] E. Drayer and T. Routtenberg, “Detection of false data injection attacks in smart grids based on graph signal processing,” IEEE Syst. J., vol. 14, no. 2, pp. 1886–1896, Jun. 2020. 





[14] O. Boyaci et al., “Graph neural networks based detection of stealth false data injection attacks in smart grids,” IEEE Syst. J., vol. 16, no. 2, pp. 2946–2957, Jun. 2022. 





[15] A. S. Musleh, G. Chen, and Z. Y. Dong, “A survey on the detection algorithms for false data injection attacks in smart grids,” IEEE Trans. Smart Grid, vol. 11, no. 3, pp. 2218–2234, May 2020. 





[16] L. Cheng, H. Zang, Y. Xu, Z. Wei, and G. Sun, “Augmented convolutional network for wind power prediction: A new recurrent architecture design with spatial-temporal image inputs,” IEEE Trans. Ind. Informat., vol. 17, no. 10, pp. 6981–6993, Oct. 2021. 





[17] Z. Zhang, Y. Zhang, D. Yue, C. Dou, X. Ding, and H. Zhang, “Economicdriven hierarchical voltage regulation of incremental distribution networks: A cloud-edge collaboration based perspective,” IEEE Trans. Ind. Informat., vol. 18, no. 3, pp. 1746–1757, Mar. 2022. 





[18] Z. Su et al., “Secure and efficient federated learning for smart grid with edge-cloud collaboration,” IEEE Trans. Ind. Informat., vol. 18, no. 2, pp. 1333–1344, Feb. 2022. 





[19] J. Zhang, Y. Wang, K. Zhu, Y. Zhang, and Y. Li, “Diagnosis of interturn short-circuit faults in permanent magnet synchronous motors based on few-shot learning under a federated learning framework,” IEEE Trans. Ind. Informat., vol. 17, no. 12, pp. 8495–8504, Dec. 2021. 





[20] X. Zhang, F. Fang, and J. Wang, “Probabilistic solar irradiation forecasting based on variational Bayesian inference with secure federated learning,” IEEE Trans. Ind. Informat., vol. 17, no. 11, pp. 7849–7859, Nov. 2021. 





[21] X. Wu, L. You, R. Wu, Q. Zhang, and K. Liang, “Management and control of load clusters for ancillary services using internet of electric loads, based on cloud-edge-end distributed computing,” IEEE Internet Things J., vol. 9, no. 19, pp. 18267–18279, Oct. 2022. 





[22] Y. Wang, Y. Zhu, and J. Qin, “Research on intelligent distribution network architecture based on end-edge-cloud collaborative computing,” Front. Sci. Eng., vol. 1, no. 4, pp. 83–89, 2021. 





[23] X. Wang, B. Yang, Z. Wang, Q. Liu, C. Chen, and X. Guan, “A compressed sensing and CNN-based method for fault diagnosis of photovoltaic inverters in edge computing scenarios,” IET Renewable Power Gener., vol. 16, no. 7, pp. 1434–1444, 2022. 





[24] M. Esmalifalak, G. Shi, Z. Han, and L. Song, “Bad data injection attack and defense in electricity market using game theory study,” IEEE Trans. Smart Grid, vol. 4, no. 1, pp. 160–169, Mar. 2013. 





[25] Y. Lin and A. Abur, “A highly efficient bad data identification approach for very large scale power systems,” IEEE Trans. Power Syst., vol. 33, no. 6, pp. 5979–5989, Nov. 2018. 





[26] M. R. Mengis and A. Tajer, “Data injection attacks on electricity markets by limited adversaries: Worst-case robustness,” IEEE Trans. Smart Grid, vol. 9, no. 6, pp. 5710–5720, Nov. 2018. 





[27] H. B. McMahan, E. Moore, D. Ramage, and B. A. y Arcas, “Federated learning of deep networks using model averaging,” 2016, arXiv:1602.05629. 





[28] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural Computation, vol. 9, no. 8, pp. 1735–1780, 1997. 





[29] B. Yu, H. Yin, and Z. Zhu, “Spatio-temporal graph convolutional networks: A deep learning framework for traffic forecasting,” 2017, arXiv:1709.04875. 





[30] T. N. Kipf and M. Welling, “Semi-supervised classification with graph convolutional networks,” 2016, arXiv:1609.02907. 





[31] Elia Open Data, 2022. [Online]. Available: https://opendata.elia.be/pages/ home/ 





[32] R. D. Zimmerman, C. E. Murillo-Sánchez, and R. J. Thomas, “MAT-POWER: Steady-state operations, planning, and analysis tools for power systems research and education,” IEEE Trans. Power Syst., vol. 26, no. 1, pp. 12–19, Feb. 2011. 





[33] S. Wang, S. Bi, and Y.-J. A. Zhang, “Locational detection of the false data injection attack in a smart grid: A multilabel classification approach,” IEEE Internet Things J., vol. 7, no. 9, pp. 8218–8227, Sep. 2020. 



![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/7df28a44248c108df3b90810832de84b044eaa7f1c9bccd9e7b5799ae824c57e.jpg)


Dong Yue (Fellow, IEEE) received the Ph.D. degree in control theory and control engineering from the South China University of Technology, Guangzhou, China, in 1995. 

He is currently a Professor and the Dean of the Institute of Advanced Technology for Carbon Neutrality, the Dean of the College of Automation and Artificial Intelligence, and the Director of the Academic Committee of the University, Nanjing University of Posts and Telecommunication. His current research interests include 

networked control, optimization, multiagent systems, and smart grid. 

Dr. Yue was the recipient of the 2022 IEEE Rudolf Chope Research and Development Award, the Norbert Wiener Review Award by IEEE/CAA JOURNAL OF AUTOMATICA SINICA in 2020, and the Best Paper Award of IEEE SYSTEMS JOURNAL in 2022. He was the Chair of the IEEE IES Technical Committee on NCS and Applications. He was the Co-Editor-in-Chief for IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS and the Associate Editor for IEEE INDUSTRIAL ELECTRONICS MAGAZINE, IEEE TRANSACTIONS ON SYSTEMS, MAN, AND CYBERNETICS: SYSTEMS, IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS, IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS, and Journal of the Franklin Institute. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/038df23c2bfb0eb0ac7c658748161a01412b70717d5eadeb2b9ca999a1e495da.jpg)


Gerhard P. Hancke (Life Fellow, IEEE) received the B.Sc., B.Eng., and M.Eng. degrees in electronic engineering from the University of Stellenbosch, Stellenbosch, South Africa, in 1970, 1970, and 1973, respectively, and the Ph.D. degree in electronic engineering from the University of Pretoria, Pretoria, South Africa, in 1983. 

He is currently a Professor with the Nanjing University of Posts and Telecommunications, Nanjing, China, and also with the University of Pretoria and is recognized internationally as a 

Pioneer and the Leading Scholar of Industrial Wireless Sensor Networks Research. He initiated and coedited the first Special Section on Industrial Wireless Sensor Networks in IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS in 2009 and IEEE TRANSACTIONS ON INDUSTRIAL INFORMAT-ICS in 2013. 

Dr. Hancke has been an Associate Editor and the Guest Editor for IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS, IEEE ACCESS, and previously the IEEE TRANSACTIONS ON INDUSTRIAL ELECTRONICS. He is currently the Editor-in-Chief of IEEE TRANSACTIONS ON INDUSTRIAL INFORMATICS. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/5d21e59a8a81f84eed1a0abcf5fb01b2d25391b3d512874580d22aed86ede37f.jpg)


Houjun Li received the B.S. degree in measurement and control technology in 2020 from the College of Automation and Artificial Intelligence, Nanjing University of Posts and Telecommunications, Nanjing, China, where he is currently working toward the Ph.D. degree in information acquisition and control. 

His current research interests include graph neural networks, federated learning, and the application of artificial intelligence in power systems. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/fc02de7c5b5739821bfce4af2c6f7db4439e4d2648f0f0d41fbb2add9d6f3841.jpg)


Chunxia Dou (Senior Member, IEEE) received the Ph.D. degree in control theory and control engineering from the Institute of Electrical Engineering, Yanshan University, Qinhuangdao, China, in 2005. 

In 2010, she joined the Department of Engineering, Peking University, Beijing, China, where she was a Postdoctoral Fellow for two years. Since 2015, she has been a Professor with the Institute of Advanced Technology for Carbon Neutrality, Nanjing University of 

Posts and Telecommunications. Her current research interests include multiagent-based control, event-triggered hybrid control, distributed coordinated control, and multimode switching control and their applications in power systems, microgrids, and smart grids. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/b6e712677c5eede170d288602707c8a6f9ec79f21649fb6b3e557172686e7a91.jpg)


Zeng Zeng received the B.S. and M.S. degrees in computer application technology from Nanjing University, Nanjing, China, in 2008 and 2011, respectively. 

He is currently a Senior Engineer with State Grid Jiangsu Electric Power Company, Ltd., Information Communication Branch, Nanjing. His current research interests include power Internet of Things and edge computing. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/aa16b5b5d6ba5daf2b15f5c123964093ffcac57f726fd6ebecee8598e765a1cf.jpg)


Wei Guo received the Ph.D. degree in electrical engineering from North China Electric Power University, Beijing, China, in 2020. 

Since 2020, he has been with State Grid Hebei Economic Research Institute, Shijiazhuang, China. His research interests include microgrid optimal operation and energy storage application technology. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-03-21/fc5309d4-a392-4700-a0db-989c65b799a2/1ad1afa552941a8bd21be83297c9affca5a674591c54eb1e4fd3c66a942b745e.jpg)


Lei Xu is currently working toward the Ph.D. degree in information acquisition and control with the Nanjing University of Posts and Telecommunications, Nanjing, China. 

His current research interests include modeling, operation, and control of energy storage and plug-in electric vehicles. 