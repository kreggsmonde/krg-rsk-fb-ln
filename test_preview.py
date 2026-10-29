"""
Скрипт быстрого теста: генерирует 15-секундный фрагмент для проверки синтеза аудио,
позиции пузыря субтитров, эквалайзера и визуального рендера.
"""
import sys, os
from auto_pipeline import run_auto_pipeline

if __name__ == "__main__":
    print("[TEST] Запуск 15-секундного теста превью...")
    run_auto_pipeline(
        target_minutes=0.5,
        topic="Искусство слушать друг друга в паре",
        dry_run=True,
        preview_seconds=15.0
    )
