# FedKG-Maint — مراجعة تقنية مستقلة مقابل متطلبات المشروع

تاريخ المراجعة: 2026-10-25

## نطاق المراجعة وحدود التحقق

تم تحليل 16 ملفًا مرفوعًا: PDF للمتطلبات، ستة Jupyter Notebooks، تقرير Markdown، وثمانية ملفات CSV/JSON Audit artifacts (بما فيها split audit بصيغتين). مراجعة الكود تمت بصورة ثابتة static review لجميع خلايا Python، مع تحليل النتائج النصية المحفوظة؛ لم يتم إعادة تدريب النماذج أو تشغيل المشروع من الصفر بسبب غياب مجموعات بيانات Azure الخام، مجلد `prep_v3/` المنشأ أثناء التشغيل، النماذج المدرّبة، ملفات التنبؤ، ومخرجات Phase 3 v2 المرجعية. نجاح اختبارات من داخل Notebook يعكس مخرجات محفوظة في الملف ولا يمثل تحققًا تنفيذيًا جديدًا مستقلاً.

إجمالي خلايا الكود المراجعة: 51. جميعها تُحلَّل نحويًا باستخدام `ast.parse` دون أخطاء SyntaxError؛ لا توجد مخرجات Error ظاهرة داخل الـNotebooks المرفوعة. جميع قيم `execution_count` غير موجودة (None)، رغم احتفاظ معظم الـNotebooks بنصوص نتائج تشغيل. لا يثبت ذلك التلاعب؛ لكنه يمنع التثبت من ترتيب التنفيذ عبر Metadata وحدها.

## مصفوفة الالتزام بالتكليف

| بند التكليف | الحالة من الملفات المقدمة | الدليل/الفجوة |
|---|---|---|
| Data Collection: NASA C-MAPSS + Azure | جزئي | Azure مستخدم؛ لا تنفيذ موثق لـNASA C-MAPSS |
| Simulated non-IID factories and independent site | منفذ بنطاق محاكاة | خمسة مصانع × 20 Machine، وFactory 5 محجوزة إشرافيًا؛ هناك معايرة غير إشرافية على المصنع الخامس |
| Feature engineering and 24-hour target | منفذ | 25 Feature بآفاق rolling 24h و7d؛ هدف 24h؛ Purge windows واختبارات زمنية |
| Local normalization per factory | منفذ بنطاق المحاكاة | `prep_v3` ينشئ خمسة local scalers؛ `Privacy_Utility_LocalNorm_v1` يستخدم local policy؛ توجد تجارب أخرى تستعمل global |
| Local maintenance knowledge graphs with ontology | منفذ بنيويًا | RDF/Turtle مع 5 graphs وshared ontology؛ لا تنبؤ باستخدام KG ولا توصيات maintenance مدعومة بنمذجة أسباب |
| Two distinct federated strategies vs local-only and central | غير موثق اكتمالها | FedAvg/ClippedFedAvg/DP-FedAvg ومتوسط مركزي Linear في الملفات المقدمة؛ ملف Phase 3 v2 الأساسي غير مرفق؛ لا local-only training يمكن تدقيقه |
| Privacy mechanism and trade-off | جزئي متقدم | Gaussian client-update DP مع RDP accountant وتجارب sigma؛ لا end-to-end DP ولا secure aggregation حقيقية |
| LLM+KG explanation and grounded-vs-ungrounded | غير مقدم | لا Notebook أو نتائج توضح LLM retrieval-grounding، human evaluation أو hallucination testing |
| Evaluation: PR-AUC/F1, communication, heterogeneity | جزئي | PR-AUC/F1/ROC-AUC/event recall وcluster bootstrap؛ لا تحليل موثق لكلفة الاتصال وتفاوت عدد المشاركين أو stress run |
| Ablations and robust statistical evidence | جزئي | no-maintenance ablation وnormalization comparison، DP-vs-clipped bootstrap؛ لا graph/LLM ablations؛ اختبار محدود إلى 20 machine و3 seeds |

## تحليل مراحل التنفيذ

### 1. Data Preparation v3

**ما يفعله الكود فعليًا:** بيانات Azure في الجداول الخمسة Telemetry, Errors, Failures, Maintenance, Machines؛ يحسب `label_failure_24h=1` عندما توجد Failure لنفس الماكينة في الفترة `(t, t+24h]`؛ يتحقق عبر ثلاث دوال مستقلة؛ يستبعد آخر 24 صفًا لكل ماكينة؛ ينتج Features Past-only وLinear/Tree-ready Parquet artifacts، بالإضافة إلى local/global scalers وتحليل Data Leakage.

**القيم المحفوظة داخل Notebook:** raw telemetry 876,100؛ 100 Machine؛ 5 factories؛ train 557,200/11,664 positive، validation 68,000/1,133، test_time_late 69,920/1,377، test_site_late 17,480/384، test_site_full 87,380/1,440. الاختبار الرئيسي لـFactory 5 بعد feature-only local calibration 87,360 rows ويحتوي 60 distinct failure events.

**إيجابيات:** المستقبل غير مستخدم في rolling stats (الحساب على `shift(1)`)، Events تُحسب عبر `merge_asof` مع `allow_exact_matches=False`، استخدام عدم تداخل مفاتيح calibration/test، Purge للـ24 ساعة قبل validation/test، اختبار `F-1` على 200 صف لكل split واختبار Positive Control (`F-2`). جميعها أدلة داخلية جيدة لكنها ليست إثباتًا عامًا بعدم وجود كل أنواع leakage.

**تنبيهات:** تقسيم المصنع بواسطة machine-model quotas محاكاة وليست خمسة مواقع مستقلة حقيقيًا؛ كتلة stress ذات توزيع type-shift محفوظة فقط ولم تظهر نتائج تشغيل لها. الـLocalScaler الخاص بالمصنع الخامس يستعمل بياناته غير الموسومة قبل التقييم؛ التعميم هنا Adaptation وليس Zero-shot. توليد الـFeatures والـScalers يجري في محاكاة مركزية، وليس منع مشاركة raw data مبرهنًا عمليًا. Maintenance سجل تفاعلي: قرابة 97.6% من سجلات الـFailures لها replacement لنفس المكون عند نفس الساعة؛ استخدام *السابق فقط* جيد، لكنه قد يجعل Recency proxy for past failures.

### 2. Centralized Baselines

يحوي LogReg وHistGradientBoosting وأساسات heuristic وprevalence؛ يستخدم تكرارات machine bootstrap مع 1000 replicate ويختار hyperparameters من Validation.

`test_site_full` PR-AUC: HGB global/full 0.925، HGB global/no-maintenance 0.680، LogReg global/full 0.659، LogReg local/full 0.638، HGB local/full 0.396، prevalence ≈0.0165. HGB global/full أعلى من FedAvg compact linear في Phase 3، لكن **هذه معماريات مختلفة وعدد Features مختلف؛ ليست مقارنة مناسبة لقياس تكلفة Federated Learning وحدها**. الفرق بين HGB local وglobal قد ينتج من عدم تناسق معنى كل Feature بين Client-specific scalers في نموذج واحد.

لا يظهر تنفيذ local-only model في Phase 2؛ هو صراحة مرحلة centralized baselines فقط.

### 3. Privacy Utility v3 (Global Normalization)

تستخدم أربع Factory Clients للـTraining، Factory 5 Held-out؛ 7 Features من الـ25 (`volt`, `rotate`, `pressure`, `vibration`, error recency, has prior error, maintenance recency)، نموذج Linear = 8 Parameters، 3 Communication rounds، Seeds 42/43/44. Sweep على Local epochs =1/3، clip norms 0.02/0.05/0.1/0.2/0.5، noise multipliers 1.0/1.25/1.5/2.0، بإجمالي 40 configurations ×3 seeds=120 candidate DP runs. اختيار config بالـValidation فقط ثم Score للـHeld-out.

**المخرجات المحفوظة:** اختيار 1 local epoch، clip_norm=0.1، sigma=1.0؛ Gaussian-mechanism manual RDP epsilon ≈9.837642 عند delta=1e-5. Mean PR-AUC: DP-FedAvg 0.325846، ClippedFedAvg 0.295369، FedAvg 0.295369، CentralCompactLinear 0.377797.

**تفسير:** clipping/noise layers حقيقية من ناحية كود المحاكاة: `delta=local-base`، `clip_update(delta,C)`، `mean(clipped_deltas)`، ثم Gaussian noise std=`sigma*C/4`. لكن `ClippedFedAvg` و`FedAvg` متطابقان تقريبًا في النتائج المعروضة، ما يستدعي قياس عدد الـClient Updates التي جرى قصها فعلًا. DP أعلى في هذا الـBenchmark، ولا يثبت ذلك أن noise يحسن الأداء بشكل عام.

### 4. Local Normalization v1

هذا Notebook يعيد التجربة السابقة باستخدام `policy="local"` لكل Clients وFactory 5 بعد Calibration. أرقام النتائج المحفوظة: Mean PR-AUC DP 0.3186، ClippedFedAvg/FedAvg 0.2875، CentralCompactLinear 0.3702. اختيار epochs/clip/sigma مماثل (1/0.1/1)، والقيد نفسه epsilon≈9.8376. هذا أقرب إلى شرط local preprocessing من global v3.

**تناقض توثيقي محدد:** مقدمة الـNotebook تقول إنه *لم يتم تشغيله* وإن Outputs تم مسحها، بينما نسخته المرفوعة تحتوي على مخرجات تدريب واختبار وPASS. يجب تحديث المقدمة أو توفير Execution Provenance يثبت هل نُفّذ لاحقًا؛ لا يكفي الاستناد إلى الجملتين معًا. كما أن `execution_count` فارغ.

### 5. Closure Audit v2 + Markdown report

التقرير الموجود يراجع **global-policy v3** فقط، وليس LocalNorm v1. يقول إنه تحقق من 12 prediction files (4 methods ×3 seeds)، وأعاد PR-AUC، واستخدم paired machine-cluster bootstrap (2,000 replicate)، وأجرى مستقلًا RDP cross-check بواسطة `dp-accounting`، ونجح في 11/11 check.

الفرق المتوسط DP minus clipped هو +0.030477 PR-AUC، بفاصل 95% bootstrap [0.018166, 0.041067]. هذه نتيجة موجبة في نفس held-out machines، مشروطة بالنماذج الناتجة وبالمقارنات ذاتها، ولا تعني دلالة عالمية أو تكرارًا خارجيًا مستقلًا أو formal p-value.

إجمالي Epsilon المذكور صالح **فقط** للـclipped/noised aggregate channel تحت add/remove-one-client adjacency، denominator ثابت، all clients participate، trusted server. ليس ضمانًا لكل workflow؛ preprocessing وvalidation-based selection وcandidate-search وexternal release خارج حد الضمان. لا يوجد Audit مطابق بنفس المستوى لنظام LocalNorm في الملفات المقدمة. Notebook Audit نفسه لا يحتوي Outputs؛ ملف Markdown يحتوي نتائج Run سابق بحسب وصفه، ولا توجد prediction Parquets لإعادة تأكيد bootstrap من الصفر.

### 6. Phase 4 Local Knowledge Graphs

الـNotebook يقرأ Azure source tables، ويعيد استخدام Factory mapping من Prep v3، ويبني RDF ontology مشتركة (151 triples) وخمسة Local RDF/Turtle graphs، كل منها حوالي 161,000–162,000 triples (نحو 9.2MB). يعدّ 3,919 error occurrences، 3,286 maintenance events، 761 component failure records، و100 machines. `36/36` structural checks pass بحسب Outputs. الفرق بين 761 records و719 distinct failure (machine,timestamp) هو اختلاف وحدة العد، وليس بالضرورة تناقضًا.

الـOntology تحتوي Machine, Component, ErrorCode, ErrorOccurrence, MaintenanceEvent, FailureEvent, TelemetryDailySummary وخصائص وصفية؛ لا تحتوي Knowledge عن المسببات causal failure modes ولا MaintenanceAction recommendation class يمكن التحقق منه، ولذلك هي **Event/Observation KG** مفيدة ولكنها ليست reasoning engine مكتملة.

الدالة `retrieve_as_of` تطبق timestamp filter للأحداث، وتسمح فقط بتلخيصات الأيام المكتملة (`dailyDate < day(as_of)`)؛ هذا اتجاه صحيح لمنع مستقبل اليوم نفسه. لكن الاختبار المثبت Smoke Test واحد قرب آخر تاريخ، وليس adversarial negative-control suite في أوقات تاريخية متعددة. إنشاء Graph يشمل أحداث فشل مستقبلية بالنسبة لتواريخ Prediction التاريخية؛ استخدامه مباشرة دون enforced as-of filter قد يسبب Future Leakage، لذا لا يجب منح LLM وصولًا حرًا لكل الرسم البياني.

### 7. LLM + KG Integration

لا توجد ضمن 16 ملفًا مرحلة تستقبل prediction, machine ID, prediction timestamp؛ تسترجع Evidence حسب الوقت ومن رسم المصنع الصحيح؛ ثم تنشئ LLM explanation مع إسناد Evidence IDs وتتحقق من unsupported claims. لا توجد Ablation grounded vs no-KG ولا hallucination evaluation أو human evaluation.

## التعارضات المؤكدة بين الـArtifacts

ملفات `factory_heldout_split_audit.csv/.json`, `final_factory_label_audit.csv`, `final_model_feature_audit.csv`, `final_data_readiness_audit.json`, وغيرها تمثل مرحلة أقدم. تتفق في 557,200 train rows و68,000 validation rows، لكنها لا تتفق مع الـv3 في labels أو held-out test scope:

| المقارنة | Audit files الأقدم | prep_v3 notebook |
|---|---:|---:|
| Train positive rows | 11,637 | 11,664 |
| Validation positive rows | 1,076 | 1,133 |
| Held-out late positive rows | 312 | 384 |
| Held-out evaluation الأساسي | 17,480 | 87,380 |
| Number of documented scalers | 5 | 6 |

`missing_value_handling_audit.csv` يذكر 26 feature columns في مرحلة وسيطة، بينما prep_v3 يستبعد `has_prior_maintenance` الثابت ويستخدم 25 Model Features؛ يجب عدم اعتبار ذلك وحده عيبًا، لكن يجب توثيق اختلاف الإصدارات. `temporal_feature_audit.csv` يسجل missing values في خطوة وسيطة بينما ملف missing-handling audit يذكر صفرًا بعد المعالجة؛ هذا قابل للتفسير بإزالة missing values، وليس تعارضًا نهائيًا بالضرورة.

## فحص الربط والاعتماد بين الـNotebooks

```text
Project PDF
  ↓
Azure Raw CSVs (غير مرفقة)
  ↓
Data Preparation v3 (ينشئ prep_v3/ + fedkg_data.py + Parquet + local/global scalers)
  ├── Phase 2 Baselines (ينشئ fedkg_eval.py + baseline results)
  │     └── Phase 3 v2 أصلية (مرجعية مطلوبة ولكن Notebook ونتائجها غير مرفقة)
  │             ├── Phase 3 Privacy Utility v3  [global policy]
  │             │     └── Phase 3 Closure Audit + Final EN Report  [global فقط]
  │             └── Phase 3 Privacy LocalNorm v1 [local policy؛ نتائج محفوظة]
  └── Phase 4 Local KG (RDF/Turtle لكل مصنع؛ بلا model/KG integration حتى الآن)
            └── Phase 5 LLM + KG explanation (غير مقدم)
```

الـNotebooks ليست self-contained: تعتمد على مسارات `/content/drive/MyDrive/FedKG-Maint/...` ومخرجات مراحل سابقة، وبعض هذه المخرجات غير موجودة مع الملفات المرفوعة. لا يمكن إعادة التشغيل من هذه الحزمة وحدها. إعداد نسخ `requirements.txt` أو `environment.yml`، checksum manifest للـArtifacts، وملفات التشغيل المرجعية مطلوب لتقوية الـReproducibility.

## القضايا المرتبة حسب الأولوية

| Priority | Issue | Required acceptance criterion |
|---|---|---|
| P0 | انفصال إصدارات Audit v2/v3 | جميع الأرقام والتوزيعات تأتي من Manifest version واحد مع hash + Run ID |
| P0 | غياب baseline FedProx/personalized أو عدم توفر Phase 3 v2 الأصلية | نتائج على نفس data/policy/seeds لـFedAvg + Federated Strategy ثانية، local-only + centralized |
| P0 | غياب LLM explanation integration | pipeline end-to-end: prediction→time-safe KG retrieval→grounded output→automatic faithfulness checks |
| P0 | Privacy budget يغطي mechanism واحد لا workflow البحث الكامل | تصريح threat model واضح وحساب privacy composition لكل releases اللازمة أو تقييد claim لما هو مغطّى فقط |
| P1 | Closure على global بدل local | independent local-policy closure audit + prediction reproducibility + paired bootstrap |
| P1 | Test reused في مراحل متعددة | تثبيت final protocol وتقييم خارجي إضافي/نوع Factory Shift جديد غير مستخدم في الضبط |
| P1 | Stress manifest غير مقاس | مقارنة degree of heterogeneity وmodel-type shift مع قياس performance |
| P1 | Reported central full-feature vs compact FL ليس apples-to-apples | مقارنة موحدة architecture/features/splits/policy + إضافة results منفصلة لنماذج أكبر |
| P1 | KG يحتوي future events ويحمل source-private facts | enforce as-of and factory authorization + tests تضمن عدم إرجاع Future Facts أو معلومات مصانع أخرى |
| P1 | Communication cost / number of clients غير محللين | bytes transmitted/rounds/cost and curves under 2/3/4 participating clients حسب تصميم protocol |
| P2 | LocalNorm Notebook مقدمة تقول unexecuted رغم outputs | provenance metadata + نسخة وصف موحدة مع النتائج |
| P2 | Dependency environment وall raw/derived artifacts مفقودة | one-command replay، package lock، Artifact manifest وأكواد checksum |
| P2 | NASA dataset غير مستخدم | NASA branch إذا كان إلزاميًا أو توثيق موافقة تقصر النطاق على Azure |
| P2 | Evaluation limited to 3 seeds & 20 machines | additional seeds/sites + uncertainty by machine/event + non-inferiority targets ذات صلة هندسيًا |

## الترتيب الهندسي الصحيح لاستكمال النظام

1. **Freeze baseline**: اختر Prep v3 + `policy="local"` كمسار الامتثال، مع ربط Run IDs إلى Predictions وSplit Manifest؛ أعد إصدار كل Audits على هذا المسار.
2. **Complete federated experiments**: FedAvg, FedProx (أو Personalized FL)، DP-FedAvg، local-only وcentralized مع identical compact feature set أولًا، ثم full-feature model منفصل. سجّل PR-AUC, F1, event recall, false alarms/operating horizon.
3. **Close local privacy experiment**: privacy scope مصاغ بوضوح مع `dp-accounting` وCI paired across machines؛ راجع كل output من selection sweep قبل الادعاء بأي composition كلي.
4. **Secure KG retrieval layer**: per-factory data permissions؛ immutable timestamp filter؛ لا future failures ولا unfinished-day summaries في evidence. سجل Fact IDs وtimestamps وprovenance لكل استرجاع.
5. **Explainability prototype**: output JSON schema يحتوي model risk, observations, cited KG facts, suggested check/maintenance action, uncertainty; تعليمات تمنع ادعاءات سبب مباشر غير مثبت.
6. **Ablation and evaluation**: Grounded vs ungrounded LLM، KG facts removed، maintenance features removed، privacy off/on، factories/heterogeneity/communication، hallucination/faithfulness manual rubric.
7. **Reproducibility package**: all versions, external data source checksums, environment, output files, evaluation scripts, diagrams and final limitations.

## قرار المراجع

**Ready as research prototype building blocks: YES. Ready as a complete, fully verified 7-part project: NO.**

الأجزاء الأربعة المهمة (Preprocessing، Centralized Baselines، DP-client-update experiments، Local Knowledge Graphs) لديها أدلة تنفيذ جيدة داخل الملفات، لكن اختبار end-to-end ومقارنة FL المتوازنة وLLM+KG غير موثقين أو غير موجودين ضمن الحزمة. تقرير Phase 3 Closure هو نجاح محدود للبروتوكول المُراجع، وليس قبولًا لجميع متطلبات المشروع.
