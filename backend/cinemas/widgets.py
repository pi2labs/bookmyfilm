from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import Theater, Movie
        
class TheaterForeignKeyWidget(ForeignKeyWidget):
    def __init__(self):
        super().__init__(Theater, "id")

    def render(self, value, obj=None, **kwargs):
        if not value:
            return ""

        return f"{value.name} ({value.city})"

    def clean(self, value, row=None, **kwargs):
        if not value:
            return None

        if value.endswith(")") and "(" in value:
            name, city = value.rsplit("(", 1)

            name = name.strip()
            city = city.replace(")", "").strip()

            theater, _ = Theater.objects.get_or_create(
                name=name,
                city=city
            )

            return theater

        return Theater.objects.get(pk=value)

class TheaterManyToManyWidget(ManyToManyWidget):

    def __init__(self):
        super().__init__(Theater, separator=",")

    def render(self, value, obj=None, **kwargs):
        try:
            print("RENDER VALUE:", value, type(value))

            if value is None:
                return ""

            return ", ".join(str(theater) for theater in value.all())
        except AttributeError:
            return ""

    def clean(self, value, row=None, **kwargs):
        if not value:
            return []

        theaters = []

        for item in value.split(","):
            item = item.strip()

            name, city = item.rsplit("(", 1)

            theaters.append(
                Theater.objects.get(
                    name=name.strip(),
                    city=city[:-1].strip()
                )
            )

        return theaters


class MovieForeignKeyWidget(ForeignKeyWidget):
    def __init__(self):
        super().__init__(Movie, "title")

    def render(self, value, obj=None, **kwargs):
        return value.title if value else ""

    def clean(self, value, row=None, **kwargs):
        if not value:
            return None

        return Movie.objects.get(title=value)