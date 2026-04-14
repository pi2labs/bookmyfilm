from django.contrib import admin
from django import forms

from .models import Movie, Theater, Format, Screen, Showtime, Person, MovieCast

# Register your models here.
admin.site.register(Person)
admin.site.register(Format)
admin.site.register(MovieCast)

@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class ShowtimeInline(admin.TabularInline):
    model = Showtime
    extra = 5  # show 5 empty rows
    autocomplete_fields = ['theater', 'screen']
    filter_horizontal = ('formats',)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ShowtimeInline]


@admin.action(description="Duplicate selected showtimes")
def duplicate_showtimes(modeladmin, request, queryset):
    for obj in queryset:
        formats = obj.formats.all()
        obj.pk = None
        obj.save()
        obj.formats.set(formats)

class ShowtimeAdminForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If editing existing object
        if self.instance and self.instance.theater_id:
            self.fields['screen'].queryset = Screen.objects.filter(
                theater_id=self.instance.theater_id
            )
        else:
            self.fields['screen'].queryset = Screen.objects.none()


class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'theater', 'date', 'formatted_time', 'screen', 'price')
    actions = [duplicate_showtimes]
    ordering = ('screen', 'date', 'start_time')
    save_as = True
    list_filter = ('screen', 'date', 'theater')
    form = ShowtimeAdminForm

    def formatted_time(self, obj):
        return obj.start_time.strftime("%H:%M")  # ✅ 24-hour format

    formatted_time.short_description = "Start Time"


admin.site.register(Showtime, ShowtimeAdmin)
