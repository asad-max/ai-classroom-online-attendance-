import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Clear and recreate media/faces and media/encodings directories."

    def handle(self, *args, **kwargs):
        media_root = settings.MEDIA_ROOT
        targets = ['faces', 'encodings']

        for folder in targets:
            path = os.path.join(media_root, folder)

            if os.path.exists(path):
                shutil.rmtree(path)
                self.stdout.write(self.style.SUCCESS(f"🗑 Deleted: {path}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Folder not found: {path}"))

            os.makedirs(path, exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f"📁 Recreated: {path}"))

        self.stdout.write(self.style.SUCCESS("✅ Face data reset complete."))
