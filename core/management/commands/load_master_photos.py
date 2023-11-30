import os
from django.core.management.base import BaseCommand
from core.models import Master, GalleryPicture

class Command(BaseCommand): 
    help = 'Load gallery photos for each master'

    def handle(self, *args, **kwargs):
        masters = Master.objects.all()
        for master in masters:
            self.load_photos_for_master(master)

    def load_photos_for_master(self, master):
        existing_media_path = 'media'
        gallery_path = os.path.join(existing_media_path, 'gallery')
        gallery_photos = [filename for filename in os.listdir(gallery_path) if filename.startswith(str(master.id) + "-")]
        for filename in gallery_photos:
            _, created = GalleryPicture.objects.get_or_create(master=master, image=os.path.join('gallery', filename))
            if created:
                print(f'Photo {filename} linked to master {master.id}')
            else:
                print(f'Photo {filename} already linked to master {master.id}')