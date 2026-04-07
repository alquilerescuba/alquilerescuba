from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'), # Asegúrate de que este nombre coincida con tu primera migración
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='main_photo',
            field=models.ImageField(upload_to='properties/', verbose_name='Foto principal'),
        ),
        migrations.AlterField(
            model_name='propertyimage',
            name='image',
            field=models.ImageField(upload_to='properties/gallery/', verbose_name='Imagen'),
        ),
    ]
