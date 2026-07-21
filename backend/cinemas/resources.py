# cinemas/resources.py

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .widgets import TheaterForeignKeyWidget, TheaterManyToManyWidget, MovieForeignKeyWidget

from .models import (
    Movie,
    Person,
    Theater,
    Showtime,
    Screen,
    Format,
    MovieTheater
)

class TheaterResource(resources.ModelResource):
    display_name = fields.Field(column_name="display_name")

    class Meta:
        model = Theater
        fields = ("id", "name", "city", "display_name")

    def dehydrate_display_name(self, obj):
        return f"{obj.name} ({obj.city})"

class MovieTheaterResource(resources.ModelResource):

    movie = fields.Field(
        column_name="movie",
        attribute="movie",
        widget=MovieForeignKeyWidget()
    )

    theater = fields.Field(
        column_name="theater",
        attribute="theater",
        widget=TheaterForeignKeyWidget()
    )

    class Meta:
        model = MovieTheater
        fields = (
            "id",
            "movie",
            "theater",
        )
        export_order = (
            "movie",
            "theater",
        )

class ScreenResource(resources.ModelResource):
    theater = fields.Field(
        column_name='theater',
        attribute='theater',
        widget=TheaterForeignKeyWidget()
    )

    class Meta:
        model = Screen
        fields = ("id", "name", "theater")


class ShowtimeResource(resources.ModelResource):
    movie = fields.Field(
        column_name='movie',
        attribute='movie',
        widget=ForeignKeyWidget(Movie, 'title')
    )

    theater = fields.Field(
        column_name='theater',
        attribute='theater',
        widget=ForeignKeyWidget(Theater, 'name')
    )

    screen = fields.Field(
        column_name='screen',
        attribute='screen',
        widget=ForeignKeyWidget(Screen, 'name')
    )

    formats = fields.Field(
        column_name='formats',
        attribute='formats',
        widget=ManyToManyWidget(Format, field='name')
    )

    class Meta:
        model = Showtime