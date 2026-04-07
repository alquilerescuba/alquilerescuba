from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    class Meta:
        verbose_name_plural = "Categorías"
    def __str__(self):
        return self.name

class Property(models.Model):
    LOCATIONS = [
        ("vinales", "Viñales, Pinar del Río"),
        ("playa", "Playa, La Habana"),
        ("vedado", "Vedado, La Habana"),
        ("nuevo_vedado", "Nuevo Vedado, La Habana"),
        ("centro_habana", "Centro Habana, La Habana"),
        ("habana_vieja", "Habana Vieja, La Habana"),
        ("fontanar", "Fontanar, La Habana"),
        ("calabazar", "Calabazar, La Habana"),
        ("boca_ciega", "Boca Ciega, La Habana"),
        ("guanabo", "Guanabo, La Habana"),
        ("penas_altas", "Peñas Altas, La Habana"),
        ("varadero", "Varadero, Matanzas"),
        ("santa_marta", "Santa Marta, Matanzas"),
    ]
    RENTAL_TYPES = [("entire", "Toda la propiedad"), ("room", "Por habitaciones")]
    PRICE_CATEGORIES = [("night", "Por noche"), ("month", "Por mes"), ("daypass", "Pasadía")]

    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de propiedad")
    location = models.CharField(max_length=50, choices=LOCATIONS, verbose_name="Ubicación")
    address = models.CharField(max_length=255, verbose_name="Dirección exacta")
    bedrooms = models.PositiveIntegerField(default=1, verbose_name="Habitaciones")
    guests = models.PositiveIntegerField(default=1, verbose_name="Huéspedes")
    bathrooms = models.PositiveIntegerField(default=1, verbose_name="Baños")
    rental_type = models.CharField(max_length=20, choices=RENTAL_TYPES, default="entire", verbose_name="Tipo de alquiler")

    has_wifi = models.BooleanField(default=False, verbose_name="WiFi")
    has_tv = models.BooleanField(default=False, verbose_name="TV")
    has_kitchen = models.BooleanField(default=False, verbose_name="Cocina")
    has_parking = models.BooleanField(default=False, verbose_name="Parqueo")
    has_pool = models.BooleanField(default=False, verbose_name="Piscina")
    has_ac = models.BooleanField(default=False, verbose_name="Aire acondicionado")
    has_billiard = models.BooleanField(default=False, verbose_name="Billar")
    has_washing_machine = models.BooleanField(default=False, verbose_name="Lavadora")
    has_charcoal_oven = models.BooleanField(default=False, verbose_name="Horno al carbón")

    price_category = models.CharField(max_length=10, choices=PRICE_CATEGORIES, default="night", verbose_name="Categoría de precio")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio por noche (USD)")
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio por mes (USD)")
    price_per_daypass = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio por pasadía (USD)")

    # Changed upload_to to "" to match root bucket access
    main_photo = models.ImageField(upload_to="", verbose_name="Foto principal")
    is_active = models.BooleanField(default=True, verbose_name="Activa")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Propiedad"
        verbose_name_plural = "Propiedades"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.get_location_display()}"

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        return round(sum(r.rating for r in reviews) / reviews.count(), 1) if reviews.exists() else 0

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name="images", on_delete=models.CASCADE)
    # Changed upload_to to ""
    image = models.ImageField(upload_to="", verbose_name="Imagen")
    caption = models.CharField(max_length=100, blank=True)

class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i}★") for i in range(1, 6)])
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ["property", "user"]
