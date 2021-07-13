from django.contrib import admin
from .models import Groups,Organization,Membershiplevel, Team_Messages
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models

# Register your models here.
admin.site.register(Groups)
admin.site.register(Organization)
admin.site.register(Membershiplevel)

class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)

class Team_MessagesAdmin(admin.ModelAdmin):
    list_filter = ['team','user', 'timestamp']
    list_display = ['team','user', 'timestamp', 'content']
    search_fields = ['team__title','user__username', 'content']
    readonly_field = ['id','user', 'timestamp']

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = Team_Messages

admin.site.register(Team_Messages,Team_MessagesAdmin)
