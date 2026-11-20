from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_ent", "0003_auto_20210610_1716"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entinstitution",
            name="ent",
            field=models.CharField(
                choices=[
                    ("HDF", "Hauts-de-France"),
                    ("CORRELYCE", "Corrélyce"),
                    ("GMINVENT", "GMInvent"),
                ],
                default="HDF",
                max_length=12,
                verbose_name="Environnements Numériques de Travail",
            ),
        ),
    ]
