from django.core.management.base import BaseCommand

from simple_forums import models
from simple_forums.backends.search import get_search_class


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        if not models.Thread.objects.count():
            self.stdout.write(
                self.style.WARNING("There are no threads to index."))

        backend = get_search_class()()

        # clear out old index first
        backend.wipe()

        count = 0
        for thread in models.Thread.objects.all():
            backend.add(thread)
            count += 1

        # SUCCESS style was introduced in django 1.9
        if hasattr(self.style, 'SUCCESS'):
            out = self.style.SUCCESS("Updated %d thread(s)" % count)
        else:
            out = "Updated %d thread(s)" % count

        self.stdout.write(out)
