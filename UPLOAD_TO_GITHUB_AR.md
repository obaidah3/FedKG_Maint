# رفع المشروع النهائي الحالي إلى GitHub

هذه الحزمة نسخة Azure Phases 1–5 تشمل الكود والنتائج التجميعية و51 تقريرًا/إعدادًا أصليًا صغيرًا من Drive مع بصمات تحقق SHA-256؛ **لا تحوي البيانات الخام أو سرّ Groq أو ملفات إجابات الحالات الخاصة**.

- فك ضغط الملف، ثم افتح Git Bash داخل المجلد الناتج.
- نفذ بعد إنشاء مستودع GitHub فارغ `FedKG-Maint`:

```bash
git init
git branch -M main
git add .
git status
git commit -m "Azure phases 1-5: KG-grounded Groq explainability closure"
git remote add origin https://github.com/YOUR_USERNAME/FedKG-Maint.git
git push -u origin main
```

لو كنت رفعت نسخة سابقة من نفس المشروع إلى GitHub، لا تنشئ تاريخ Git جديد فوق القديم؛ انقل الملفات المحدثة إلى نسخة الـ repository الحالية، ثم `git add . && git commit -m "Add Phase 5 results" && git push`.

لا ترفع `GROQ_API_KEY`, `.env`, بيانات Drive الخام، `phase5_all_explanations_private.json` أو `human_review_blinded.csv` إلى repo عام. توثيق التقييم الأوتوماتيكي موجود في `reports/PHASE5_FINAL_EXPLAINABILITY.md`، ولا يجب وصفه على أنه Human Evaluation.

### قبل الـ commit (فحص الإصدار النهائي)

```bash
python scripts/validate_repo.py
python scripts/verify_original_drive_reports.py
python -m unittest discover -s tests -v
```

ملاحظة: تم السماح لملف `fedkg_shared_ontology.ttl` الخاص **بالمخطط المشترك فقط** بالرفع في `.gitignore`. ملفات KG الخاصة بالمصانع (`factory_*.ttl`) تظل مستبعدة. تقارير `results/original_drive_reports/` هي مخرجات صغيرة، وليست مصدرًا لإعادة الحساب الكامل للنتائج دون بيانات Drive.
