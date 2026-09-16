---
type: obsidian-operation-guide
status: active
updated: 2026-09-16
scope: SSOC only
---

# راه‌اندازی و سینک Obsidian برای SSOC

این راهنما فقط برای همین مخزن است. هیچ مخزن دیگری را وارد این Vault نکنید.

## نقطهٔ شروع

1. در Obsidian گزینهٔ **Open folder as vault** را بزنید.
2. پوشهٔ محلی مخزن `Self-Structuring-Object-Cognition` را انتخاب کنید.
3. این فایل را باز کنید: [[docs/knowledge_map/SSOC_Project_Map.canvas]].
4. برای شروع خواندن، [[docs/knowledge_map/README|راهنمای نقشهٔ دانشی]] را باز کنید.

## چه چیزهایی در Git ثبت می‌شوند؟

- یادداشت‌های Markdown در `docs/knowledge_map/`
- نقشه‌های Canvas با پسوند `.canvas`
- تغییرهای آگاهانهٔ ساختار Vault

تنظیمات شخصیِ چیدمان پنجره‌ها ثبت نمی‌شوند. این تنظیمات در `.obsidian/workspace.json` و `.obsidian/workspaces.json` هستند و در `.gitignore` آمده‌اند.

## روند امن همگام‌سازی

هر بار پیش از شروع کار:

```bash
git status
git pull --ff-only
```

پس از تغییر نقشه یا یادداشت:

```bash
git add docs/knowledge_map
git commit -m "Update SSOC knowledge map"
git push
```

اگر `git status` تغییرهای دیگری نشان داد، پیش از Pull آن‌ها را بررسی کنید. روی تغییرهای محلیِ نامشخص Pull نکنید.

## مرز نقشه

نقشه باید به فایل‌های واقعی پروژه پیوند داشته باشد و وضعیت، تصمیم، فرضیه و پرسش باز را از هم جدا نگه دارد. تغییر کد به‌تنهایی نقشه را به‌روز نمی‌کند؛ در هر تغییر مفهومیِ مهم، یادداشت یا Canvas مرتبط نیز باید آگاهانه به‌روز شود.
