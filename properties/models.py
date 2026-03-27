from django.db import models


class Category(models.Model):
    """Casa o Apartamento"""

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Property(models.Model):
    """La propiedad que se alquila"""

    # Ubicaciones ordenadas por provincias
    LOCATIONS = [
        # Pinar del Río
        ("vinales", "Viñales, Pinar del Río"),
        # La Habana
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
        # Matanzas
        ("varadero", "Varadero, Matanzas"),
        ("santa_marta", "Santa Marta, Matanzas"),
    ]

    # Tipo de alquiler: Toda la propiedad o Por habitaciones
    RENTAL_TYPES = [
        ("entire", "Toda la propiedad"),
        ("room", "Por habitaciones"),
    ]

    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de propiedad"
    )

    location = models.CharField(
        max_length=50, choices=LOCATIONS, verbose_name="Ubicación"
    )

    address = models.CharField(max_length=255, verbose_name="Dirección exacta")

    bedrooms = models.PositiveIntegerField(default=1, verbose_name="Habitaciones")
    guests = models.PositiveIntegerField(default=1, verbose_name="Huéspedes")
    bathrooms = models.PositiveIntegerField(default=1, verbose_name="Baños")

    rental_type = models.CharField(
        max_length=20,
        choices=RENTAL_TYPES,
        default="entire",
        verbose_name="Tipo de alquiler",
    )

    # Amenidades
    has_wifi = models.BooleanField(default=False, verbose_name="WiFi")
    has_tv = models.BooleanField(default=False, verbose_name="TV")
    has_kitchen = models.BooleanField(default=False, verbose_name="Cocina")
    has_parking = models.BooleanField(default=False, verbose_name="Parqueo")
    has_pool = models.BooleanField(default=False, verbose_name="Piscina")
    has_ac = models.BooleanField(default=False, verbose_name="Aire acondicionado")
    has_billiard = models.BooleanField(default=False, verbose_name="Billar")
    has_washing_machine = models.BooleanField(default=False, verbose_name="Lavadora")
    has_charcoal_oven = models.BooleanField(
        default=False, verbose_name="Horno al carbón"
    )

    # Categoría de precio
    PRICE_CATEGORIES = [
        ("night", "Por noche"),
        ("month", "Por mes"),
        ("daypass", "Pasadía"),
    ]

    price_category = models.CharField(
        max_length=10,
        choices=PRICE_CATEGORIES,
        default="night",
        verbose_name="Categoría de precio",
    )

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio por noche (USD)",
        null=True,
        blank=True,
    )

    price_per_month = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio por mes (USD)",
        null=True,
        blank=True,
    )

    price_per_daypass = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Precio por pasadía (USD)",
        null=True,
        blank=True,
    )

    main_photo = models.ImageField(
        upload_to="properties/", verbose_name="Foto principal"
    )

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
        """Calcula el promedio de valoraciones de la propiedad"""
        reviews = self.reviews.all()
        if reviews.exists():
            return sum(r.rating for r in reviews) / reviews.count()
        return 0

    @property
    def average_rating(self):
        """Calcula el promedio de valoraciones como en Airbnb"""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    @property
    def reviews_count(self):
        """Cantidad de valoraciones"""
        return self.reviews.count()


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Propiedad",
    )
    image = models.ImageField(upload_to="properties/gallery/", verbose_name="Imagen")
    caption = models.CharField(max_length=100, blank=True, verbose_name="Pie de foto")

    class Meta:
        verbose_name = "Imagen de propiedad"
        verbose_name_plural = "Imágenes de propiedades"

    def __str__(self):
        return f"Imagen de {self.property.title}"


class Booking(models.Model):
    """Reserva de una propiedad"""

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Propiedad",
    )
    start_date = models.DateField(verbose_name="Fecha de entrada")
    end_date = models.DateField(verbose_name="Fecha de salida")
    guest_name = models.CharField(max_length=100, verbose_name="Nombre del huésped")
    guest_email = models.EmailField(verbose_name="Email")
    guest_phone = models.CharField(max_length=20, verbose_name="Teléfono")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.property.title}: {self.start_date} a {self.end_date}"


class Review(models.Model):
    """Valoración de una propiedad por un usuario"""

    RATING_CHOICES = [
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    ]

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Propiedad",
    )
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Usuario",
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, verbose_name="Calificación"
    )
    comment = models.TextField(verbose_name="Comentario", max_length=500)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de valoración"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última edición")

    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"
        ordering = ["-created_at"]
        unique_together = ["property", "user"]  # Un usuario solo una vez por propiedad

    def __str__(self):
        return f"{self.user.username} - {self.property.title} - {self.rating}★"
