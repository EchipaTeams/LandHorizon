# Graph neural networks and other fast surrogate models for flood inundation: what do they need, is any pretrained model usable, and is this more than a roadmap item?
Date: 2026-11-11
Scope: learned surrogates (emulators) of flood-inundation *models*: GNNs, CNN/U-Net, neural operators, physics-informed and upscaling variants. Out of bounds: running the physical models, published hazard maps, ML mapping from satellite images, discharge forecasting. Fetch notes: several PDFs (arXiv 2604.21028 body, BMVC 2025, arXiv 2307.16090 PDF) were unreadable and PMC returned a browser check, so those were cited only via abs/html pages that opened. Dataset licences were not checked on the repositories themselves unless stated. Quotes marked "(abstract)" or other were copied from the fetched page text; where the fetch tool summarised, only phrases it returned in quotation marks are used.

## Claims

### 1. The field: families, what they predict, domain size
1. **Claim:** SWE-GNN (GNN on the finite-volume mesh) predicts flood depth and unit discharge through time for dike-breach floods, but was trained on small synthetic 64x64 / 128x128 grids with 100 m cells.
   - Source: https://hess.copernicus.org/articles/27/4227/2023/
   - Quote: "We considered 130 numerical simulations of dike breach floods run on randomly generated topographies."
   - Source date: 2023
   - Source type: peer-reviewed (HESS)
   - Confidence: high (grid and cell size are from the fetch summary of the paper's dataset description, not a verbatim quote)

2. **Claim:** A 2026 MeshGraphNet surrogate (Mercier et al.) works on a real river (lower Tet, France) on a Telemac2D mesh of over 400,000 nodes, trained on 56 synthetic hydrograph-driven simulations (40 train, 16 held-out events), and is evaluated on one river only.
   - Source: https://arxiv.org/html/2604.02876 (and abstract https://arxiv.org/abs/2604.02876)
   - Quote: "we generated 14×4=56 hydrographs, each with a duration of 40 hours." and "This paper focuses on developing an operationally motivated surrogate model for rapid flood forecasting on the River Têt."
   - Source date: 2026-04
   - Source type: preprint
   - Confidence: medium (preprint; mesh-size figure comes from the search snippet of the abstract, not verified in the full text)

3. **Claim:** CNN/U-Net emulators on rasters predict depth maps; e.g. a U-Net on 1 m Berlin DEM features predicts urban pluvial water depth from TELEMAC-2D simulations (1 h block-rain events), compared with a random forest.
   - Source: https://nhess.copernicus.org/articles/23/809/2023/
   - Quote: "the RF models outperformed the CNN models for predictions within the training domain"
   - Source date: 2023-02
   - Source type: peer-reviewed (NHESS, Seleem et al.)
   - Confidence: high

4. **Claim:** A context-aware CNN (Cache et al.) predicts max depth on 1 m patches for pluvial floods, trained on only 18 flood maps (1250 patches) of Zurich.
   - Source: https://hess.copernicus.org/articles/28/5443/2024/
   - Quote: "The training, testing, and validation datasets for Zurich were extracted from 18 flood maps at 1 m resolution"
   - Source date: 2024
   - Source type: peer-reviewed (HESS)
   - Confidence: high

5. **Claim:** Fourier neural operator (Sun et al., ICCV workshop 2023) predicts 15-min water-depth fields for Houston, trained on simulations from six storms and tested on two held-out storms, at 10 m DEM with 128x128 patches; simulator CREST-iMAP (ANUGA-Hydro).
   - Source: https://arxiv.org/abs/2307.16090 and https://ar5iv.labs.arxiv.org/html/2307.16090
   - Quote: "training using simulated water depths (in 15-min intervals) from six historical storm events"
   - Source date: 2023-07
   - Source type: preprint / workshop paper (not archival journal)
   - Confidence: medium

6. **Claim:** Physics-informed / hybrid variants exist: a ResNet-18 surrogate for Chicago trained on LISFLOOD-FP + Daymet rainfall 1981-2019; test years are the year after training; reported R2 above 0.96 for one city only.
   - Source: https://arxiv.org/abs/2411.19323
   - Quote: "Results over multiple years in the current climate over Chicago demonstrate an average R-squared greater than 0.96"
   - Source date: 2024-11
   - Source type: preprint
   - Confidence: medium

7. **Claim:** Low-to-high fidelity upscalers refine coarse hydraulic output into fine depth maps: a diffusion model with HEC-RAS coarse depths plus DEM as conditioning, tested on four Australian catchments (EGU 2025 abstract, not a full paper).
   - Source: https://meetingorganizer.copernicus.org/EGU25/EGU25-9285.html
   - Quote: "performing well on other catchments with minimal transfer learning"
   - Source date: 2025
   - Source type: conference abstract (treat as preprint)
   - Confidence: low (abstract only, no numbers)

8. **Claim:** A U-Net predicting the maximum water level on a grid exists for the German Wupper catchment (2026 preprint), trained on hydraulic simulations; only that one catchment is described, number of simulations not given on the abstract page.
   - Source: https://arxiv.org/abs/2604.21028
   - Quote: "predict the maximum water level across a grid"
   - Source date: 2026-04
   - Source type: preprint
   - Confidence: low (abstract only)

### 2. Training data
9. **Claim:** Every surrogate above is trained on simulator output, not on observations: SWE-GNN (numerical dike-breach runs), Mercier (Telemac2D), Seleem (TELEMAC-2D), Sun (CREST-iMAP/ANUGA), Mirhoseini (LISFLOOD-FP). The surrogate therefore inherits the simulator's accuracy. The authors of Seleem state accuracy depends on the training simulations.
   - Source: https://nhess.copernicus.org/articles/23/809/2023/
   - Quote: "The storm drainage system was not included in the TELEMAC-2D simulations."
   - Source date: 2023-02
   - Source type: peer-reviewed
   - Confidence: medium (the quote shows a simulator omission that propagates; the "accuracy depends on simulations" statement is the fetch tool's summary, not quoted)

10. **Claim:** Open datasets of simulated floods exist: SWE-GNN dataset (Zenodo 10.5281/zenodo.7764418, synthetic dike-breach on random DEMs, 130 runs) and the Seleem Berlin TELEMAC-2D outputs (Zenodo 10.5281/zenodo.7516408). Licences of these Zenodo records were not opened: not found. UrbanFloodBench (HEC-RAS coupled 1D-2D, four cities) is reported by search as CC BY-NC 4.0 (non-commercial, so a poor fit for a product); the page itself returned HTTP 403 so this is not verified.
    - Source: https://hess.copernicus.org/articles/27/4227/2023/
    - Quote: "The employed dataset can be found at https://doi.org/10.5281/zenodo.7764418"
    - Source date: 2023
    - Source type: peer-reviewed (data statement)
    - Confidence: medium (existence high; licence not found)

### 3. Compute
11. **Claim:** SWE-GNN: trained on a single V100 (32 GB); inference 100-600x faster than the numerical model on GPU, "up to 2 orders of magnitude" in the abstract. Total training wall-clock time is not reported.
    - Source: https://hess.copernicus.org/articles/27/4227/2023/
    - Quote: "SWE–GNN has a computational speed-up of up to 2 orders of magnitude faster than the numerical solver."
    - Source date: 2023
    - Source type: peer-reviewed
    - Confidence: high

12. **Claim:** Mercier: training on 8 A100 80 GB GPUs across 4 nodes (training time not reported); inference of a 6 h prediction in about 0.4 s versus about 180 min for the reference solver (ratio about 27,000x is a calculation by the fetch tool, not the authors). This is the only reference run that is also the cost the team would need to pay to make the data.
    - Source: https://arxiv.org/html/2604.02876
    - Quote: "All training runs are performed using 8 NVIDIA A100 GPUs (80 GB), distributed over 4 nodes."
    - Source date: 2026-04
    - Source type: preprint
    - Confidence: medium

13. **Claim:** Seleem U-Net training took 20 minutes to 48 hours on one Quadro P4000 GPU; inference about 20 s per depth map.
    - Source: https://nhess.copernicus.org/articles/23/809/2023/
    - Quote: "U-Net training ranged from 20 minutes to 48 hours on an NVIDIA Quadro P4000 GPU." (fetch-tool paraphrase of the paper; not verified verbatim)
    - Source date: 2023-02
    - Source type: peer-reviewed
    - Confidence: low (paraphrased)

14. **Claim:** FNO (Sun): one RTX 3090, 72 s per epoch, up to 60 epochs. Inference 0.002 s per sample. No speed-up versus the simulator is reported.
    - Source: https://ar5iv.labs.arxiv.org/html/2307.16090
    - Quote: "Training time per epoch is 72 sec wallclock time."
    - Source date: 2023-07
    - Source type: preprint
    - Confidence: medium

### 4. Generalisation (the key question)
15. **Claim:** SWE-GNN generalises to unseen synthetic topographies and breach locations, but only inside the same synthetic family (random DEMs, 100 m cells, 48 h, constant breach inflow). No real catchment.
    - Source: https://hess.copernicus.org/articles/27/4227/2023/
    - Quote: "generalizes well to unseen breach locations, bigger domains, and longer periods of time"
    - Source date: 2023
    - Source type: peer-reviewed
    - Confidence: high

16. **Claim:** Real-terrain urban pluvial test: a model trained on one part of Berlin performed poorly outside the training domain; fine-tuning with a small share of target-area data helped (CNN more than RF). Only one city, relatively flat.
    - Source: https://nhess.copernicus.org/articles/23/809/2023/
    - Quote: "the CNN models could better benefit from transfer learning technique"
    - Source date: 2023-02
    - Source type: peer-reviewed
    - Confidence: high

17. **Claim:** Cache et al. report terrain generalisation is not achieved and a single local event is needed to adapt to a new terrain.
    - Source: https://hess.copernicus.org/articles/28/5443/2024/
    - Quote: "While the generalizability to terrain is not yet fully achieved"
    - Source date: 2024
    - Source type: peer-reviewed
    - Confidence: high (second quote: "requiring only a single rainfall event to adapt the model to new terrains")

18. **Claim:** FNO zero-shot claim is weak: tested on only one holdout domain and two storms in one Houston watershed.
    - Source: https://ar5iv.labs.arxiv.org/html/2307.16090
    - Quote: "an FNO model pretrained on similar domains can be applied to the study site without fine-tuning"
    - Source date: 2023-07
    - Source type: preprint
    - Confidence: medium (the "one domain / two storms" limitation is from the fetch tool's reading, not a quote)

19. **Claim:** Upscaler: a satellite-resolution downscaling study reports zero-shot transfer only to regions with similar hydroclimate to its training region (Iowa/US Midwest). This predicts depth/extent from coarse water-fraction maps, a different task, but it is the only explicit zero-shot-region claim found.
    - Source: https://arxiv.org/abs/2502.10601
    - Quote: "our trained models can exhibit superior zero-shot performance when transferred to regions"
    - Source date: 2025-02
    - Source type: preprint
    - Confidence: low (quote is truncated; "hydroclimatologically similar" is from the fetch tool's summary)

20. **Claim:** No paper found shows a surrogate trained on one catchment and validated against observed flood extent in a different catchment without any retraining. Every error figure reported above compares with the simulator. Not found.
    - Source: not found (negative result from the searches in this task, which is not proof of absence)
    - Quote: not found
    - Source date: 2026-11-11
    - Source type: n/a
    - Confidence: low

### 5. Pretrained models
21. **Claim:** The SWE-GNN repo is MIT-licensed with a results folder said to hold trained models, but it is bound to the synthetic dataset and the README warns it needs adapting for a new dataset. Not usable on Galati as is.
    - Source: https://github.com/RBTV1/SWE-GNN-paper-repository-
    - Quote: "This version of the repository is not very robust to changes in inputs"
    - Source date: 2023 (repo; exact date not found)
    - Source type: official docs (code repo)
    - Confidence: medium (licence stated in sidebar only; weights not confirmed by file listing)

22. **Claim:** Cache et al. state their code, trained models and simulation data are public (Zenodo 10.5281/zenodo.10688079, GitHub tcache1/context_aware_flood_model). It is trained on Zurich/Swiss patches at 1 m for pluvial flooding and requires a local event to adapt; it is not a river-flood model. Licence of code/data not found.
    - Source: https://hess.copernicus.org/articles/28/5443/2024/
    - Quote: "The source codes, trained models, and simulation data are freely available in the following repository"
    - Source date: 2024
    - Source type: peer-reviewed
    - Confidence: medium

23. **Claim:** No released pretrained river-flood inundation surrogate that can be pointed at a new area (Galati: Danube, Siret, Prut) was found. Mercier states no code link, Wupper U-Net states none on the abstract page. Not found for global foundation models producing on-land depth at useful resolution (Google's flood forecasting model is covered elsewhere).
    - Source: https://arxiv.org/abs/2604.02876
    - Quote: "The MeshGraphNet implementation provided in this framework was used as the basis" (NVIDIA PhysicsNeMo is the generic framework, not a pretrained flood model)
    - Source date: 2026-04
    - Source type: preprint
    - Confidence: low (absence claim; search was not exhaustive)

### 6. Validation practice and stated limits
24. **Claim:** SWE-GNN authors state it cannot replace the solver: it needs the first time step as input and has no stability or mass-balance guarantee.
    - Source: https://hess.copernicus.org/articles/27/4227/2023/
    - Quote: "our model cannot yet completely replace numerical models as it requires the first time step of the flood evolution as input."
    - Source date: 2023
    - Source type: peer-reviewed
    - Confidence: high

25. **Claim:** Mercier names forcing uncertainty as a deployment limit, and cartographic validation as future work.
    - Source: https://arxiv.org/html/2604.02876
    - Quote: "Future work will focus on extending the cartographic validation"
    - Source date: 2026-04
    - Source type: preprint
    - Confidence: medium

26. **Claim:** Cache et al. state limits: no multi-peak events and no drainage network.
    - Source: https://hess.copernicus.org/articles/28/5443/2024/
    - Quote: "the model was neither trained nor tested for rainfall events with multiple peaks"
    - Source date: 2024
    - Source type: peer-reviewed
    - Confidence: high

## Relevance to LandHorizon
- **Verdict (honest): roadmap item, not buildable before 11 Dec 2026.** Every credible surrogate in these sources needs a calibrated hydrodynamic model of the area to generate training data first (Mercier: 56 simulations on a 400k-node Telemac2D model, 8 A100 GPUs; SWE-GNN: 130 runs but on synthetic terrain). We have no hydrodynamic model, and the constraints give about 280-350 person-hours for the whole project with no ML in the plan. The surrogate would also be validated against a simulator, which conflicts with the rule to validate against an independent sensor (claim 20).
- **Pretrained use:** none found that could be run over Galati without training and with a clear licence (claims 21-23). The SWE-GNN weights are for synthetic 100 m terrain; Cache et al. is a Zurich pluvial model that needs local adaptation. Running either over Galati would produce numbers with no evidence of validity.
- **Generalisation evidence is thin:** transfer to unseen terrain is either within a synthetic family (claim 15), needs fine-tuning (16, 17), or rests on one holdout domain (18). That is not enough to put a surrogate's output on a plot report.
- **Data and licence:** open simulation datasets (claim 10) are for other places; UrbanFloodBench is reported as non-commercial (unverified). None is usable for Galati.
- **Cost / compute (my estimate, not a source's):** a minimal credible project would need a calibrated 2D model (weeks of expert work), tens of simulations, and GPU hours that fit student credits for a small U-Net (cf. Seleem: one P4000, minutes to 48 h) but not for a mesh GNN at Mercier scale. I did not find a source stating a minimal-project cost.
- **Pitch use:** a one-paragraph roadmap line is honest: "after a calibrated hydraulic model is available for the Siret/Danube confluence, a surrogate could give rapid scenario maps; it would be validated against GFM observed extents". It must be listed as not built.
- **No change to the pipeline, contract, or Python dependencies** is recommended from this topic.

## Open questions
- Does any 2025-2026 paper validate a surrogate against observed (satellite) extent in an unseen basin? Searches did not find one; a targeted search of the Fraehr et al. 2024 paper (extrapolation beyond training range, referenced only via search snippet) and of the UrbanFloodBench preprint would help.
- Licences of the Zenodo records (7764418, 7516408, 10688079) and the Kaggle UrbanFloodBench copy were not opened.
- MaxFloodCast (peak depth, Harris County) and FloodGNN-GRU were seen only in search snippets and are not cited.
- Out of scope, one line: how to build a hydraulic model of the lower Siret/Danube (other researcher).

## Review
Reviewed: 2026-11-11, by a reviewer who did not write this file.

Method and its limits: every cited URL was opened through a fetch tool that reads the page and reports sentences back. Quotes were checked against what it returned as exact text. The last 2,500 to 25,000 characters of the four long Copernicus pages (mostly references) were not read. Three arXiv abstracts were returned as summaries plus exact-phrase confirmations, not as full verbatim text. No fetched page contained instructions addressed to the reader.

Counts: 22 verified, 3 unsupported, 1 misquoted, 0 unreachable.

### Verdicts
1. `verified`, with a correction. The quote is the start of a longer sentence ("... over two squared domains of sizes 6.4×6.4 and 12.8×12.8 km2 ..."). The paper states "a squared domain of 64×64 grids of length 100 m" and "128×128 grids of length 100 m", and "The model outputs are the estimated water depth and unit discharge". Correction: training used only the 64×64 set (60 train, 20 validation, 20 test). The 128×128 set (10 runs) is test-only, so "trained on 64x64 / 128x128" is wrong for the 128×128 part. Published 30 Nov 2023.
2. `verified`. Both quotes are exact but cut short (source: "... 40 hours, forming our database." and "... River Têt (France), at decision-relevant lead times."). The full text gives "a mesh of 412,844 nodes and 2,013,374 elements" and "40 floods are used for training and 16 floods are kept held out for evaluation". arXiv v1 is dated 3 Apr 2026; the HTML page also shows an unexplained "August 24, 2026".
3. `verified`. Quote exact (abstract). 1 m DEM, TELEMAC-2D and "1 h duration precipitation events (block rainfall)" are all in the text. Published 24 Feb 2023.
4. `verified`. Quote exact; "We extracted a total of 1250 patches for training and validation of the model" confirms the patch count. Published 18 Dec 2024.
5. `verified`. Quote exact. 10 m DEM, 128×128 patches, two holdout events, CREST-iMAP with ANUGA-Hydro all confirmed. arXiv 29 Jul 2023; also in the ICCV 2023 workshop proceedings.
6. `unsupported`. The quote is exact and the facts about the paper hold (ResNet-18, LISFLOOD-FP, Daymet "from 1981 to 2019", "testing on the subsequent year", Chicago only). But the paper does not present itself as physics-informed or hybrid: it calls its design a "statistical-neural architecture" and mentions physics-informed models only as other people's work. It is not evidence that "physics-informed / hybrid variants exist". Usable only if reworded as a Gaussian-process plus ResNet surrogate.
7. `verified`. Quote exact; diffusion model, HEC-RAS, DEM plus coarse depth as conditioning, and the four catchments (Wollombi, Chowilla, Burnett River, Lismore) are in the abstract. Superseded: see "Missed" below (Flood-LDM).
8. `verified`. Quote exact; U-Net, Wupper, Germany confirmed on the abstract page (22 Apr 2026). Number of simulations and code are not stated there.
9. `verified`. The quote is the start of a longer sentence ("... due to the unavailability of detailed data of the storm drainage system."). The unquoted statement is also in the conclusions: "the accuracy of the predicted flood maps by a data-driven model highly depends on the accuracy" of the hydrodynamic simulations used for training. Each simulator named was confirmed under its own claim (SWE-GNN uses Delft3D-FM).
10. `verified` for the two Zenodo datasets only. Quote exact; the Seleem DOI 10.5281/zenodo.7516408 is in that paper's data statement. I opened both records: both are CC BY 4.0 (7764418 is 115 MB, 7516408 is 44 GB). The UrbanFloodBench sentence stays unverified and must not be used: the University of Sydney record returned HTTP 403 to me as well, and a search did not confirm CC BY-NC.
11. `verified`. Quote exact (abstract). "an Nvidia Tesla V100S-PCIE-32GB for training and deployment" and "ranging from 100 to 600 times faster than the numerical model on the GPU" are in the text; the 100 to 600 range is for the 128×128 test set. Training time is not reported (only "150 epochs with early stopping").
12. `verified` for the numbers. Quote exact. The text gives "about 0.4 s on a single NVIDIA A100 GPU" against "about 180 min on 56 CPU cores", so the 27,000x ratio compares one GPU with 56 CPU cores. The last sentence of the claim ("the only reference run that is also the cost the team would need to pay") is the researcher's interpretation and is in no source.
13. `misquoted`. The quoted sentence is not in the source (the researcher said it was a paraphrase). The facts are correct. The real sentences are: "The U-Net models were trained using a high-performance machine with an NVIDIA Quadro P4000 GPU", "The training time ranged from 20 min to 48 h and from 10 min to 2 h for the U-Net and RF models respectively." and "The U-net models needed around 20 s to predict and map the water depth, while the RF models took around 3 min."
14. `verified`. The quote is the start of "Training time per epoch is 72 sec wallclock time and inference time is 0.002 sec/sample." RTX 3090 and "the maximum epochs used is 60" confirmed. No speed-up against the simulator is reported.
15. `verified`. Quote exact (abstract). "a simulation time of 48 h" and "a constant input discharge of 50 m3 s−1 as the boundary condition" confirmed. The authors write "The model should also be validated in real case studies".
16. `verified`. Quote exact (abstract). Supporting text: "For the CNN models, the loss of performance was also considerable but clearly less pronounced than for the RF models", transfer learning with "only 10 % of the available training data", and "The city has a relatively flat topography."
17. `verified`. Both quotes exact. Both test cities (Lucerne, Singapore) were retrained on one rainfall event.
18. `verified`. Quote exact. The text says "We then trained an FNO model using D1–D3 data and tested on D4", on the two holdout events. Two notes: the paper never calls its own experiment "zero-shot", and it only places D4 in the Brays Bayou watershed, without saying where D1 to D3 are.
19. `verified`. Quote exact, and the abstract sentence does continue "... with hydroclimatological similarity to the U.S. Midwest". Note: the models are trained on synthetic physics-based simulations and evaluated on real flood events in Iowa, so "its training region (Iowa/US Midwest)" is loose wording. Still a preprint; no journal version found.
20. `unsupported`. There is no source and no quote, so nothing can be verified. My own searches did not find a counterexample either (see "Missed"), but that is still a negative search result. Keep it as "not found" and do not use it as a finding.
21. `verified`. Quote exact (README). MIT licence shown in the sidebar; the README says "results: Contains trained models and respective configuration files, used for the paper's results." The repo date could not be confirmed (no commit dates shown). I did not list the files inside `results`.
22. `verified`. Quote exact. Licence now found: Zenodo record 10688079 is CC BY 4.0 and contains `models_weights.zip` (1.2 GB). The GitHub repo shows no licence.
23. `unsupported`. The quote exists, but in the HTML full text, not on the cited abstract page, and it only shows that PhysicsNeMo was the framework. It does not support "no pretrained river-flood surrogate exists". The Mercier and Wupper parts hold (no code link on either page). The absence claim as a whole is a search result, not a sourced fact.
24. `verified`. Quote exact. Also in the text: "the proposed model does not strictly enforce conservation laws such as mass balance" and "we provide no theoretical guarantee that stability can be enforced for an indefinite number of time steps". Partly outdated, see mSWE-GNN below.
25. `verified`. Quote exact (start of a longer sentence). Forcing uncertainty appears as "where the inflow hydrograph is itself uncertain and may be revised over time". The reference for the maps is "the original high-resolution Telemac simulation", not observations.
26. `verified`. Quote exact. Drainage limit: "The lack of representation of the drainage network could represent a limit to the transferability of the model".

### What the researcher missed
- **SWE-GNN has a successor.** mSWE-GNN (Bentivoglio et al., NHESS, 23 Jan 2025) says the earlier models "cannot accommodate time-varying boundary conditions" and that SWE-GNN "requires the first time step to be given by a numerical solver". It is tested on a real area, "dike ring 15 Lopiker- and Krimpenerwaard in the Netherlands". Without fine-tuning the result was modest; after fine-tuning on one simulation it reports "mean absolute errors of 0.12 m for water depth", and the speed-up drops to "4 to 8 times" once the fine-tuning run is counted. Training is still on 100 synthetic Perlin-noise simulations from Delft3D, dike-breach only. This is the most relevant real-terrain result for a GNN and it supports the file's conclusion. https://nhess.copernicus.org/articles/25/335/2025/
- **Claim 7 is superseded.** The same group published Flood-LDM (arXiv 2511.14033, 18 Nov 2025, accepted at WACV 2026), whose title claims "zero-shot High-Resolution Flood Mapping". I read the abstract only; accuracy is stated against fine-grid simulated maps, not observations. https://arxiv.org/abs/2511.14033
- **The largest cross-catchment test is not in section 4.** Guo et al. 2022 (J. Hydrol., doi 10.1016/j.jhydrol.2022.127726), which Cache et al. describe as having "assessed the terrain generalizability of a data-driven flood model across 656 catchments in Switzerland", with no rainfall input. I could not open the paper itself (HTTP 403), so this rests on Cache et al.'s description. https://hess.copernicus.org/articles/28/5443/2024/
- **More unseen-site tests, all against the simulator.** A CIROH 2026 poster trains a CNN on LISFLOOD-FP at three sites and tests on two unseen ones, where it "replicates LISFLOOD-FP flood extents" (https://ciroh.ua.edu/abstracts/transferable-deep-learning-flood-inundation-mapping-trained-on-lisflood-fp-simulations/). EGUsphere preprint 2026-1982 (12 May 2026) is "trained on high-fidelity two-dimensional shallow-water simulations"; the fetch tool reported a referee comment that all targets come from ANUGA (https://egusphere.copernicus.org/preprints/2026/egusphere-2026-1982/). Neither contradicts claim 20.
- **Possible counterexample to the open question, not opened.** Frame et al. 2024 (doi 10.1029/2024GL109424) is described in a search snippet as trained on satellite-observed floods and generalising to new locations. Wiley returned HTTP 403 and the PDF was unreadable. It is not a simulator surrogate, so it is outside this file's scope, but it bears on the first open question. https://doi.org/10.1029/2024GL109424
- **Relevant to claim 23, search snippet only.** NVIDIA PhysicsNeMo ships a HydroGraphNet flood example (White River near Muncie, HEC-RAS ground truth). It is site-specific and I found no released checkpoint. https://docs.nvidia.com/physicsnemo/26.05/physicsnemo/examples/weather/flood_modeling/hydrographnet/README.html
- **Vendor involvement, no independent validation.** The Mercier preprint has an NVIDIA co-author, uses NVIDIA's framework and hardware, is not peer-reviewed, and has no validation against observations. https://arxiv.org/html/2604.02876
- **Licences that were listed as "not found".** All three Zenodo records are CC BY 4.0: https://zenodo.org/records/7764418, https://zenodo.org/records/7516408, https://zenodo.org/records/10688079. UrbanFloodBench remains unverified (https://ses.library.usyd.edu.au/handle/2123/35562, HTTP 403).

### Problems in "Relevance to LandHorizon"
The main verdict (roadmap item, nothing to build, no change to pipeline, contract or dependencies) respects the constraints: no ML in the plan, the 11 Dec deadline, the person-hours, Python 3.14. It is backed by verified claims 2, 9, 12, 15, 16, 17, 24 and 25. The problems are in the details.
- **Bullet 1 leans on claim 20**, which is unsupported. The conflict with the independent-sensor rule should rest on claims 9 and 25 instead (training and reference data are simulator output; Mercier's map reference is the Telemac run).
- **"Calibrated" is not in any source.** The sources say the surrogates are trained on simulations, not that the models were calibrated. "Every credible surrogate needs a model of the area" also outruns the evidence: claim 19, Guo et al. and Flood-LDM train elsewhere and transfer. None of those is shown to work against observations, so the conclusion holds, but "every" should go.
- **"With a clear licence" is wrong for Cache et al.** The weights are CC BY 4.0 on Zenodo (https://zenodo.org/records/10688079). The real obstacles are that it is a 1 m urban pluvial model that needs a local event, and LandHorizon's terrain is the Copernicus 30 m DEM. "None found" also cites claim 23, which is unsupported: write it as "not found in our searches".
- **The pitch line promises validation against GFM.** No verified claim shows any surrogate validated against satellite extent. GFM is Sentinel-1, the same source as the product's own flood layer, and the constraints record that GFM fails the spring dry-window test (9.06 % against a 1 % limit). It is independent of the simulator but is not a clean reference, and the line should say so. "Scenario maps" must also not turn into return periods or probabilities claimed from our own data.
- **The cost bullet has no verified backing.** "Weeks of expert work" is the researcher's own estimate (it is labelled as such). The U-Net comparison rests on claim 13, whose quote was wrong although its numbers are right. The student-credit figure is marked "(course notes)" in the constraints and was not rechecked.
- **Claim 12's last sentence** should not be carried into a synthesis; it is not from the source.
