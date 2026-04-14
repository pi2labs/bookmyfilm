from django.db.models import Q
from django.http import JsonResponse
from collections import defaultdict
from datetime import date, datetime, timedelta
from django.utils import timezone

from .models import Movie, Showtime

WINDOW_DAYS = 5

# UI uses English names; DB may store German spellings (e.g. München).
_CITY_ALIASES = {
    "munich": ["Munich", "München", "Muenchen"],
    "hamburg": ["Hamburg"],
    "frankfurt": ["Frankfurt", "Frankfurt am Main"],
    "berlin": ["Berlin"],
    "stuttgart": ["Stuttgart"],
    "bonn": ["Bonn"],
    "düsseldorf": ["Düsseldorf", "Duesseldorf", "Dusseldorf"],
    "dusseldorf": ["Düsseldorf", "Duesseldorf", "Dusseldorf"],
}


def _city_q(city_param):
    """OR match on canonical + alias names (case-insensitive)."""
    if not city_param or not str(city_param).strip():
        return None
    raw = str(city_param).strip()
    key = raw.lower()
    names = _CITY_ALIASES.get(key, [raw])
    q = Q()
    for name in names:
        q |= Q(theater__city__iexact=name)
    return q


def _show_start_datetime(showtime):
    """Combine show date + start time in the active timezone for comparison with now."""
    tz = timezone.get_current_timezone()
    naive = datetime.combine(showtime.date, showtime.start_time)
    if timezone.is_naive(naive):
        return timezone.make_aware(naive, tz)
    return naive


def _parse_date_param(value):
    if not value or not str(value).strip():
        return None
    try:
        return date.fromisoformat(str(value).strip())
    except ValueError:
        return None


def _window_bounds():
    today = timezone.localdate()
    last_day = today + timedelta(days=WINDOW_DAYS - 1)
    return today, last_day


def movie_list(request):
    city = (request.GET.get("city") or "").strip()

    today, last_day = _window_bounds()
    now = timezone.now()

    show_qs = Showtime.objects.filter(date__gte=today, date__lte=last_day)
    cq = _city_q(city)
    if cq is not None:
        show_qs = show_qs.filter(cq)

    movie_ids = set()
    for s in show_qs.select_related("movie"):
        if _show_start_datetime(s) < now:
            continue
        movie_ids.add(s.movie_id)

    if city:
        movies = Movie.objects.filter(id__in=movie_ids).order_by("title")
    else:
        movies = Movie.objects.all().order_by("title")

    data = []
    for m in movies:
        data.append({
            "id": m.id,
            "slug": m.slug,
            "title": m.title,
            "poster_url": m.poster_url,
            "rating": float(m.rating) if m.rating else None,
            "genres": m.genres or "",
            "release_date": m.release_date,
        })

    return JsonResponse(data, safe=False)


def movie_detail(request, movie_title):
    city = (request.GET.get("city") or "").strip()
    filter_date = _parse_date_param(request.GET.get("date"))

    movie = Movie.objects.get(slug=movie_title)

    today = timezone.localdate()
    release_date = movie.release_date

    if release_date and release_date > today:
        start_date = release_date
    else:
        start_date = today
        
    last_date = start_date + timedelta(days=WINDOW_DAYS - 1)

    now = timezone.now()

    showtimes = Showtime.objects.filter(movie=movie).select_related(
        "theater", "screen"
    ).prefetch_related("formats").order_by(
        "date", "start_time", "theater__name"
    )

    showtimes = showtimes.filter(date__gte=start_date, date__lte=last_date)
    cq = _city_q(city)
    if cq is not None:
        showtimes = showtimes.filter(cq)
    if filter_date:
        showtimes = showtimes.filter(date=filter_date)

    grouped_by_date = defaultdict(lambda: defaultdict(list))

    for s in showtimes:
        if _show_start_datetime(s) < now:
            continue

        theater_key = f"{s.theater.name} ({s.theater.city})"
        date_key = s.date.isoformat()

        grouped_by_date[date_key][theater_key].append({
            "date": s.date.isoformat(),
            "start_time": s.start_time.strftime("%H:%M"),
            "end_time": s.end_time.strftime("%H:%M") if s.end_time else None,
            "isOriginalVersion": s.original_version,
            "screen": s.screen.name,
            "price": float(s.price),
            "formats": [f.name for f in s.formats.all()],
            "language": s.language,
            "booking_url": s.booking_link,
            "wheelchair_access": s.wheelchair_accessible,
        })

    showtimes_by_date = [
        {"date": d, "theaters": dict(theaters)}
        for d, theaters in sorted(grouped_by_date.items())
    ]

    data = {
        "id": movie.id,
        "slug": movie.slug,
        "title": movie.title,
        "release_date": movie.release_date,
        "rating": float(movie.rating) if movie.rating else None,
        "age_group": movie.age_group,
        "duration": "%dh %02dm" % divmod(movie.duration, 60),
        "genres": movie.genres,
        "poster_url": movie.poster_url,
        "trailer_url": movie.trailer_url,
        "synopsis": movie.synopsis,
        "showtimes_by_date": showtimes_by_date,
    }

    return JsonResponse(data)
