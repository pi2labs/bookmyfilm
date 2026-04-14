from django.db import models
from django.utils.text import slugify

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=255)
    photo_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    synopsis = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Minutes")
    genres=models.CharField(max_length=100, blank=True)
    age_group=models.CharField(max_length=2, blank=True)
    # 🎭 Many actors
    cast = models.ManyToManyField(Person, related_name='acted_movies', blank=True)

    # 🎥 Directors (can be multiple)
    directors = models.ManyToManyField(Person, related_name='directed_movies', blank=True)

    # ✍️ Writers
    writers = models.ManyToManyField(Person, related_name='written_movies', blank=True)

    # 📅 Release date
    release_date = models.DateField(null=True, blank=True)
    poster_url=models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)

    def generate_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1

        while Movie.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
            unique_slug = f"{slug}-{num}"
            num += 1

        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Theater(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.city})"
    

class Format(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Screen(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # Kino 01

    def __str__(self):
        return f"{self.theater} - {self.name}"


class Showtime(models.Model):
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE)
    booking_link=models.URLField()
    theater=models.ForeignKey(Theater, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)

    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)

    original_version = models.BooleanField(blank=True)

    # 🎥 Format
    formats = models.ManyToManyField(Format)

    # 💰 Price
    price = models.DecimalField(max_digits=6, decimal_places=2)
    language=models.CharField(max_length=50, blank=True, default="Deutsch")

    # ♿ Accessibility
    wheelchair_accessible = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.movie} - {self.theater} - {self.date} {self.start_time}"

class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role_name = models.CharField(max_length=255)