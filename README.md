# راهنمای مخزن Self-Structuring Object Cognition

این مخزن در حال حاضر آرشیو یک مسیر فکری و مجموعه‌ای از نمونه‌های اولیه است؛ نه یک نظریهٔ تثبیت‌شده و نه یک سامانهٔ شناختی آمادهٔ اجرا.

## وضعیت نگهداری

- نسخهٔ اصلی تا Commit `8fbfa4601641571b08171d44fbc0a3b75324d8e4` در شاخهٔ `archive/original-2026-08-11` ثابت شده است.
- هیچ‌یک از Notebookها یا فایل‌های اصلی در مرحلهٔ فهرست‌برداری حذف، جابه‌جا یا بازنویسی نشده‌اند.
- اسناد جدید «نمایه و نقد» هستند و جای منبع اصلی را نمی‌گیرند.

## از کجا شروع کنیم؟

1. [نقشهٔ دانشی و راهنمای Obsidian](docs/knowledge_map/README.md)
2. [نقشهٔ دیداری مسیر پروژه](docs/knowledge_map/SSOC_Project_Map.canvas)
3. [داشبورد وضعیت واقعی کار](docs/knowledge_map/research_dashboard.md)
4. [مسیر قوی و مسیرهای ضعیف](docs/knowledge_map/project_flow.md)
5. [کارت امتیاز ایده‌ها](docs/knowledge_map/idea_scorecard.md)
6. [فهرست فایل‌ها](docs/inventory/file_inventory.md)
7. [نقشهٔ موضوعی](docs/inventory/topic_map.md)
8. [نمایهٔ سلول‌ها](docs/inventory/cell_index.md)
9. [تناقض‌ها و ریسک‌ها](docs/inventory/contradictions_and_risks.md)
10. [ارزیابی فنی کد](docs/inventory/technical_findings.md)
11. [منابع نیازمند راستی‌آزمایی](docs/inventory/references_to_verify.md)
12. [راهبرد ساخت هستهٔ بدیهیات عقلی](docs/knowledge_map/rational_core_strategy.md)
13. [مشخصات اجرایی نسخهٔ ۰٫۱](specs/rational_core_v0_1.md)
14. [واژه‌نامهٔ عملیاتی](specs/glossary.md)
15. [آزمایش ۰۱: تناقض](specs/experiment_01.md)
16. [نتیجهٔ آزمایش ۰۱](docs/experiments/experiment_01_result.md)

## وضعیت مرحله

مرحلهٔ حفظ نسخهٔ اصلی و فهرست‌برداری سطح اول تمام شده است. نسخهٔ آزمایشی ۰٫۱ هسته نیز به‌صورت یک بستهٔ مستقل و قطعی ساخته شده است. این نسخه فقط تناقض مستقیم را در ورودی کنترل‌شده می‌آزماید و نباید نظریهٔ نهایی یا شاهد فهم عمومی تلقی شود.

## اجرای نسخهٔ ۰٫۱

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m rational_core examples/contradiction.json --pretty
PYTHONPATH=src:. python scripts/run_experiment_01.py
```

بستهٔ جدید وابستگی اجرایی خارجی ندارد. فایل `aristotle_logic.py` و Notebookهای اصلی برای حفظ آرشیو تغییر نکرده‌اند.

## قاعدهٔ کار

اصل محتوا حفظ می‌شود. «گفتهٔ کاربر»، «پاسخ تولیدشده»، «ادعا»، «فرضیه»، «کد» و «نتیجهٔ واقعی اجرا» در مراحل بعد از هم جدا می‌شوند. هیچ ادعایی صرفاً به دلیل تکرارشدن در چند Notebook معتبر تلقی نمی‌شود.
