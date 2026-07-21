from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django import forms

from .models import Movie, Theater, Format, Screen, Showtime, Person, MovieCast, MovieTheater
from .resources import  ShowtimeResource, TheaterResource, ScreenResource, MovieTheaterResource

# Register your models here.

class PersonAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
admin.site.register(Person, PersonAdmin)

class FormatAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
admin.site.register(Format, FormatAdmin)

class MovieCastAdmin(ImportExportModelAdmin):
    search_fields = ('movie__title', 'person__name')
admin.site.register(MovieCast, MovieCastAdmin)

@admin.register(Screen)
class ScreenAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    resource_class = ScreenResource

@admin.register(Theater)
class TheaterAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    resource_class = TheaterResource

class ShowtimeInline(admin.TabularInline):
    model = Showtime
    extra = 5  # show 5 empty rows
    autocomplete_fields = ['theater', 'screen']
    filter_horizontal = ('formats',)


class MovieTheaterInline(admin.TabularInline):
    model = MovieTheater
    extra = 1
    autocomplete_fields = ("theater",)

@admin.register(Movie)
class MovieAdmin(ImportExportModelAdmin):
    search_fields = ('title',)
    inlines = [ShowtimeInline, MovieTheaterInline]
    autocomplete_fields = ('cast', 'directors', 'writers')


@admin.register(MovieTheater)
class MovieTheaterAdmin(ImportExportModelAdmin):
    autocomplete_fields = ("movie", "theater")
    search_fields = (
        "movie__title",
        "theater__name",
        "theater__city",
    )
    resource_class = MovieTheaterResource

    list_display = (
        "movie",
        "theater",
    )


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


class ShowtimeAdmin(ImportExportModelAdmin):
    class Meta:
        unique_together = (
        'movie',
        'theater',
        'screen',
        'date',
        'start_time',
    )
    
    list_display = ('movie', 'theater', 'date', 'formatted_time', 'screen', 'price')
    autocomplete_fields = ('movie', 'theater', 'screen')
    actions = [duplicate_showtimes]
    ordering = ('screen', 'date', 'start_time')
    save_as = True
    list_filter = ('screen', 'date', 'theater')
    form = ShowtimeAdminForm
    resource_class = ShowtimeResource

    def formatted_time(self, obj):
        return obj.start_time.strftime("%H:%M")  # ✅ 24-hour format

    formatted_time.short_description = "Start Time"


admin.site.register(Showtime, ShowtimeAdmin)
