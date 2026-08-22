# CES 2026 반도체 기술 딥리서치 보고서

**작성 기준일:** 2026-08-21  
**행사:** CES 2026, 2026-01-06~09, 미국 라스베이거스  
**분석 범위:** CES 2026에서 공식 발표·시연·수상작 전시된 기술 가운데 반도체 **소자·공정·패키징·센서·가속기**와 직접 연결되는 12개 독립 사례

---

## 0. 경영진 요약

CES 2026의 반도체 메시지는 단순한 “AI PC 성능 경쟁”이 아니었다. 실제 기술 축은 다음 세 층으로 나뉜다.

1. **트랜지스터와 전력 전달의 구조 변화:** Intel 18A의 GAA(RibbonFET)와 후면 전력 공급(PowerVia)은 미세화의 병목을 소자 구조와 배선 구조를 함께 바꾸어 해결하려는 대표 사례다.
2. **이종 소자·센서의 고기능화:** SiC 전력 MOSFET, 저지연 MEMS IMU, 실리콘 기반 RGB OLEDoS, SPAD 기반 dToF가 차량·XR·로봇의 물리 인터페이스를 구성한다.
3. **패키징·공정 인프라의 재설계:** 유리 코어, 초고순도 공정가스 필터, 식각 장비 내부의 온디바이스 AI는 칩 밖의 재료·오염·운영 데이터가 수율과 시스템 성능을 좌우한다는 사실을 보여준다.

가장 성숙한 사례는 이미 양산 공정과 제품 출하 일정이 제시된 **Intel Core Ultra Series 3/18A**, 2026년 1분기 공급이 예고된 **AMD Ryzen AI 400**, 2026년 상반기 기기 탑재가 예고된 **Snapdragon X2 Plus**다. 반면 **DEEPX DX-M2**, **CuFlat-PKGCore**, **AetherCore**, **DutchBoy S**는 공개된 독립 검증 데이터가 부족하므로, 높은 연구 잠재력과 별개로 파일럿·프로토타입 단계로 평가해야 한다.

> **핵심 팩트체크:** CES Innovation Awards 페이지의 성능 문구는 원칙적으로 출품사가 제출한 설명이다. CTA 수상 자체는 기술의 상업적 성숙도나 성능 수치를 독립 시험한 결과가 아니다. CES 참가사 AGC의 공식 안내에도 CTA가 출품 설명의 정확성을 검증하거나 제품을 시험하지 않았다고 명시돼 있다([AGC CES 2026 안내](https://www.agc.com/en/ces/)). 따라서 본 보고서는 해당 수치를 모두 **“출품사 주장”**으로 표시한다.

---

## 1. 조사 방법과 판정 기준

### 1.1 포함 기준

- CES 2026 공식 행사 기간과 연결된 회사 공식 발표, 공식 시연 또는 CES 2026 Innovation Awards 페이지가 존재할 것.
- 반도체 소자, 제조 공정, 패키징, 센서, 가속기 아키텍처와의 기술적 연결을 구체적으로 설명할 수 있을 것.
- 단순 완제품 기능 소개보다 소자·재료·공정 변수가 연구 문제로 환원되는 사례를 우선할 것.
- 서로 다른 물리 소자나 공정 원리를 가진 사례를 독립 항목으로 구성할 것.

### 1.2 증거 위계

| 등급 | 근거 | 본 보고서의 처리 |
|---|---|---|
| A | 회사·학회·저널의 1차 원문, DOI 원문 | 사실 또는 해당 주체의 공식 발표로 서술 |
| B | CES/CTA 공식 제품·수상 페이지 | CES 참여·수상 사실은 확인, 성능은 출품사 주장으로 제한 |
| C | 후속 회사 공식 제품 페이지 | 현재 상태·사양 변경 확인에 사용 |
| D | 제3자 기사·유통 정보 | 핵심 결론에는 사용하지 않음 |

### 1.3 성숙도와 연구가치 척도

- **성숙도 M1:** 개념/로드맵, **M2:** 실험실 시제품, **M3:** 고객 샘플·파일럿, **M4:** 양산 진입/제한 출하, **M5:** 대규모 상용화.
- **연구가치 1~5:** 독립 연구로 다룰 수 있는 물리 변수, 공개되지 않은 병목, 산업 파급력을 함께 평가한 정성 점수.
- 논문은 제품 회사가 직접 인용했다는 의미가 아니다. 별도 확인이 없는 한 모든 논문은 **본 보고서가 작동 원리와 병목을 연결하기 위해 선정한 독립 학술 근거**다.

---

## 2. 기술 사례별 심층 분석

## 2.1 Samsung Display — 1.4형 5,000 PPI RGB OLEDoS 헤드셋 시연

### 공식 CES 정보

- **공식 제목:** “A New Era of Experience, Powered by AI & Display” 내 RGB OLEDoS 헤드셋
- **날짜/유형:** 2026-01-06~09 / 고객 대상 비공개 전시에서 헤드셋 폼팩터 시연
- **1차 출처:** [Samsung Display CES 2026](https://news.samsungdisplay.com/34419), [SID 2025 선행 공개](https://news.samsungdisplay.com/34337)

### 기술 설명

**목적.** XR 광학계에서 시야각과 각해상도를 높이고 screen-door effect를 줄이려면 수천 PPI의 밝고 작은 패널이 필요하다. 동시에 광학계 손실을 상쇄할 휘도와 색재현, 구동 백플레인의 데이터 처리 능력이 필요하다.

**작동과 구성.** OLEDoS(OLED-on-Silicon)는 유리 TFT가 아니라 CMOS 실리콘 백플레인 위에 OLED 발광층을 형성한다. 이번 패널은 백색 OLED와 컬러필터 방식이 아니라 R/G/B 서브픽셀이 직접 발광하는 **RGB direct emission**을 사용한다. 색필터 흡수 손실을 줄일 잠재력이 있지만, 미세 패턴에서 서로 다른 유기 발광재료를 정밀 증착해야 한다.

**차별점과 공개 성능.** 1.4형, 5,000 PPI, 120 Hz, DCI-P3 최대 99%, 최대 15,000 nit가 회사의 공식 공개 수치다. CES 2026의 새로움은 이 패널을 **실제 헤드셋 형태로 시연**했다는 점이다. 패널 자체는 2025년 SID에서 이미 공개되었으므로 “CES 2026 최초 5,000 PPI 패널”로 쓰면 부정확하다.

**소자·공정 관계.** CMOS 픽셀 회로의 면적, OLED 서브픽셀 패터닝 오차, 유기층 손상, 봉지와 열, 마이크로렌즈/광학 결합이 함께 수율과 휘도를 정한다. 5,000 PPI에서 픽셀 피치는 약 5.08 μm이므로 서브픽셀과 격벽·배선을 더 작은 치수로 구현해야 한다.

**한 줄 요약:** 삼성의 CES 시연은 5,000 PPI RGB OLEDoS를 헤드셋에 통합한 진전이지만, 패널 최초 공개는 SID 2025였다는 구분이 필요하다.

### 관련 검증 논문

1. **R. Kaçar, R. B. Serin, E. Uçar, M. Artuç, A. Ülkü, B. Kınacı**, “OLED-on-Silicon (OLEDoS) Microdisplays: Technology Challenges, Design Considerations, and Adaptation in XR Ecosystem — Review,” *Next Nanotechnology*, 7, 100132, 2025. [DOI 10.1016/j.nxnano.2025.100132](https://doi.org/10.1016/j.nxnano.2025.100132).  
   **관련성:** OLEDoS 백플레인, 발광, 광학, 열과 XR 통합의 병목을 종합한다.
2. **C.-m. Kang, H. Lee**, “Recent Progress of Organic Light-Emitting Diode Microdisplays for AR/VR Applications,” *Journal of Information Display*, 23(1), 19–32, 2022. [DOI 10.1080/15980316.2021.1917461](https://doi.org/10.1080/15980316.2021.1917461).  
   **관련성:** OLED 마이크로디스플레이의 픽셀 구조·휘도·수명·색 방식의 상충관계를 설명한다.
3. **Y. Tamatsukuri et al.**, “5009-ppi, 10000-cd/m², OLED/OS/Si Structure Display with Built-in CPU and Display Driver,” *Journal of the Society for Information Display*, 33(5), 314–323, 2025. [DOI 10.1002/jsid.2058](https://doi.org/10.1002/jsid.2058).  
   **관련성:** 5,000 PPI급 OLED/실리콘 통합과 온칩 구동의 실현 가능성을 직접 보여준다.

### 병목과 개발 과제

- RGB 미세 패터닝의 shadowing·혼색·파티클 결함과 대면적 수율.
- 청색 OLED 수명, 고휘도 열화, burn-in 및 픽셀 간 균일도.
- CMOS 백플레인 전류 정확도, 데이터 대역폭, 고휘도에서의 전력·열.
- 광학계의 pancake 손실, 시선추적 기반 foveated rendering과의 시스템 최적화.

### 현재 상태·브리프

- **상태:** M2~M3. 고성능 패널과 헤드셋 데모는 확인되지만, 고객 제품 양산·출하 시점은 공개되지 않았다.
- **반도체 직접성:** 높음 — 실리콘 CMOS 백플레인과 유기 발광 소자의 이종집적.
- **연구가치:** 5/5 — 패터닝·수명·열·광학을 연결하는 다학제 과제다.

---

## 2.2 STMicroelectronics — VL53L9 2.3k-zone dToF 3D LiDAR

### 공식 CES 정보

- **공식 제목:** “ST VL53L9 Time-of-Flight Sensor”
- **날짜/유형:** 수상 페이지 공개일 미표기; CES 행사 2026-01-06~09 / Innovation Awards Honoree, Embedded Technologies·수상작 전시
- **1차 출처:** [CES 수상 페이지](https://www.ces.tech/ces-innovation-awards/2026/st-vl53l9-time-of-flight-sensor/), [ST 제품 페이지](https://www.st.com/en/imaging-and-photonics-solutions/vl53l9cx.html), [2024년 최초 발표](https://newsroom.st.com/media-center/press-item.html/p4608.html), [2026년 양산 발표](https://newsroom.st.com/media-center/press-item.html/p4783.html)

### 기술 설명

**목적.** 로봇·카메라·스마트 인프라에 주변광과 피사체 색의 영향이 작은 절대 깊이 지도를 소형 모듈로 제공하는 것이 목적이다.

**작동과 구성.** VCSEL에서 짧은 광 펄스를 조사하고, SPAD(single-photon avalanche diode) 배열에서 광자의 도착시간 히스토그램을 측정해 거리 \(d=c\Delta t/2\)를 계산한다. 모듈은 조명 광학, SPAD 수신기, time-to-digital 변환, 히스토그램 처리와 보정 기능을 통합한다. 약 2,300개 거리 존, 2D IR 영상과 3D 깊이를 동시에 제공하며 외부 호스트의 계산 부담을 줄이는 온칩 처리가 핵심이다.

**차별점과 공개 성능.** CES 페이지는 5 cm~10 m, dual-scan flood illumination, 외부 캘리브레이션 불필요를 출품 설명으로 제시했다. 2026년 후속 공식 양산 사양은 5 cm~9 m, 최대 100 fps, 54°×42° FoV, 약 1° 각해상도다. 범위가 10 m에서 9 m로 바뀐 것은 측정 조건·최종 제품 규격의 정제 가능성을 시사하며, 두 숫자를 혼용하면 안 된다.

**소자·공정 관계.** SPAD의 photon detection probability, dark-count rate, afterpulsing, dead time, 픽셀 간 crosstalk와 TDC bin width가 거리 정밀도와 전력에 직결된다. 3D 적층 또는 고밀도 결합은 광검출층과 디지털 처리층을 독립 최적화할 수 있게 한다.

**한 줄 요약:** VL53L9은 SPAD·TDC·광원·온칩 처리까지 묶은 2.3k-zone dToF 모듈이며, CES는 최초 발표가 아니라 수상·상용화 전환을 보여준 무대였다.

### 관련 검증 논문

1. **E. Charbon**, “Single-Photon Imaging in Complementary Metal Oxide Semiconductor Processes,” *Philosophical Transactions of the Royal Society A*, 372, 20130100, 2014. [DOI 10.1098/rsta.2013.0100](https://doi.org/10.1098/rsta.2013.0100).  
   **관련성:** CMOS SPAD의 작동, 배열화, 잡음과 시간분해능의 기초를 설명한다.
2. **C. Niclass, M. Soga, H. Matsubara, S. Kato, M. Kagami**, “A 100-m Range 10-Frame/s 340×96-Pixel Time-of-Flight Depth Sensor in 0.18-μm CMOS,” *IEEE Journal of Solid-State Circuits*, 48(2), 559–572, 2013. [DOI 10.1109/JSSC.2012.2227607](https://doi.org/10.1109/JSSC.2012.2227607).  
   **관련성:** SPAD 배열, 시간상관, 픽셀/프레임 속도/거리의 트레이드오프를 실리콘으로 검증한다.
3. **J. Kostamovaara, S. S. Jahromi, P. Keränen**, “Temporal and Spatial Focusing in SPAD-Based Solid-State Pulsed Time-of-Flight Laser Range Imaging,” *Sensors*, 20, 5973, 2020. [DOI 10.3390/s20215973](https://doi.org/10.3390/s20215973).  
   **관련성:** 태양광 배경과 제한된 광자 예산에서 시공간 집중이 측정 범위와 정밀도를 개선하는 원리를 다룬다.

### 병목과 개발 과제

- 강한 주변광에서의 pile-up, multi-path interference, 낮은 반사율 물체의 photon starvation.
- SPAD DCR·afterpulsing·crosstalk와 온도 변화.
- VCSEL eye safety 한계 안에서 범위·프레임률·FoV를 동시에 확보하는 문제.
- 다중 센서 간 간섭, 투명·반사 표면, 움직임 왜곡과 캘리브레이션.

### 현재 상태·브리프

- **상태:** CES 당시 M3, 2026-06-22 공식 발표 기준 M4~M5. ST는 2026년 7월 초 대량생산을 예고했다.
- **반도체 직접성:** 최상 — SPAD/TDC 이미징 소자와 광전자 통합.
- **연구가치:** 5/5 — 통계 광자처리, 소자 잡음, 광학·알고리즘 공동최적화가 가능하다.

---

## 2.3 DEEPX — DX-M2 Physical AI 로드맵과 DX-H1 V-NPU

### 공식 CES 정보

- **공식 제목:** “CES 2026 Media Briefing: DEEPX Unveils Physical AI Vision Roadmap” 및 “DX-H1 V-NPU”
- **날짜/유형:** 2026-01-06 / 로드맵 발표·시연; CES 2026 Innovation Awards Honoree(Embedded Technologies)
- **1차 출처:** [DEEPX 미디어 브리핑](https://deepx.ai/ces-2026-media-briefing-deepx-unveils-physical-ai-vision-roadmap/), [DX-H1 CES 수상 페이지](https://www.ces.tech/ces-innovation-awards/2026/dx-h1-v-npu/), [DX-H1 제품 페이지](https://deepx.ai/products/dx-h1-v-npu/)

### 기술 설명

**목적.** 로봇·카메라·산업 장비에서 네트워크 연결 없이 대규모 비전·멀티모달 모델을 낮은 전력으로 실행하고, 데이터센터 전송량과 지연을 줄이는 것이 목표다.

**작동과 구성.** DX-H1은 여러 비디오 스트림의 CNN/비전 추론을 병렬 처리하는 PCIe형 V-NPU 가속기다. 제품 페이지는 카드당 50 TOPS, 약 40 W, 최대 64채널을 제시한다. DX-M2는 MoE와 압축·희소성을 이용해 필요한 expert만 활성화하고 메모리 이동을 줄여 20B~100B급 모델을 5 W 미만에서 처리하겠다는 차세대 로드맵이다.

**차별점과 공개 성능.** CES 수상 설명은 1,000채널 처리에 GPU 40개·약 9,200 W 대신 DX-H1 카드 16개·560 W가 필요하다고 주장한다. DX-M2의 100B/5 W와 데이터센터 트래픽 80% 감소 역시 회사의 목표·추정치다. 모델 구조, 정밀도, 컨텍스트 길이, 토큰/s, DRAM 구성, 정확도 손실과 열 조건이 공개되지 않아 동등 비교로 볼 수 없다.

**소자·공정 관계.** NPU의 에너지는 MAC 횟수보다 SRAM/DRAM 이동, NoC, 희소성 불균형, 양자화와 메모리 대역폭에 크게 좌우된다. 2 nm급 공정 계획은 누설과 배선 전력, SRAM scaling, 패키지 메모리의 실제 효과를 함께 검증해야 한다.

**한 줄 요약:** DEEPX는 비전 NPU의 상용화와 100B급 초저전력 Physical AI 로드맵을 제시했지만, 핵심 수치는 아직 동등 조건의 독립 벤치마크가 필요하다.

### 관련 검증 논문

1. **V. Sze, Y.-H. Chen, T.-J. Yang, J. S. Emer**, “Efficient Processing of Deep Neural Networks: A Tutorial and Survey,” *Proceedings of the IEEE*, 105(12), 2295–2329, 2017. [DOI 10.1109/JPROC.2017.2761740](https://doi.org/10.1109/JPROC.2017.2761740).  
   **관련성:** NPU 에너지의 핵심이 연산보다 데이터 이동·메모리 계층·데이터플로에 있음을 정량적으로 정리한다.
2. **Y.-H. Chen, T. Krishna, J. S. Emer, V. Sze**, “Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks,” *IEEE Journal of Solid-State Circuits*, 52(1), 127–138, 2017. [DOI 10.1109/JSSC.2016.2616357](https://doi.org/10.1109/JSSC.2016.2616357).  
   **관련성:** 데이터 재사용과 row-stationary dataflow가 엣지 가속기의 전력을 줄이는 방법을 실측한다.
3. **N. P. Jouppi et al.**, “In-Datacenter Performance Analysis of a Tensor Processing Unit,” *ISCA 2017*, 2017. [DOI 10.1145/3079856.3080246](https://doi.org/10.1145/3079856.3080246).  
   **관련성:** 특화 행렬연산기, 온칩 메모리와 워크로드별 활용률을 실제 추론 시스템에서 비교한다.

### 병목과 개발 과제

- 100B급 모델에서 온칩 SRAM 용량과 외부 메모리 대역폭·용량의 물리적 한계.
- 희소 MoE의 expert imbalance, 라우팅 지연, 작은 batch에서의 낮은 PE 활용률.
- TOPS가 아닌 모델별 tokens/s/W, 정확도, 지연 P99, 메모리 전력의 공개.
- 컴파일러·연산자 지원, 양자화 안정성, 장기 공급과 안전 인증.

### 현재 상태·브리프

- **상태:** DX-H1 M3~M4, DX-M2 M1~M2. CES 페이지와 회사 자료는 제품·로드맵을 확인하지만 대규모 독립 고객 검증은 공개되지 않았다.
- **반도체 직접성:** 높음 — 전용 NPU 데이터패스·메모리·공정 설계.
- **연구가치:** 5/5 — 모델/하드웨어 공동설계와 공정-메모리 한계 검증에 적합하다.

---

## 2.4 NVIDIA — Vera Rubin 6칩 랙스케일 플랫폼

### 공식 CES 정보

- **공식 제목:** “NVIDIA Kicks Off the Next Generation of AI With Rubin”
- **날짜/유형:** 2026-01-05 / CES 플랫폼 발표
- **1차 출처:** [NVIDIA 공식 발표](https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer)

### 기술 설명

**목적.** 거대 MoE·추론형 AI·비디오 생성에서 단일 GPU 성능보다 랙 전체의 메모리·통신·네트워크를 하나의 컴퓨터로 최적화해 토큰당 비용을 낮추는 것이 목표다.

**작동과 구성.** CES 발표는 Vera CPU, Rubin GPU, NVLink 6 Switch, ConnectX-9, BlueField-4, Spectrum-6의 **6개 칩**을 한 플랫폼으로 묶었다. Rubin GPU는 3세대 Transformer Engine과 adaptive compression, NVFP4 추론 50 PFLOPS를 회사 사양으로 제시한다. NVLink 6는 GPU당 3.6 TB/s, NVL72 랙 집계 260 TB/s를 제공하고 in-network collective 연산을 지원한다.

**차별점과 공개 성능.** NVIDIA는 Blackwell 대비 토큰당 비용 최대 10분의 1, MoE 학습에 필요한 GPU 수 최대 4분의 1을 주장한다. 이는 모델, 정밀도, 소프트웨어 버전, 전력·네트워크 조건이 고정된 NVIDIA 내부 비교다. 또한 이후 발표의 “7-chip platform”과 CES 2026의 “6 chips”를 혼합하면 안 된다.

**소자·공정 관계.** 랙스케일 AI의 병목은 GPU 연산뿐 아니라 HBM 대역폭·용량, 패키지 신호 무결성, 스위치 SerDes 전력, 케이블, 냉각과 집단통신이다. 저정밀 연산은 실리콘 MAC 밀도를 높이지만 정확도와 스케일 관리가 필요하다.

**한 줄 요약:** Rubin은 GPU 한 개가 아니라 6종 반도체와 NVLink/HBM/네트워크를 공동설계해 AI 공장을 랙 단위로 최적화한 사례다.

### 관련 검증 논문

1. **S. Rajbhandari, J. Rasley, O. Ruwase, Y. He**, “ZeRO: Memory Optimizations Toward Training Trillion Parameter Models,” *SC20*, 2020. [DOI 10.5555/3433701.3433727](https://doi.org/10.5555/3433701.3433727).  
   **관련성:** 모델 상태를 분할해 대규모 학습의 메모리 중복을 줄이는 시스템 원리를 제시한다.
2. **A. Li, S. L. Song, J. Chen, J. Li, X. Liu, N. R. Tallent, K. J. Barker**, “Evaluating Modern GPU Interconnect: PCIe, NVLink, NV-SLI, NVSwitch and GPUDirect,” *IEEE Transactions on Parallel and Distributed Systems*, 31(1), 94–110, 2020. [DOI 10.1109/TPDS.2019.2928289](https://doi.org/10.1109/TPDS.2019.2928289).  
   **관련성:** GPU 연결 토폴로지와 NUMA 효과가 애플리케이션 성능을 제한하는 방식을 실측한다.
3. **D. U. Lee et al.**, “A 128Gb 8-High 512GB/s HBM2E DRAM with a Pseudo Quarter Bank Structure, Power Dispersion and an Instruction-Based At-Speed PMBIST,” *IEEE ISSCC*, 2020. [DOI 10.1109/ISSCC19947.2020.9062977](https://doi.org/10.1109/ISSCC19947.2020.9062977).  
   **관련성:** TSV 적층 HBM의 대역폭, 전력 분산과 테스트 구조를 보여줘 Rubin의 메모리 병목을 설명한다.

### 병목과 개발 과제

- HBM 용량·수율·열, 인터포저와 CoWoS급 패키징 공급.
- collective 통신의 topology-aware scheduling과 tail latency.
- NVFP4/adaptive compression의 모델별 정확도와 재현성.
- 랙 전력, 액체냉각, 광·전기 네트워크의 에너지와 서비스성.

### 현재 상태·브리프

- **상태:** M3~M4. NVIDIA는 플랫폼이 full production에 있고 파트너 제품은 2026년 하반기 제공 예정이라고 CES 발표에서 밝혔다. 실제 고객 대규모 가동 데이터는 아직 제한적이다.
- **반도체 직접성:** 높음 — GPU, CPU, 스위치, DPU, NIC와 패키지·메모리의 시스템 반도체 공동설계.
- **연구가치:** 5/5 — 소자보다 시스템·패키지·통신·냉각의 공동최적화 가치가 크다.

## 2.5 Intel — Core Ultra Series 3(Panther Lake)와 Intel 18A

### 공식 CES 정보

- **공식 제목:** “CES 2026: Intel Core Ultra Series 3 Debut — First Built on Intel 18A”
- **날짜/유형:** 2026-01-05 / CES 사전 제품 발표 및 플랫폼 데뷔
- **1차 출처:** [Intel Newsroom](https://newsroom.intel.com/client-computing/ces-2026-intel-core-ultra-series-3-debut-first-built-on-intel-18a), [Intel 18A 기술 페이지](https://www.intel.com/content/www/us/en/foundry/process/18a.html)

### 기술 설명

**목적.** 모바일 PC에서 CPU·GPU·NPU를 하나의 전력 한계 안에 넣으면서 성능/와트와 배터리 시간을 동시에 높이는 것이 목적이다. 동시에 Panther Lake는 Intel 18A의 실제 대량생산 가능성을 증명하는 선도 제품 역할을 한다.

**작동과 구성.** Intel이 공개한 상위 구성은 최대 16개 CPU 코어, 최대 12개 Xe GPU 코어, 50 TOPS NPU를 결합한다. 공정 측면의 핵심은 두 가지다.

- **RibbonFET:** 여러 개의 얇은 실리콘 나노리본 채널을 게이트가 사방에서 감싸는 GAA 구조다. FinFET보다 채널 전위를 더 잘 제어해 짧은 채널 효과와 누설을 줄이고, 저전압에서의 구동 여유를 키운다.
- **PowerVia:** 신호와 전력을 모두 전면 배선층에서 공급하던 구조에서 벗어나 전력을 웨이퍼 후면으로 전달한다. 전면 배선을 신호 라우팅에 더 많이 쓸 수 있고, 전원망의 IR drop과 동적 전압 강하를 줄인다.

**차별점과 공개 성능.** Intel은 Core Ultra Series 3가 동급 전력의 이전 세대 대비 멀티스레드 성능 최대 60%, 게임 성능 최대 77%, 특정 조건에서 배터리 27시간을 달성한다고 발표했다. 이는 Intel이 정의한 워크로드와 비교 조건의 **회사 측 수치**다. Intel 18A 페이지는 Intel 3 대비 동일 전력에서 최대 18% 성능 향상, 동일 성능에서 38% 전력 절감, 30% 밀도 개선을 주장한다. 공정 명칭의 “18A”는 물리 게이트 길이 1.8 nm를 뜻하는 직접 치수가 아니라 노드 브랜드다.

**소자·공정 관계.** GAA의 정전기 제어 이득만으로는 전력망 혼잡과 전압 강하를 제거할 수 없다. 반대로 후면 전력 공급만으로는 트랜지스터의 누설·저전압 구동 문제를 해결할 수 없다. Panther Lake의 연구적 의미는 GAA, 후면 전력, 설계기술 공동최적화(DTCO), 칩렛 패키징을 동일 제품에서 함께 검증한다는 데 있다.

**한 줄 요약:** Intel 18A는 GAA 트랜지스터와 후면 전력망을 결합해 “미세화”를 소자와 배선의 동시 혁신으로 바꾼 CES 2026의 가장 직접적인 선단공정 사례다.

### 관련 검증 논문

1. **N. Loubet et al.**, “Stacked Nanosheet Gate-All-Around Transistor to Enable Scaling Beyond FinFET,” *2017 Symposium on VLSI Technology*, 2017. [DOI 10.23919/VLSIT.2017.7998183](https://doi.org/10.23919/VLSIT.2017.7998183).  
   **관련성:** 적층 나노시트 GAA의 소자 구조와 FinFET 이후 스케일링 논리를 실험적으로 제시해 RibbonFET의 물리적 기반을 설명한다.
2. **J. Ryckaert et al.**, “Extending the Roadmap Beyond 3 nm through System Scaling Boosters: A Case Study on Buried Power Rail and Backside Power Delivery,” *2019 Electron Devices Technology and Manufacturing Conference*, 2019. [DOI 10.1109/EDTM.2019.8731234](https://doi.org/10.1109/EDTM.2019.8731234).  
   **관련성:** 매립 전원 레일과 후면 전력 전달이 셀 면적과 전원 무결성에 미치는 영향을 다룬다.
3. **D. Prasad et al.**, “Buried Power Rails and Back-side Power Grids: Arm CPU Power Delivery Network Design Beyond 5 nm,” *IEEE IEDM*, 2019. [DOI 10.1109/IEDM19573.2019.8993617](https://doi.org/10.1109/IEDM19573.2019.8993617).  
   **관련성:** CPU 블록 수준에서 후면 전력망의 IR drop·배선·면적 효과를 분석한다.

### 병목과 개발 과제

- GAA 리본 두께·폭·간격 변동에 따른 문턱전압 및 구동전류 분포.
- 후면 thinning, nano-TSV 정렬, 전력 비아 저항, 웨이퍼 휨과 열 방출의 동시 최적화.
- 저전압 성능 이득을 실사용 워크로드에서 유지하기 위한 SRAM Vmin과 전원 무결성.
- 공정 수율과 비용: 새로운 트랜지스터와 후면 공정을 동시에 도입하는 초기 수율 램프가 핵심 위험이다.

### 현재 상태·브리프

- **상태:** M4~M5. Intel은 18A가 2025년에 생산에 들어갔다고 밝히며, Core Ultra Series 3의 2026-01-06 예약 및 2026-01-27 글로벌 공급을 발표했다.
- **반도체 직접성:** 최상 — 트랜지스터, 배선, 공정 통합이 핵심.
- **연구가치:** 5/5 — GAA 변동성, 후면 전력, 열, 수율을 아우르는 다물리 연구가 가능하다.

---

## 2.6 Bosch — 750 V/1,200 V 듀얼채널 트렌치 SiC MOSFET·전력모듈

### 공식 CES 정보

- **공식 제목:** Bosch Semiconductors at CES 2026 — “Latest dual-channel SiC trench MOSFETs”
- **날짜/유형:** 2026-01-06~09 / 부스 16203 기술 전시
- **1차 출처:** [Bosch Semiconductors CES 2026](https://www.bosch-semiconductors.com/events/ces-2026.html)

### 기술 설명

**목적.** 전기차 인버터·온보드 충전기와 고효율 전력변환기에서 실리콘 IGBT보다 높은 스위칭 주파수, 낮은 손실, 높은 접합온도 운용을 달성하는 것이 목표다.

**작동과 구성.** 4H-SiC의 넓은 밴드갭과 높은 임계 전계는 같은 차단전압에서 더 얇고 고농도인 드리프트층을 허용한다. Bosch는 750 V와 1,200 V 등급의 트렌치 게이트 MOSFET과 이를 사용한 전력모듈을 전시했다. “듀얼채널” 트렌치 구조는 트렌치 측벽의 채널과 전계 분포를 설계해 낮은 온저항과 게이트 산화막 신뢰성 사이의 균형을 노린다.

**차별점과 공개 성능.** CES 공식 페이지는 독자적 advanced trench architecture와 두 전압 등급을 명시하지만, R\(_\mathrm{DS(on)}\), 칩 면적, 단락 내량, 반복 애벌랜치, 게이트 산화막 수명과 같은 비교 가능한 숫자는 공개하지 않았다. 따라서 “더 효율적”이라는 일반론을 제품 우위로 확정할 수 없다.

**소자·공정 관계.** 트렌치 깊이와 코너 형상, p-shield, 채널 이동도, SiC/SiO₂ 계면 트랩, 산화막 전계가 성능과 수명을 직접 결정한다. 모듈에서는 칩 자체보다 접합·기판·와이어/클립·열계면의 기생 인덕턴스와 열저항이 스위칭 성능을 제한할 수 있다.

**한 줄 요약:** Bosch의 CES 시연은 SiC 트렌치 MOSFET이 자동차 전력반도체의 주류로 이동했음을 보여주지만, 공개 수치만으로 경쟁 우위를 판정하기에는 부족하다.

### 관련 검증 논문

1. **T. Kimoto**, “Material Science and Device Physics in SiC Technology for High-Voltage Power Devices,” *Japanese Journal of Applied Physics*, 54, 040103, 2015. [DOI 10.7567/JJAP.54.040103](https://doi.org/10.7567/JJAP.54.040103).  
   **관련성:** SiC 재료 결함, 드리프트층, 계면 이동도와 고전압 소자의 기본 물리를 종합한다.
2. **K. Puschkarsky, T. Grasser, T. Aichinger, W. Gustin, H. Reisinger**, “Review on SiC MOSFETs High-Voltage Device Reliability Focusing on Threshold Voltage Instability,” *IEEE Transactions on Electron Devices*, 66(11), 4604–4616, 2019. [DOI 10.1109/TED.2019.2938262](https://doi.org/10.1109/TED.2019.2938262).  
   **관련성:** SiC/SiO₂ 계면 트랩과 바이어스 온도 스트레스에 따른 문턱전압 이동을 정리한다.
3. **A. J. Lelis, R. Green, D. B. Habersat**, “SiC MOSFET Threshold-Stability Issues,” *Materials Science in Semiconductor Processing*, 78, 32–37, 2018. [DOI 10.1016/j.mssp.2017.11.028](https://doi.org/10.1016/j.mssp.2017.11.028).  
   **관련성:** 실제 구동 조건에서 문턱전압 불안정성이 회로 설계와 신뢰성에 미치는 영향을 연결한다.

### 병목과 개발 과제

- 트렌치 코너의 산화막 전계 집중과 장기 TDDB.
- 계면 트랩에 의한 낮은 채널 이동도, 동적 R\(_\mathrm{DS(on)}\), 문턱전압 드리프트.
- 단락 내량과 낮은 도통손실의 상충관계.
- 고속 스위칭 시 모듈 기생성분, EMI, 게이트 오동작 및 열사이클 신뢰성.

### 현재 상태·브리프

- **상태:** M3~M4. CES는 실제 소자·모듈 전시를 확인하지만, 해당 페이지에는 양산 개시일과 고객 채택 수치가 없다.
- **반도체 직접성:** 최상 — 와이드밴드갭 전력소자와 트렌치 공정이 핵심.
- **연구가치:** 5/5 — 계면 신뢰성, 전계 설계, 모듈 다물리 최적화가 모두 미해결이다.

---

## 2.7 Bosch Sensortec — BMI5 MEMS IMU 플랫폼

### 공식 CES 정보

- **공식 제목:** “From immersive XR to advanced robotics and wearables: Bosch Sensortec launches BMI5 motion sensor platform”
- **날짜/유형:** 2026-01-05 / CES 제품군 출시 및 시연
- **1차 출처:** [Bosch Sensortec 공식 발표](https://www.bosch-sensortec.com/en/news/from-immersive-xr-to-advanced-robotics-and-wearables-bosch-sensortec-launches-bmi5-motion-sensor-platform.html)

### 기술 설명

**목적.** XR 헤드셋, 로봇, 웨어러블에서 회전·가속을 낮은 지연으로 감지하면서 진동, 전력, 동기화 오차를 줄이는 범용 관성센서 플랫폼이다.

**작동과 구성.** MEMS 가속도계는 관성력에 따른 proof mass 변위를 정전용량 변화로 읽고, MEMS 자이로는 진동 구조에 생기는 코리올리 힘을 검출한다. BMI5는 공통 MEMS 아키텍처를 바탕으로 BMI560(XR·OIS), BMI563(로봇·XR), BMI570(웨어러블)을 구성한다. 센서 내부의 programmable edge-AI classifier는 원시 움직임을 외부 프로세서로 계속 전송하지 않고 이벤트로 분류할 수 있다.

**차별점과 공개 성능.** Bosch는 0.5 ms 미만 지연, 약 0.6 μs 시간 증분, 1 ns 타이밍 해상도, 이전 대비 두 배 full-scale range, 낮은 노이즈와 높은 진동 강건성을 발표했다. 다만 각 수치의 시험 대역폭, 온도 범위, 축별 노이즈 밀도와 bias instability 조건은 CES 발표에 모두 제시되지 않았다.

**소자·공정 관계.** MEMS 공진 구조의 질량·스프링 상수·감쇠, 전극 간격, 패키지 진공도, ASIC의 아날로그 프런트엔드와 시간 동기화 회로가 최종 성능을 정한다. 로봇용에서는 단일 정적 노이즈보다 vibration rectification error와 장기 온도 드리프트가 더 큰 병목이 될 수 있다.

**한 줄 요약:** BMI5는 MEMS 구조, 초정밀 시간동기, 센서 내부 AI를 하나의 플랫폼으로 묶어 XR·로봇의 지연과 진동 문제를 겨냥한다.

### 관련 검증 논문

1. **N. Yazdi, F. Ayazi, K. Najafi**, “Micromachined Inertial Sensors,” *Proceedings of the IEEE*, 86(8), 1640–1659, 1998. [DOI 10.1109/5.704269](https://doi.org/10.1109/5.704269).  
   **관련성:** MEMS 가속도계·자이로의 구동과 검출 원리, 잡음원을 정립한 기초 리뷰다.
2. **C. Acar, A. M. Shkel**, “Inherently Robust Micromachined Gyroscopes With 2-DOF Sense-Mode Oscillator,” *Journal of Microelectromechanical Systems*, 15(2), 380–387, 2006. [DOI 10.1109/JMEMS.2006.872224](https://doi.org/10.1109/JMEMS.2006.872224).  
   **관련성:** 공정 변동과 대역폭에 강건한 자이로 구조 설계를 다뤄 BMI5의 진동 강건성 목표와 연결된다.
3. **W. A. Gill et al.**, “A Review of MEMS Vibrating Gyroscopes and Their Reliability Issues in Harsh Environments,” *Sensors*, 22, 7405, 2022. [DOI 10.3390/s22197405](https://doi.org/10.3390/s22197405).  
   **관련성:** 온도, 충격, 진동, 패키징이 자이로 신뢰성에 미치는 영향을 정리한다.

### 병목과 개발 과제

- 공정·온도 변화에 따른 quadrature error, bias instability, scale-factor drift.
- 고진동 로봇 환경에서 vibration rectification error와 공진 모드 결합.
- 센서·카메라·디스플레이 간 timestamp 보정과 clock drift.
- 엣지 분류기의 오탐/미탐, 모델 업데이트, 프라이버시 및 전력의 균형.

### 현재 상태·브리프

- **상태:** M3. 발표 시점에 샘플 제공, 2026년 3분기 대량생산 계획이 제시됐다. 기준일 현재 계획 시점은 진행 중이며 실제 HVM 달성 여부의 독립 확인 자료는 없다.
- **반도체 직접성:** 높음 — MEMS 구조와 센서 ASIC의 공동설계.
- **연구가치:** 4/5 — 공개 데이터셋을 이용한 진동·온도·AI 보정 실험 가치가 높다.

---

## 2.8 AMD — Ryzen AI 400/PRO 400과 2세대 XDNA 2 NPU

### 공식 CES 정보

- **공식 제목:** “AMD Expands AI Leadership Across Client, Graphics and Software with New Ryzen, Ryzen AI and AMD ROCm Announcements at CES 2026”
- **날짜/유형:** 2026-01-05 / CES 제품군 발표
- **1차 출처:** [AMD 공식 발표](https://ir.amd.com/news-events/press-releases/detail/1270/amd-expands-ai-leadership-across-client-graphics-and-software-with-new-ryzen-ryzen-ai-and-amd-rocm-announcements-at-ces-2026)

### 기술 설명

**목적.** 노트북에서 생성형 AI·영상·음성 모델을 클라우드에 보내지 않고 실행하면서 CPU/GPU의 전력과 메모리 부담을 줄이는 것이 목적이다.

**작동과 구성.** Ryzen AI 400/PRO 400은 최대 12개 Zen 5 CPU 코어, RDNA 계열 그래픽, 2세대 XDNA 2 NPU를 결합한다. NPU는 다수의 MAC, 로컬 메모리와 스트림 데이터플로를 이용해 행렬·텐서 연산을 CPU보다 높은 병렬성과 낮은 제어 오버헤드로 처리한다. 모델은 양자화와 그래프 컴파일을 거쳐 NPU 지원 연산자로 매핑되고, 지원되지 않는 연산은 CPU/GPU로 fallback될 수 있다.

**차별점과 공개 성능.** AMD의 최대 NPU 성능은 60 TOPS, CPU는 최대 12코어, configurable TDP는 15~54 W다. 60 TOPS는 이론 피크 연산량이며, 모델 지연·정확도·메모리 전력·연산자 활용률을 포함하지 않는다. 따라서 Snapdragon·Intel·DEEPX와 단순 TOPS 숫자만 비교해서는 안 된다.

**소자·공정 관계.** NPU의 실제 효율은 MAC 배열보다 SRAM 용량, NoC, 데이터 재사용, 정밀도, DRAM 전송과 SoC 전력관리에서 결정된다. 모바일 SoC에서는 NPU만 빠르게 만들면 패키지 온도와 메모리 대역폭 때문에 지속 성능이 제한될 수 있다.

**한 줄 요약:** Ryzen AI 400은 60 TOPS XDNA 2를 CPU·GPU와 결합한 상용 AI PC SoC지만, TOPS보다 모델별 지연·전력·정확도 공개가 더 중요하다.

### 관련 검증 논문

1. **V. Sze, Y.-H. Chen, T.-J. Yang, J. S. Emer**, “Efficient Processing of Deep Neural Networks: A Tutorial and Survey,” *Proceedings of the IEEE*, 105(12), 2295–2329, 2017. [DOI 10.1109/JPROC.2017.2761740](https://doi.org/10.1109/JPROC.2017.2761740).  
   **관련성:** 데이터플로·메모리 접근·정밀도가 DNN 가속기 효율을 좌우하는 원리를 제공한다.
2. **Y.-H. Chen, T.-J. Yang, J. S. Emer, V. Sze**, “Eyeriss v2: A Flexible Accelerator for Emerging Deep Neural Networks on Mobile Devices,” *IEEE Journal on Emerging and Selected Topics in Circuits and Systems*, 9(2), 292–308, 2019. [DOI 10.1109/JETCAS.2019.2910232](https://doi.org/10.1109/JETCAS.2019.2910232).  
   **관련성:** 모바일의 다양한 layer shape와 희소성을 처리하기 위한 유연한 NoC·압축 도메인 연산을 실증한다.
3. **V. Sze, Y.-H. Chen, T.-J. Yang, J. S. Emer**, “How to Evaluate Deep Neural Network Processors: TOPS/W (Alone) Considered Harmful,” *IEEE Solid-State Circuits Magazine*, 12(3), 28–41, 2020. [DOI 10.1109/MSSC.2020.3002140](https://doi.org/10.1109/MSSC.2020.3002140).  
   **관련성:** TOPS/W 하나로 NPU를 비교할 때 정밀도·활용률·메모리·워크로드가 누락되는 문제를 직접 지적한다.

### 병목과 개발 과제

- 동적 shape, attention, LLM KV-cache 등 비정형 워크로드의 NPU 활용률.
- CPU/GPU/NPU 사이 tensor 이동과 unified memory의 실제 전력·지연.
- INT8/INT4 양자화 시 모델 정확도, 연산자별 fallback, 소프트웨어 생태계.
- 15~54 W 범위에서 장시간 workload의 온도·팬 소음·성능 유지.

### 현재 상태·브리프

- **상태:** M4~M5. AMD는 2026년 1분기부터 주요 OEM 시스템 공급을 예고했다. 구체 모델별 출하와 지속성능은 OEM 구현에 좌우된다.
- **반도체 직접성:** 높음 — CPU/GPU/NPU 이종 SoC와 전력·메모리 공동설계.
- **연구가치:** 4/5 — 표준 모델의 에너지·지연·정확도를 재현 가능하게 비교할 필요가 크다.

---

## 2.9 Qualcomm — Snapdragon X2 Plus와 80 TOPS Hexagon NPU

### 공식 CES 정보

- **공식 제목:** “Empowering Professionals and Aspiring Creators: Snapdragon X2 Plus”
- **날짜/유형:** 2026-01-05 / CES 제품 발표
- **1차 출처:** [Qualcomm 공식 발표](https://www.qualcomm.com/news/releases/2026/01/empowering-professionals-and-aspiring-creators--snapdragon-x2-pl)

### 기술 설명

**목적.** 팬리스 또는 얇은 Windows PC에서 Arm CPU와 고성능 NPU를 결합해 로컬 AI, 배터리 시간과 범용 애플리케이션 성능을 동시에 확보하는 것이 목적이다.

**작동과 구성.** 3세대 Oryon CPU, Adreno GPU, Hexagon NPU가 이종 컴퓨팅을 구성한다. Hexagon은 행렬·벡터·스칼라 경로와 로컬 메모리를 사용해 양자화된 AI 그래프를 실행하며, 소프트웨어 런타임이 작업을 CPU/GPU/NPU 사이에 분배한다.

**차별점과 공개 성능.** Qualcomm은 80 TOPS NPU, 이전 세대 대비 단일 스레드 성능 최대 35% 향상, 같은 성능에서 전력 최대 43% 절감을 주장한다. 정확한 공정 노드와 die size는 해당 CES 발표에 공개되지 않았으므로 추정하지 않는다. “80 TOPS”는 정밀도와 workload가 같은 경우에만 비교 의미가 있다.

**소자·공정 관계.** 모바일 NPU는 데이터 재사용, 압축, 메모리 bank 충돌과 저전압 동작이 핵심이다. Arm PC에서는 x86 애플리케이션 에뮬레이션이나 드라이버가 NPU와 무관하게 시스템 전력·사용 경험을 제한할 수 있어, 칩 수준과 플랫폼 수준을 구분해야 한다.

**한 줄 요약:** Snapdragon X2 Plus는 80 TOPS Hexagon을 앞세운 Arm AI PC SoC로, 피크 성능보다 메모리 이동·연산자 지원·지속 전력의 검증이 핵심이다.

### 관련 검증 논문

1. **T. Chen, Z. Du, N. Sun, J. Wang, C. Wu, Y. Chen, O. Temam**, “DianNao: A Small-Footprint High-Throughput Accelerator for Ubiquitous Machine-Learning,” *ASPLOS 2014*, 2014. [DOI 10.1145/2541940.2541967](https://doi.org/10.1145/2541940.2541967).  
   **관련성:** 범용 모바일 추론을 위한 작은 신경망 가속기의 계산·메모리 분할 원리를 제시한다.
2. **X. Zhang, X. Zhou, M. Lin, J. Sun**, “ShuffleNet: An Extremely Efficient Convolutional Neural Network for Mobile Devices,” *IEEE CVPR*, 2018. [DOI 10.1109/CVPR.2018.00716](https://doi.org/10.1109/CVPR.2018.00716).  
   **관련성:** 채널 셔플과 group convolution으로 제한된 모바일 연산 예산에서 정확도를 유지하는 모델 측 공동설계를 보여준다.
3. **Y.-H. Chen, T.-J. Yang, J. S. Emer, V. Sze**, “Eyeriss v2: A Flexible Accelerator for Emerging Deep Neural Networks on Mobile Devices,” *IEEE JETCAS*, 9(2), 292–308, 2019. [DOI 10.1109/JETCAS.2019.2910232](https://doi.org/10.1109/JETCAS.2019.2910232).  
   **관련성:** 모바일 모델의 희소성과 다양한 계층 형상을 처리하는 하드웨어 유연성의 필요성을 입증한다.

### 병목과 개발 과제

- NPU 지원 연산자 범위와 CPU/GPU fallback 비용.
- KV-cache·대규모 모델의 메모리 용량/대역폭, 로컬 AI의 개인정보 보호 검증.
- Arm Windows 애플리케이션·드라이버 호환성과 하드웨어 성능의 분리 평가.
- 배터리·열 제한 아래에서의 장시간 tokens/s/W, 오디오·카메라 동시 처리.

### 현재 상태·브리프

- **상태:** M4. Qualcomm은 Snapdragon X2 Plus 탑재 기기를 2026년 상반기에 공급할 예정이라고 발표했다. 실제 OEM별 성능은 메모리·냉각·펌웨어에 따라 달라진다.
- **반도체 직접성:** 높음 — Arm CPU, GPU, NPU, 메모리와 전력관리 SoC.
- **연구가치:** 4/5 — 동일 모델·정밀도·전력계측을 사용한 플랫폼 비교가 필요하다.

---

## 2.10 CIT — CuFlat-PKGCore 초평탄 구리 증착 유리 패키지 코어

### 공식 CES 정보

- **공식 제목:** “CuFlat-PKGCore: Ultra-Flat Copper-Deposited Glass for Semiconductor Packaging”
- **날짜/유형:** 수상 페이지 공개일 미표기; CES 행사 2026-01-06~09 / Innovation Awards Honoree, Computer Hardware·수상작 전시
- **1차 출처:** [CES 수상 페이지](https://www.ces.tech/ces-innovation-awards/2026/cuflat-pkgcore-ultra-flat-copper-deposited-glass-for-semiconductor-packaging/)

### 기술 설명

**목적.** AI 가속기용 대형 패키지에서 유기 코어의 열팽창·휨·미세배선 한계를 줄이고, 고속 신호 손실을 낮출 수 있는 유리 코어와 평탄한 동박 계면을 제공하는 것이 목적이다.

**작동과 구성.** 유리는 낮은 유전손실과 우수한 치수 안정성을 제공하고, TGV(through-glass via)와 양면 재배선으로 칩렛·HBM을 연결할 수 있다. CuFlat-PKGCore는 화학 도금 대신 독자적 **건식 구리 증착**으로 유리 위에 얇고 평탄한 Cu를 형성한다고 설명한다. 표면 거칠기가 작으면 고주파에서 skin effect와 conductor loss를 낮출 잠재력이 있고, 미세선폭 RDL의 리소그래피 초점·접착 균일도에도 유리하다.

**차별점과 공개 성능.** CES 출품 설명은 NVIDIA AI 가속기 등에 쓰이는 HVLP4 대비 “HVLP6, 200배 더 평탄”, 기존보다 20°C 높은 온도에서도 안정적이라고 주장한다. 그러나 거칠기 단위, 측정 면적·필터, 접착력, peel strength, 주파수별 삽입손실, TGV 수율과 열사이클 표본 수가 공개되지 않았다. “NVIDIA에 채택”을 의미하는 문구도 아니다.

**소자·공정 관계.** 유리 core thickness, CTE, 탄성률, TGV 직경·pitch, Cu seed/adhesion layer, Cu grain과 표면 거칠기가 warpage·열·신호·수율을 함께 결정한다. 구리-유리 접착을 높이기 위한 거칠기 증가는 고주파 손실을 키울 수 있어 근본 상충이 존재한다.

**한 줄 요약:** CuFlat은 초평탄 건식 Cu/유리 계면으로 차세대 패키지의 신호와 치수 안정성을 노리지만, 공개 계측 데이터와 신뢰성 검증이 아직 부족하다.

### 관련 검증 논문

1. **V. Sukumaran et al.**, “Design, Fabrication and Characterization of Low-Cost Glass Interposers with Fine-Pitch Through-Package-Vias,” *IEEE ECTC*, 583–588, 2011. [DOI 10.1109/ECTC.2011.5898571](https://doi.org/10.1109/ECTC.2011.5898571).  
   **관련성:** 미세 pitch TPV와 유리 인터포저의 전기·열기계 가능성을 실증한다.
2. **V. Sukumaran, T. Bandyopadhyay, V. Sundaram, R. Tummala**, “Low-Cost Thin Glass Interposers as a Superior Alternative to Silicon and Organic Interposers for Packaging of 3-D ICs,” *IEEE Transactions on Components, Packaging and Manufacturing Technology*, 2(9), 1426–1433, 2012. [DOI 10.1109/TCPMT.2012.2204392](https://doi.org/10.1109/TCPMT.2012.2204392).  
   **관련성:** 유리의 CTE·치수 안정성·비용과 실리콘/유기 기판의 상충관계를 비교한다.
3. **V. Sukumaran et al.**, “Design, Fabrication, and Characterization of Ultrathin 3-D Glass Interposers With Through-Package-Vias at Same Pitch as TSVs in Silicon,” *IEEE Transactions on Components, Packaging and Manufacturing Technology*, 4, 786–795, 2014. [DOI 10.1109/TCPMT.2014.2303427](https://doi.org/10.1109/TCPMT.2014.2303427).  
   **관련성:** 30 μm 유리와 15 μm TPV, 20 GHz 손실을 통해 미세화와 취성·도금 난제를 직접 다룬다.

### 병목과 개발 과제

- 건식 Cu의 대면적 균일도, pinhole, 잔류응력과 glass adhesion.
- TGV drilling의 chipping·microcrack, Cu void와 plating 시간을 포함한 수율.
- 대형 패널의 warpage, handling, singulation, 열사이클·습열 신뢰성.
- 표면 거칠기와 접착력의 상충, 주파수 56/112/224 Gbps급 insertion loss 검증.

### 현재 상태·브리프

- **상태:** M2~M3 추정. CES 수상작은 확인되지만 고객 qualification, 월 생산능력, JEDEC 신뢰성 결과는 공개되지 않았다.
- **반도체 직접성:** 최상 — 패키지 기판 재료·금속화 공정.
- **연구가치:** 5/5 — 표면·접착·신호·열기계의 계면 연구 가치가 매우 높다.

---

## 2.11 IDeas — AetherCore 초고순도 공정가스 필터

### 공식 CES 정보

- **공식 제목:** “AetherCore: Ultra-Clean Gas Filtration for Next-Gen Semiconductor Manufacturing”
- **날짜/유형:** 수상 페이지 공개일 미표기; CES 행사 2026-01-06~09 / Innovation Awards Honoree·수상작 전시
- **1차 출처:** [CES 수상 페이지](https://www.ces.tech/ces-innovation-awards/2026/aethercore-ultra-clean-gas-filtration-for-next-gen-semiconductor-manufacturing/)

### 기술 설명

**목적.** CVD·ALD·식각 등에서 사용하는 초고순도 가스의 입자를 제거하면서 압력 강하와 필터 교체 주기를 줄여 결함·다운타임을 낮추는 것이 목적이다.

**작동과 구성.** 다공성 금속 필터는 서로 연결된 tortuous pore를 통해 입자를 표면·깊이에서 포집한다. AetherCore는 구형이 아닌 **flake형 금속 분말**과 조절 가능한 기공 구조를 사용한다고 설명한다. 얇고 넓은 입자는 소결 후 통로의 aspect ratio와 포집 표면적을 바꿔 높은 유량과 미세 포집을 동시에 노릴 수 있다.

**차별점과 공개 성능.** 출품 설명은 기존 99.99999% 대비 99.9999999% 제거, flow efficiency 40% 향상, 3주마다 교체, 다운타임 10%·노동 20% 감소를 주장한다. 하지만 시험 입자 크기·재료·농도, 가스 종류, 유량·압력, log reduction, 표본 수와 장기 shedding/outgassing가 공개되지 않아 수치의 재현성을 판단할 수 없다.

**소자·공정 관계.** 필터는 칩 내부 소자는 아니지만 파티클과 금속 오염이 박막 pinhole, pattern bridge, plasma 불안정과 수율 저하로 이어지는 전공정 핵심 부품이다. pore size distribution, porosity, tortuosity, 분말 형상, 소결온도와 압력이 효율·압력강하·강도·수명을 함께 정한다.

**한 줄 요약:** AetherCore는 flake형 금속분말의 기공 설계로 초고순도와 고유량을 함께 노리지만, 9-nine급 주장에는 입자 크기별 독립 시험이 필수다.

### 관련 검증 논문

1. **M. S. A. Heikkinen, N. H. Harley**, “Experimental Investigation of Sintered Porous Metal Filters,” *Journal of Aerosol Science*, 31(6), 721–738, 2000. [DOI 10.1016/S0021-8502(99)00550-9](https://doi.org/10.1016/S0021-8502(99)00550-9).  
   **관련성:** 소결 다공성 금속의 입자 penetration과 구조·유동 조건의 관계를 실험한다.
2. **A. Colorado, K. Vakhshoori**, “Is Your Gas Filter as Clean as You Think? Evaluation of UHP Gas Filters of Differing Membrane Types for Contamination Contribution,” *IEEE/SEMI Advanced Semiconductor Manufacturing Conference*, 2001. [DOI 10.1109/ASMC.2001.925628](https://doi.org/10.1109/ASMC.2001.925628).  
   **관련성:** 반도체용 UHP 필터 자체의 수분·금속·입자 오염 기여를 비교한다.
3. **M.-J. Kim, M.-J. Lee, H.-J. Kim, J.-Y. Kim, J.-W. Lee, J.-Y. Yun**, “Fabricating Metal Powder Filters with Material Extrusion Additive Manufacturing,” *Archives of Metallurgy and Materials*, 70(3), 1159–1163, 2025. [DOI 10.24425/amm.2025.154461](https://doi.org/10.24425/amm.2025.154461).  
   **관련성:** 반도체 가스용 금속분말 필터에서 분말 크기·소결온도·기공률·투과도를 연결한다.

### 병목과 개발 과제

- 1~10 nm급 입자에서 크기별 penetration curve와 most penetrating particle size 확인.
- 압력강하-유량-효율의 Pareto 관계, loading에 따른 수명과 pore blocking.
- 부식성·반응성 가스에서 금속 용출, outgassing, particle shedding.
- fab qualification, SEMI 표준 시험, lot 간 분말 형상·기공 분포 재현성.

### 현재 상태·브리프

- **상태:** M2~M3 추정. CES 수상 외에 실제 fab qualification과 대량 교체 이력은 공개되지 않았다.
- **반도체 직접성:** 높음 — 전공정 오염 제어와 수율을 좌우하는 핵심 소모품.
- **연구가치:** 5/5 — 기공 구조·에어로졸 수송·오염 분석의 정량 검증 여지가 크다.

---

## 2.12 AIBIZ — DutchBoy S 식각장비 온디바이스 AI

### 공식 CES 정보

- **공식 제목:** “DutchBoy S: Semiconductor Etch Equipment On-Device AI Platform”
- **날짜/유형:** 수상 페이지 공개일 미표기; CES 행사 2026-01-06~09 / Innovation Awards Honoree, Artificial Intelligence·수상작 전시
- **1차 출처:** [CES 수상 페이지](https://www.ces.tech/ces-innovation-awards/2026/dutchboy-s-semi-conductor-etch-equipment-on-device-ai-platform/)

### 기술 설명

**목적.** 식각 장비의 200개 이상 센서와 계측 시계열을 장비 근처에서 분석해 이상을 조기에 감지하고, 원인 후보를 엔지니어에게 설명하여 scrap과 다운타임을 줄이는 것이 목적이다.

**작동과 구성.** 장비의 chamber pressure, RF power/reflection, gas flow, temperature, endpoint/OES, valve와 MFC 신호를 동기화·정규화한 뒤 딥러닝 기반 anomaly detector가 정상 패턴과의 차이를 계산한다. root-cause visualization은 변수 중요도·시간구간·설비 부품을 연결해 경보를 설명한다. “온디바이스”는 원시 fab 데이터를 외부 클라우드로 보내지 않고 장비 로컬 appliance에서 처리한다는 의미다.

**차별점과 공개 성능.** CES 페이지는 200개 이상 센서, 실시간 분석, 원인 시각화를 설명하지만 정확도, false-alarm rate, detection delay, 처리 샘플링률, 실제 wafer yield 개선, fab 배치 수는 공개하지 않았다. 따라서 “실시간”과 “정확한 원인”을 정량 성능으로 확대해석할 수 없다.

**소자·공정 관계.** 식각 plasma는 recipe, chamber seasoning, consumable wear와 wafer loading에 따라 비정상·다중모드 분포를 보인다. 공정 drift와 진짜 fault를 구분하려면 AI 모델뿐 아니라 plasma·장비 물리, 센서 교정과 domain adaptation이 필요하다.

**한 줄 요약:** DutchBoy S는 식각 장비 내부에서 200개 이상 신호를 분석하는 엣지 FDC 플랫폼이지만, fab 수준의 오탐·수율·지연 데이터가 공개돼야 가치가 검증된다.

### 관련 검증 논문

1. **J. Moyne, J. Iskandar**, “Big Data Analytics for Smart Manufacturing: Case Studies in Semiconductor Manufacturing,” *Processes*, 5(3), 39, 2017. [DOI 10.3390/pr5030039](https://doi.org/10.3390/pr5030039).  
   **관련성:** 반도체 fab의 FDC, virtual metrology, predictive maintenance 데이터 구조와 적용 단계를 정리한다.
2. **G. A. Susto, A. Schirru, S. Pampuri, S. McLoone, A. Beghi**, “Machine Learning for Predictive Maintenance: A Multiple Classifier Approach,” *IEEE Transactions on Industrial Informatics*, 11(3), 812–820, 2015. [DOI 10.1109/TII.2014.2349359](https://doi.org/10.1109/TII.2014.2349359).  
   **관련성:** 반도체 장비 benchmark에서 고차원·censored data와 유지보수 의사결정을 연결한다.
3. **S. H. Kim, C. Y. Kim, D. H. Seol, J. E. Choi, S. J. Hong**, “Machine Learning-Based Process-Level Fault Detection and Part-Level Fault Classification in Semiconductor Etch Equipment,” *IEEE Transactions on Semiconductor Manufacturing*, 35(2), 174–185, 2022. [DOI 10.1109/TSM.2022.3161512](https://doi.org/10.1109/TSM.2022.3161512).  
   **관련성:** 실제 식각 장비의 OC-SVM 이상탐지와 XGBoost 부품 수준 원인분류를 검증해 DutchBoy S의 핵심 기능과 직접 대응한다.

### 병목과 개발 과제

- 고장 데이터 희소·불균형, recipe/장비/챔버별 domain shift.
- false alarm과 missed detection의 경제적 비용을 반영한 threshold 설정.
- 센서 clock 정렬, 결측·교정 drift, feature leakage와 label 품질.
- 설명가능성, 모델 업데이트 승인, 사이버보안, 실시간 deterministic latency.

### 현재 상태·브리프

- **상태:** M2~M3 추정. CES 수상작 설명 외에 양산 fab 배치 규모와 KPI는 공개되지 않았다.
- **반도체 직접성:** 높음 — 식각 공정장비의 FDC·예지보전 계층.
- **연구가치:** 5/5 — 공개 식각 데이터와 물리정보를 결합한 재현 연구 여지가 크다.

---

## 3. 12개 사례 비교

| # | 회사·기술 | 핵심 소자/공정 | CES 유형 | 대표 공개 수치* | 성숙도 | 연구가치 | 가장 큰 미확인점 |
|---:|---|---|---|---|---:|---:|---|
| 1 | Samsung Display RGB OLEDoS | CMOS Si 백플레인 + RGB 유기발광 미세패턴 | 헤드셋 시연 | 1.4형, 5,000 PPI, 15,000 nit | M2–M3 | 5 | RGB 수명·수율·양산 고객 |
| 2 | ST VL53L9 | SPAD + TDC + VCSEL dToF | CES Honoree/전시 | 2.3k zone, 5 cm–9 m(최종), 100 fps | M4–M5 | 5 | 주변광·다중경로 실제 오차 |
| 3 | DEEPX DX-H1/DX-M2 | 비전 NPU, 희소/MoE 로드맵 | 발표·Honoree | DX-H1 50 TOPS/40 W; DX-M2 100B/<5 W 목표 | M1–M4 혼합 | 5 | 모델·정밀도·메모리 포함 독립 검증 |
| 4 | NVIDIA Rubin | GPU·CPU·NVLink Switch·DPU·NIC·Ethernet | 플랫폼 발표 | GPU당 NVLink 3.6 TB/s, NVL72 260 TB/s | M3–M4 | 5 | 토큰당 비용의 동등 조건 검증 |
| 5 | Intel Core Ultra 3/18A | GAA RibbonFET + PowerVia BSPD | 제품 데뷔 | 16 CPU cores, 12 Xe cores, NPU 50 TOPS | M4–M5 | 5 | 초기 18A 수율·비용·장기 신뢰성 |
| 6 | Bosch SiC | 750/1,200 V 트렌치 SiC MOSFET·모듈 | 부스 전시 | 전압 등급만 공개 | M3–M4 | 5 | RDS(on), 단락, 산화막 수명 |
| 7 | Bosch BMI5 | MEMS 자이로/가속도계 + 센서 ASIC | 제품 출시 | <0.5 ms, 약 0.6 μs time increment | M3 | 4 | 온도·진동 전 범위 수치와 HVM 달성 |
| 8 | AMD Ryzen AI 400 | Zen 5 + GPU + XDNA 2 NPU | 제품 발표 | NPU 최대 60 TOPS, 15–54 W | M4–M5 | 4 | 모델별 지속 성능·fallback 비용 |
| 9 | Qualcomm X2 Plus | Oryon + Adreno + Hexagon NPU | 제품 발표 | NPU 80 TOPS | M4 | 4 | 공정·die 정보, tokens/s/W |
| 10 | CIT CuFlat-PKGCore | 유리 코어 + 건식 초평탄 Cu | CES Honoree/전시 | “HVLP4 대비 200배 평탄” 주장 | M2–M3 | 5 | 계측 정의·접착·TGV 수율·qualification |
| 11 | IDeas AetherCore | flake 금속분말 소결 다공 필터 | CES Honoree/전시 | 99.9999999%, flow +40% 주장 | M2–M3 | 5 | 입자 크기별 log reduction과 shedding |
| 12 | AIBIZ DutchBoy S | 식각 장비 로컬 AI/FDC appliance | CES Honoree/전시 | 200개 이상 센서 | M2–M3 | 5 | 오탐·지연·수율·fab 배치 규모 |

\* 회사 또는 CES 출품사가 공개한 값이며, 동일 시험조건의 독립 비교값이 아님.

### 비교 해석

- **가장 직접적인 소자 혁신:** Intel 18A, Bosch SiC, Bosch BMI5, Samsung OLEDoS, ST dToF.
- **시스템 반도체 공동설계:** DEEPX, NVIDIA, AMD, Qualcomm은 연산기 자체보다 메모리·NoC·소프트웨어가 실제 효율을 좌우한다.
- **공정·패키징 인프라:** CIT, IDeas, AIBIZ는 칩 밖의 재료·오염·장비 데이터가 선단 노드 수율을 제한하는 문제를 겨냥한다.
- **근거 공개가 가장 충분한 축:** Intel, ST, AMD, Qualcomm은 공식 사양·공급 일정이 비교적 구체적이다. 다만 내부 벤치마크의 독립성 문제는 남는다.
- **검증 공백이 가장 큰 축:** CuFlat, AetherCore, DutchBoy S는 제품 아이디어는 반도체 공정과 직접 연결되지만 표준화된 계측·고객 qualification 결과가 없다.

---

## 4. CES 2026에서 읽히는 반도체 기술 트렌드

### 4.1 트랜지스터 미세화에서 전력망 재배치로

GAA만으로는 전면 배선 혼잡과 IR drop을 해결할 수 없다. Intel 18A는 채널 제어(RibbonFET)와 전원 전달(PowerVia)을 한 노드에 묶어, PPA 개선의 단위가 트랜지스터 하나에서 표준셀·배선·패키지로 확장됐음을 보여준다.

### 4.2 “엣지 AI”와 “AI 팩토리”의 양극화

AMD·Qualcomm·DEEPX는 수십 W 이하 또는 5 W 목표의 로컬 추론을, NVIDIA는 수십 GPU가 연결된 랙스케일 추론·학습을 지향한다. 두 영역 모두 MAC 수보다 메모리 이동과 네트워크가 지배한다는 공통점이 있다.

### 4.3 TOPS에서 workload-level KPI로의 전환 압력

50, 60, 80 TOPS를 직접 비교하면 정밀도, sparsity, utilization, 메모리, 정확도와 thermal throttling을 놓친다. CES 마케팅 수치와 학술 재현성의 간극을 줄이려면 MLPerf 계열의 모델·정확도·전력 측정과 공개 compiler version이 필요하다.

### 4.4 물리 AI의 센서 반도체화

BMI5와 VL53L9는 센서가 단순 ADC 출력을 넘어서 timestamp, 이벤트 분류, depth reconstruction을 칩 내부에서 수행하는 방향을 보여준다. 센서 소자, mixed-signal ASIC와 엣지 알고리즘이 하나의 설계 단위가 된다.

### 4.5 와이드밴드갭 전력소자의 주류 진입

750 V와 1,200 V SiC MOSFET은 전기차와 전력변환의 주력 전압대를 직접 겨냥한다. 남은 차별화는 단순 항복전압이 아니라 계면·게이트 산화막 수명, 단락 내량, 모듈 열·기생성분과 비용이다.

### 4.6 유리 코어가 만드는 패키징의 재료 전환

AI 칩의 reticle 초과 패키지가 커질수록 유기 기판의 warpage와 미세배선 한계가 두드러진다. 유리는 치수 안정성과 낮은 손실이 강점이지만 취성, TGV, Cu 접착과 패널 핸들링이 양산 장벽이다.

### 4.7 오염제어와 장비 AI가 수율 기술로 부상

AetherCore와 DutchBoy S는 선단공정의 경쟁력이 노광 장비만으로 결정되지 않음을 보여준다. 가스의 나노입자, 센서 drift, 챔버 상태와 예지보전이 defect density와 equipment availability를 좌우한다.

### 4.8 이종집적이 제품 카테고리를 가로지름

OLEDoS의 CMOS/유기층, dToF의 SPAD/처리회로, AI 가속기의 GPU/HBM/스위치, 18A의 칩렛·후면전력은 서로 다른 재료·노드·기능을 연결한다. 단일 die의 공정 최적화만으로는 전체 성능을 설명하기 어렵다.

---

## 5. 우선순위 Top 5

### 5.1 반도체 소자 Top 5

| 순위 | 소자 | 선정 이유 | 핵심 검증 KPI |
|---:|---|---|---|
| 1 | Intel 18A RibbonFET + PowerVia | GAA와 BSPD의 첫 대규모 클라이언트 제품 통합이라는 직접성·파급력 | Vmin, IR drop, routed area, yield, BTI/TDDB |
| 2 | Bosch 750/1,200 V SiC trench MOSFET | 전기차 전력변환의 효율·열·충전 속도에 직접 영향 | RDS(on)·Qg, short-circuit time, ΔVth, Rth |
| 3 | ST VL53L9 SPAD dToF | SPAD·TDC·VCSEL·온칩 처리의 고밀도 통합과 즉시 상용성 | range RMSE, DCR, ambient robustness, fps/W |
| 4 | Samsung 5,000 PPI RGB OLEDoS | CMOS 백플레인과 RGB 직접발광의 극미세 이종집적 | PPI yield, luminance lifetime, mura, W/nit |
| 5 | Bosch BMI5 MEMS IMU | 로봇·XR의 시간동기와 진동 환경을 겨냥한 물리 센서 플랫폼 | bias instability, VRE, latency, clock drift |

### 5.2 반도체 공정·패키징 Top 5

| 순위 | 공정/인프라 | 선정 이유 | 핵심 검증 KPI |
|---:|---|---|---|
| 1 | Intel 18A GAA+BSPD 통합 | FEOL·MOL·BEOL·후면 공정을 동시에 바꾸는 양산 사례 | wafer yield, via resistance, overlay, thermal resistance |
| 2 | CIT CuFlat 유리 코어 금속화 | 대형 AI 패키지의 warpage·고속손실·미세선폭 병목을 동시에 겨냥 | Ra/Rq, peel strength, insertion loss, TGV yield |
| 3 | IDeas AetherCore 가스 필터 | 공정가스 오염과 장비 가동률을 재료 미세구조로 개선 | log reduction vs size, ΔP, shedding, lifetime |
| 4 | AIBIZ DutchBoy S 식각 FDC | 공정장비 데이터의 로컬 실시간 진단으로 수율·가동률 개선 잠재력 | FAR, MDR, detection latency, yield/OEE uplift |
| 5 | Samsung RGB OLEDoS 패터닝 | 5 μm급 픽셀 피치에서 이종 유기재료를 Si에 정렬·증착 | mask alignment, pixel defect density, color crosstalk |

> Intel 18A와 Samsung OLEDoS는 소자와 공정이 불가분이므로 두 목록에 중복 포함했다.

---

## 6. 공통 병목 종합

| 계층 | 공통 병목 | 관련 사례 | 필요한 시험 |
|---|---|---|---|
| 소자 전기 | Vth 변동, 누설, 산화막·계면 트랩 | Intel 18A, Bosch SiC | wafer-level 분포, BTI/TDDB, 온도·바이어스 가속수명 |
| 소자 광학 | photon budget, DCR, 유기재료 열화 | ST dToF, Samsung OLEDoS | 온도별 DCR, 주변광 RMSE, 휘도 수명·mura |
| MEMS | bias·scale factor·진동 정류 오차 | Bosch BMI5 | Allan variance, shaker, thermal cycling, multi-axis cross-coupling |
| 메모리/데이터 이동 | SRAM 한계, DRAM/HBM 대역폭, NoC 활용률 | DEEPX, NVIDIA, AMD, Qualcomm | 모델별 메모리 traffic, energy/op가 아닌 energy/inference |
| 패키지/배선 | warpage, TGV/TSV, Cu 접착, 고속손실 | CIT, NVIDIA, Intel | 열기계 cycle, 112/224 Gbps SI, via chain yield |
| 열 | hotspot, 냉각, 지속 성능 | 전 사례 | junction-to-ambient Rth, throttling curve, rack PUE |
| 공정 오염 | 입자 포집과 압력강하, shedding | IDeas | 입자 크기별 log reduction, UHP gas blank, 장기 loading |
| 장비 데이터 | drift, class imbalance, domain shift | AIBIZ | time-split 검증, chamber transfer, FAR/MDR와 비용함수 |
| 검증 표준 | 회사별 서로 다른 조건·피크 수치 | 전 사례 | 공통 workload, accuracy constraint, 공개 metrology protocol |

가장 중요한 횡단 병목은 **측정의 정의**다. “TOPS”, “평탄도 200배”, “99.9999999%”, “10배 낮은 비용”은 측정 대상·조건·오차막대가 없으면 과학적 비교값이 아니다. CES 기술을 연구 과제로 전환하는 첫 단계는 더 높은 수치를 만드는 것이 아니라, 수치의 시험 프로토콜을 공개하는 것이다.

---

## 7. 향후 기술 방향

1. **GAA+BSPD의 세대 확장:** 표준셀 수준 이득을 SRAM·아날로그·I/O까지 확장하고, 후면 전력과 후면 신호/광 I/O의 결합을 탐색해야 한다.
2. **유리·실리콘·유기 기판의 하이브리드화:** 모든 층을 유리로 바꾸기보다 glass core, fine RDL, silicon bridge, optical I/O를 기능별로 조합하는 방향이 유력하다.
3. **모델-컴파일러-메모리-공정 공동설계:** 엣지 NPU는 peak TOPS 대신 모델별 tensor shape, sparsity, SRAM 크기와 공정 전압을 함께 최적화해야 한다.
4. **광자·관성 센서의 이벤트화:** raw frame을 보내지 않고 깊이·움직임 이벤트를 센서에서 생성하며, uncertainty와 timestamp를 함께 출력하는 센서가 중요해진다.
5. **SiC 신뢰성 중심 경쟁:** 낮은 RDS(on) 경쟁에서 threshold stability, short-circuit, 모듈 열사이클과 실제 mission profile 수명 경쟁으로 이동한다.
6. **Physics-informed fab AI:** black-box anomaly score에 plasma 상태방정식, 장비 topology, maintenance log와 causal graph를 결합해 챔버 간 전이성을 높여야 한다.
7. **오염 관리의 sub-10 nm 계측:** 필터 성능을 단일 효율 숫자가 아니라 particle-size-resolved penetration, outgassing, metal contribution과 수명으로 평가해야 한다.
8. **시스템 탄소·물 사용량까지 포함한 효율:** AI 칩의 TOPS/W뿐 아니라 제조 수율, 냉각, HBM·패키지와 운영 전력의 life-cycle 효율을 비교해야 한다.

---

## 8. 바로 실행 가능한 연구 주제

| # | 연구 질문 | 독립변수 | 종속변수/평가지표 | 권장 방법 |
|---:|---|---|---|---|
| 1 | GAA ribbon 형상 변동이 저전압 SRAM/logic에 미치는 영향은? | ribbon width/thickness, Vt, contact R | Vmin, delay σ, leakage, SNM | TCAD + Monte Carlo compact model |
| 2 | BSPD가 CPU 블록의 전원·열에 주는 순효과는? | backside via pitch/R, grid layer, power map | IR drop, droop, hotspot, routed area | PDN extraction + electrothermal simulation |
| 3 | SiC trench의 전계 완화와 온저항 최적점은? | trench radius, p-shield dose, oxide thickness | RDS(on), Eox peak, Qg, breakdown | TCAD + accelerated gate stress |
| 4 | 5,000 PPI RGB OLEDoS의 수율 제한 결함은? | mask offset, aperture, organic thickness | dead pixel, crosstalk, luminance uniformity, lifetime | DOE + electroluminescence microscopy |
| 5 | SPAD dToF의 9 m 범위를 결정하는 photon budget은? | laser power, PDE, DCR, bin width, ambient lux | range RMSE, miss rate, fps/W | Monte Carlo photon simulation + outdoor test |
| 6 | 로봇 진동에서 BMI형 IMU 오차를 줄이는 최적 보정은? | vibration PSD, temperature, mounting, filter | VRE, bias drift, attitude error, latency | shaker + thermal chamber + Allan analysis |
| 7 | 50/60/80 TOPS NPU를 공정하게 비교할 수 있는가? | model, precision, batch, compiler, memory | accuracy, P50/P99 latency, J/inference, utilization | 동일 ONNX 모델·외부 전력계·공개 로그 |
| 8 | 유리 위 초평탄 Cu의 접착-손실 Pareto frontier는? | seed/adhesion layer, Cu grain, Ra/Rq | peel strength, S21, line resistance, warpage | AFM/XPS + peel + high-speed coupon |
| 9 | flake 분말이 필터의 효율-압력강하를 개선하는가? | aspect ratio, size distribution, sinter T/P | size-resolved penetration, ΔP, shedding, strength | aerosol challenge + SEM tomography |
| 10 | 식각 FDC가 chamber/recipe를 넘어 전이되는가? | chamber, recipe, maintenance state, sensor subset | FAR, MDR, lead time, root-cause top-k | leave-one-chamber-out + physics-informed features |
| 11 | NVLink형 랙에서 topology가 MoE tail latency에 미치는 영향은? | expert placement, routing, link load | token/s, P99, energy/token, link utilization | trace-driven simulator + rack telemetry |
| 12 | 센서 내부 AI가 시스템 에너지를 실제로 줄이는가? | event threshold, model size, duty cycle | total J/task, miss rate, host wakeups, privacy leakage | sensor/host 동시 전력 계측 |

연구 결과는 평균값만 보고하지 말고, 표본 수·오차막대·온도·전압·소프트웨어 버전·정확도 제약·데이터셋을 함께 공개해야 한다.

---

## 9. CES 발표와 학술 검증 사이의 간극

| CES 메시지 | 학술문헌이 뒷받침하는 범위 | 아직 필요한 증거 |
|---|---|---|
| Intel 18A가 성능/전력을 개선 | GAA와 BSPD의 물리·PDN 이득은 다수 논문이 지지 | Panther Lake wafer yield, 장기 신뢰성, 동일 설계 비교 |
| SiC trench가 고효율 | SiC의 낮은 drift 저항과 고온 특성은 확립 | Bosch 소자의 RDS(on)·Qg·단락·TDDB 데이터 |
| BMI5가 저지연·진동 강건 | MEMS 구조와 진동 오차 모델은 확립 | Bosch 정의의 전 대역·온도 시험 조건과 raw data |
| 5,000 PPI RGB OLEDoS가 XR을 개선 | Si 백플레인·고PPI 가능성과 병목은 검증됨 | RGB 직접패턴 수율·청색 수명·헤드셋 열/광효율 |
| VL53L9가 2.3k-zone depth 제공 | SPAD dToF 원리와 배열화는 검증됨 | outdoor, multipath, interference benchmark |
| NPU가 수십 TOPS 또는 100B/<5 W | dataflow·희소성·저정밀 이득은 검증됨 | 동일 모델 정확도·메모리 포함 end-to-end J/token |
| Rubin이 토큰 비용을 10배 낮춤 | 메모리 분할·NVLink·HBM의 시스템 이점은 검증됨 | 독립 TCO, workload·전력·utilization 공개 |
| CuFlat이 200배 평탄 | 유리 인터포저와 Cu/TGV 가능성은 검증됨 | roughness 정의, adhesion, panel yield, reliability |
| AetherCore가 9-nine 효율 | 다공 금속의 포집 원리는 검증됨 | 입자 크기별 log reduction, ΔP, UHP contamination |
| DutchBoy가 실시간 원인 진단 | 반도체 식각 FDC 방법은 학술적으로 검증됨 | 다중 fab의 FAR/MDR, causal validity, yield uplift |

학술문헌은 **원리의 가능성**을 뒷받침하지만 특정 CES 제품의 성능을 자동으로 검증하지 않는다. 반대로 CES 데모는 제품 통합의 실재를 보여주지만 실험 설계·원시 데이터·오차막대를 제공하지 않는 경우가 많다. 두 영역을 연결하려면 업체가 benchmark protocol과 제한된 익명 데이터셋을 공개하고, 학계는 실제 공정 제약과 비용함수를 평가에 포함해야 한다.

---

## 10. 팩트체크 기록

| 항목 | 판정 | 근거와 주의점 |
|---|---|---|
| CES 2026 일정은 1월 6~9일 | 확인 | [CES 공식 보도자료](https://www.ces.tech/press-releases/ces-2026-the-future-is-here) |
| Samsung 5,000 PPI 패널이 CES 2026에서 최초 공개 | **부정확** | 패널은 [SID 2025](https://news.samsungdisplay.com/34337)에서 선행 공개; CES의 새로움은 헤드셋 시연 |
| VL53L9가 CES 2026에서 최초 발표 | **부정확** | ST는 [2024-02-22](https://newsroom.st.com/media-center/press-item.html/p4608.html) 최초 발표; CES는 수상·전시 |
| VL53L9 범위가 10 m | 조건부 | CES/2024 설명은 10 m, 2026 최종 양산 발표는 9 m. 최종 제품 표기는 9 m 사용 |
| Intel 18A는 물리 1.8 nm 게이트 | **부정확** | 18A는 노드명; 실제 치수의 단일 표현이 아님 |
| Intel·AMD·Qualcomm의 성능향상 수치 | 회사 주장 | 각사 내부 비교 조건이며 독립 동일플랫폼 실험 아님 |
| Bosch SiC가 경쟁사보다 우수 | 판단 보류 | 전압과 구조만 공개; 핵심 전기·신뢰성 수치 없음 |
| BMI5가 기준일 현재 대량생산 | 미확인 | 발표는 2026년 3분기 계획; 기준일에 실제 달성 공지 확인 안 됨 |
| DEEPX DX-M2가 이미 100B/<5 W 달성 | **확인 불가/로드맵** | 회사가 제시한 목표이며 모델·메모리·속도 조건 미공개 |
| Rubin CES 플랫폼은 7칩 | **CES 기준 부정확** | 2026-01-05 CES 발표는 6칩; 이후 확장 표현과 분리 필요 |
| 50·60·80 TOPS가 곧 실제 순위 | **부정확** | 정밀도·sparsity·활용률·메모리·정확도 제약이 다름 |
| CuFlat “200배 평탄” | 출품사 주장 | 측정 단위·면적·필터·표본 수 미공개 |
| AetherCore 99.9999999%, flow +40% | 출품사 주장 | 입자 크기·가스·유량·시험기관 미공개 |
| DutchBoy S가 수율을 개선 | 가능성, 수치 미확인 | 200+ 센서와 기능은 설명되나 yield uplift·FAR/MDR 없음 |
| CES Innovation Award가 성능 독립시험을 뜻함 | **부정확** | CTA가 출품 설명의 정확성을 검증하거나 제품을 시험하지 않는다는 공식 고지 확인 |

---

## 11. References

### 11.1 CES·회사 공식 자료

1. Consumer Technology Association, “CES 2026: The Future Is Here,” CES official press release, 2026. [원문](https://www.ces.tech/press-releases/ces-2026-the-future-is-here)
2. AGC, “AGC at CES 2026,” 2026. CTA Innovation Awards 설명·시험 면책 고지 포함. [원문](https://www.agc.com/en/ces/)
3. Samsung Display, “A New Era of Experience, Powered by AI & Display,” CES 2026, 2026. [원문](https://news.samsungdisplay.com/34419)
4. Samsung Display, RGB OLEDoS at SID Display Week 2025, 2025. [원문](https://news.samsungdisplay.com/34337)
5. CES Innovation Awards, “ST VL53L9 Time-of-Flight Sensor,” 2026 Honoree. [원문](https://www.ces.tech/ces-innovation-awards/2026/st-vl53l9-time-of-flight-sensor/)
6. STMicroelectronics, “VL53L9CX,” product page, accessed 2026-08-21. [원문](https://www.st.com/en/imaging-and-photonics-solutions/vl53l9cx.html)
7. STMicroelectronics, first VL53L9 announcement, 2024-02-22. [원문](https://newsroom.st.com/media-center/press-item.html/p4608.html)
8. STMicroelectronics, VL53L9 mass-production announcement, 2026-06-22. [원문](https://newsroom.st.com/media-center/press-item.html/p4783.html)
9. DEEPX, “CES 2026 Media Briefing: DEEPX Unveils Physical AI Vision Roadmap,” 2026-01-06. [원문](https://deepx.ai/ces-2026-media-briefing-deepx-unveils-physical-ai-vision-roadmap/)
10. CES Innovation Awards, “DX-H1 V-NPU,” 2026 Honoree. [원문](https://www.ces.tech/ces-innovation-awards/2026/dx-h1-v-npu/)
11. DEEPX, “DX-H1 V-NPU,” product page, accessed 2026-08-21. [원문](https://deepx.ai/products/dx-h1-v-npu/)
12. NVIDIA, “NVIDIA Kicks Off the Next Generation of AI With Rubin,” 2026-01-05. [원문](https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer)
13. Intel, “CES 2026: Intel Core Ultra Series 3 Debut — First Built on Intel 18A,” 2026-01-05. [원문](https://newsroom.intel.com/client-computing/ces-2026-intel-core-ultra-series-3-debut-first-built-on-intel-18a)
14. Intel Foundry, “Intel 18A,” accessed 2026-08-21. [원문](https://www.intel.com/content/www/us/en/foundry/process/18a.html)
15. Bosch Semiconductors, “CES 2026,” 2026-01-06~09. [원문](https://www.bosch-semiconductors.com/events/ces-2026.html)
16. Bosch Sensortec, “Bosch Sensortec Launches BMI5 Motion Sensor Platform,” 2026-01-05. [원문](https://www.bosch-sensortec.com/en/news/from-immersive-xr-to-advanced-robotics-and-wearables-bosch-sensortec-launches-bmi5-motion-sensor-platform.html)
17. AMD, “AMD Expands AI Leadership … at CES 2026,” 2026-01-05. [원문](https://ir.amd.com/news-events/press-releases/detail/1270/amd-expands-ai-leadership-across-client-graphics-and-software-with-new-ryzen-ryzen-ai-and-amd-rocm-announcements-at-ces-2026)
18. Qualcomm, “Empowering Professionals and Aspiring Creators: Snapdragon X2 Plus,” 2026-01-05. [원문](https://www.qualcomm.com/news/releases/2026/01/empowering-professionals-and-aspiring-creators--snapdragon-x2-pl)
19. CES Innovation Awards, “CuFlat-PKGCore: Ultra-Flat Copper-Deposited Glass for Semiconductor Packaging,” 2026 Honoree. [원문](https://www.ces.tech/ces-innovation-awards/2026/cuflat-pkgcore-ultra-flat-copper-deposited-glass-for-semiconductor-packaging/)
20. CES Innovation Awards, “AetherCore: Ultra-Clean Gas Filtration for Next-Gen Semiconductor Manufacturing,” 2026 Honoree. [원문](https://www.ces.tech/ces-innovation-awards/2026/aethercore-ultra-clean-gas-filtration-for-next-gen-semiconductor-manufacturing/)
21. CES Innovation Awards, “DutchBoy S: Semiconductor Etch Equipment On-Device AI Platform,” 2026 Honoree. [원문](https://www.ces.tech/ces-innovation-awards/2026/dutchboy-s-semi-conductor-etch-equipment-on-device-ai-platform/)

### 11.2 학술 논문

22. N. Loubet et al., “Stacked Nanosheet Gate-All-Around Transistor to Enable Scaling Beyond FinFET,” *VLSI Technology*, 2017. [DOI 10.23919/VLSIT.2017.7998183](https://doi.org/10.23919/VLSIT.2017.7998183)
23. J. Ryckaert et al., “Extending the Roadmap Beyond 3 nm through System Scaling Boosters,” *EDTM*, 2019. [DOI 10.1109/EDTM.2019.8731234](https://doi.org/10.1109/EDTM.2019.8731234)
24. D. Prasad et al., “Buried Power Rails and Back-side Power Grids,” *IEDM*, 2019. [DOI 10.1109/IEDM19573.2019.8993617](https://doi.org/10.1109/IEDM19573.2019.8993617)
25. T. Kimoto, “Material Science and Device Physics in SiC Technology for High-Voltage Power Devices,” *JJAP*, 54, 040103, 2015. [DOI 10.7567/JJAP.54.040103](https://doi.org/10.7567/JJAP.54.040103)
26. K. Puschkarsky et al., “Review on SiC MOSFETs High-Voltage Device Reliability Focusing on Threshold Voltage Instability,” *IEEE TED*, 66(11), 2019. [DOI 10.1109/TED.2019.2938262](https://doi.org/10.1109/TED.2019.2938262)
27. A. J. Lelis, R. Green, D. B. Habersat, “SiC MOSFET Threshold-Stability Issues,” *Materials Science in Semiconductor Processing*, 78, 2018. [DOI 10.1016/j.mssp.2017.11.028](https://doi.org/10.1016/j.mssp.2017.11.028)
28. N. Yazdi, F. Ayazi, K. Najafi, “Micromachined Inertial Sensors,” *Proceedings of the IEEE*, 86(8), 1998. [DOI 10.1109/5.704269](https://doi.org/10.1109/5.704269)
29. C. Acar, A. M. Shkel, “Inherently Robust Micromachined Gyroscopes With 2-DOF Sense-Mode Oscillator,” *JMEMS*, 15(2), 2006. [DOI 10.1109/JMEMS.2006.872224](https://doi.org/10.1109/JMEMS.2006.872224)
30. W. A. Gill et al., “A Review of MEMS Vibrating Gyroscopes and Their Reliability Issues in Harsh Environments,” *Sensors*, 22, 7405, 2022. [DOI 10.3390/s22197405](https://doi.org/10.3390/s22197405)
31. R. Kaçar et al., “OLED-on-Silicon (OLEDoS) Microdisplays: Technology Challenges…,” *Next Nanotechnology*, 7, 100132, 2025. [DOI 10.1016/j.nxnano.2025.100132](https://doi.org/10.1016/j.nxnano.2025.100132)
32. C.-m. Kang, H. Lee, “Recent Progress of Organic Light-Emitting Diode Microdisplays for AR/VR Applications,” *Journal of Information Display*, 23(1), 2022. [DOI 10.1080/15980316.2021.1917461](https://doi.org/10.1080/15980316.2021.1917461)
33. Y. Tamatsukuri et al., “5009-ppi, 10000-cd/m², OLED/OS/Si Structure Display…,” *Journal of SID*, 33(5), 2025. [DOI 10.1002/jsid.2058](https://doi.org/10.1002/jsid.2058)
34. E. Charbon, “Single-Photon Imaging in CMOS Processes,” *Philosophical Transactions A*, 372, 20130100, 2014. [DOI 10.1098/rsta.2013.0100](https://doi.org/10.1098/rsta.2013.0100)
35. C. Niclass et al., “A 100-m Range 10-Frame/s 340×96-Pixel ToF Depth Sensor in 0.18-μm CMOS,” *IEEE JSSC*, 48(2), 2013. [DOI 10.1109/JSSC.2012.2227607](https://doi.org/10.1109/JSSC.2012.2227607)
36. J. Kostamovaara, S. S. Jahromi, P. Keränen, “Temporal and Spatial Focusing in SPAD-Based Solid-State Pulsed ToF,” *Sensors*, 20, 5973, 2020. [DOI 10.3390/s20215973](https://doi.org/10.3390/s20215973)
37. V. Sze et al., “Efficient Processing of Deep Neural Networks: A Tutorial and Survey,” *Proceedings of the IEEE*, 105(12), 2017. [DOI 10.1109/JPROC.2017.2761740](https://doi.org/10.1109/JPROC.2017.2761740)
38. Y.-H. Chen et al., “Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep CNNs,” *IEEE JSSC*, 52(1), 2017. [DOI 10.1109/JSSC.2016.2616357](https://doi.org/10.1109/JSSC.2016.2616357)
39. N. P. Jouppi et al., “In-Datacenter Performance Analysis of a Tensor Processing Unit,” *ISCA*, 2017. [DOI 10.1145/3079856.3080246](https://doi.org/10.1145/3079856.3080246)
40. S. Rajbhandari et al., “ZeRO: Memory Optimizations Toward Training Trillion Parameter Models,” *SC20*, 2020. [DOI 10.5555/3433701.3433727](https://doi.org/10.5555/3433701.3433727)
41. A. Li et al., “Evaluating Modern GPU Interconnect: PCIe, NVLink, NV-SLI, NVSwitch and GPUDirect,” *IEEE TPDS*, 31(1), 2020. [DOI 10.1109/TPDS.2019.2928289](https://doi.org/10.1109/TPDS.2019.2928289)
42. D. U. Lee et al., “A 128Gb 8-High 512GB/s HBM2E DRAM…,” *ISSCC*, 2020. [DOI 10.1109/ISSCC19947.2020.9062977](https://doi.org/10.1109/ISSCC19947.2020.9062977)
43. Y.-H. Chen et al., “Eyeriss v2: A Flexible Accelerator for Emerging DNNs on Mobile Devices,” *IEEE JETCAS*, 9(2), 2019. [DOI 10.1109/JETCAS.2019.2910232](https://doi.org/10.1109/JETCAS.2019.2910232)
44. V. Sze et al., “How to Evaluate Deep Neural Network Processors: TOPS/W (Alone) Considered Harmful,” *IEEE Solid-State Circuits Magazine*, 12(3), 2020. [DOI 10.1109/MSSC.2020.3002140](https://doi.org/10.1109/MSSC.2020.3002140)
45. T. Chen et al., “DianNao: A Small-Footprint High-Throughput Accelerator for Ubiquitous Machine-Learning,” *ASPLOS*, 2014. [DOI 10.1145/2541940.2541967](https://doi.org/10.1145/2541940.2541967)
46. X. Zhang et al., “ShuffleNet: An Extremely Efficient CNN for Mobile Devices,” *CVPR*, 2018. [DOI 10.1109/CVPR.2018.00716](https://doi.org/10.1109/CVPR.2018.00716)
47. V. Sukumaran et al., “Design, Fabrication and Characterization of Low-Cost Glass Interposers…,” *ECTC*, 2011. [DOI 10.1109/ECTC.2011.5898571](https://doi.org/10.1109/ECTC.2011.5898571)
48. V. Sukumaran et al., “Low-Cost Thin Glass Interposers as a Superior Alternative…,” *IEEE TCPMT*, 2(9), 2012. [DOI 10.1109/TCPMT.2012.2204392](https://doi.org/10.1109/TCPMT.2012.2204392)
49. V. Sukumaran et al., “Design, Fabrication, and Characterization of Ultrathin 3-D Glass Interposers…,” *IEEE TCPMT*, 4, 2014. [DOI 10.1109/TCPMT.2014.2303427](https://doi.org/10.1109/TCPMT.2014.2303427)
50. M. S. A. Heikkinen, N. H. Harley, “Experimental Investigation of Sintered Porous Metal Filters,” *Journal of Aerosol Science*, 31(6), 2000. [DOI 10.1016/S0021-8502(99)00550-9](https://doi.org/10.1016/S0021-8502(99)00550-9)
51. A. Colorado, K. Vakhshoori, “Is Your Gas Filter as Clean as You Think?,” *IEEE/SEMI ASMC*, 2001. [DOI 10.1109/ASMC.2001.925628](https://doi.org/10.1109/ASMC.2001.925628)
52. M.-J. Kim et al., “Fabricating Metal Powder Filters with Material Extrusion Additive Manufacturing,” *Archives of Metallurgy and Materials*, 70(3), 2025. [DOI 10.24425/amm.2025.154461](https://doi.org/10.24425/amm.2025.154461)
53. J. Moyne, J. Iskandar, “Big Data Analytics for Smart Manufacturing: Case Studies in Semiconductor Manufacturing,” *Processes*, 5(3), 39, 2017. [DOI 10.3390/pr5030039](https://doi.org/10.3390/pr5030039)
54. G. A. Susto et al., “Machine Learning for Predictive Maintenance: A Multiple Classifier Approach,” *IEEE TII*, 11(3), 2015. [DOI 10.1109/TII.2014.2349359](https://doi.org/10.1109/TII.2014.2349359)
55. S. H. Kim et al., “Machine Learning-Based Process-Level Fault Detection and Part-Level Fault Classification in Semiconductor Etch Equipment,” *IEEE TSM*, 35(2), 2022. [DOI 10.1109/TSM.2022.3161512](https://doi.org/10.1109/TSM.2022.3161512)

---

## 12. 결론

CES 2026의 반도체 핵심은 “더 작은 노드” 하나가 아니라 **소자 구조, 전력 전달, 패키징, 센서, 메모리 이동, 공정 청정도와 장비 데이터의 결합**이다. Intel 18A와 SiC는 물리 소자 혁신을, OLEDoS·dToF·MEMS는 현실 세계를 디지털로 연결하는 센서/디스플레이의 고집적화를, 네 종류의 AI 플랫폼은 엣지에서 랙까지의 이종 컴퓨팅을, CuFlat·AetherCore·DutchBoy S는 제조 인프라의 중요성을 보여준다.

연구 우선순위는 최고 수치 재현보다 다음 세 질문에 두어야 한다. **첫째, 공개 수치의 측정 조건이 무엇인가. 둘째, 소자 이득이 패키지·메모리·열·소프트웨어를 포함한 시스템 이득으로 이어지는가. 셋째, 초기 데모가 양산 수율과 장기 신뢰성을 통과하는가.** 이 세 질문에 답하는 표준화된 실험이 CES 발표와 반도체 학술연구 사이의 가장 가치 있는 연결고리다.
