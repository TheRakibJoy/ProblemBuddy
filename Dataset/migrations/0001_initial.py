from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Handle",
            fields=[
                (
                    "handle",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Problem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "tier",
                    models.CharField(
                        choices=[
                            ("pupil", "Pupil"),
                            ("specialist", "Specialist"),
                            ("expert", "Expert"),
                            ("candidate_master", "Candidate Master"),
                            ("master", "Master"),
                            ("international_master", "International Master"),
                            ("grandmaster", "Grandmaster"),
                            ("international_grandmaster", "International Grandmaster"),
                            ("legendary_grandmaster", "Legendary Grandmaster"),
                        ],
                        db_index=True,
                        max_length=32,
                    ),
                ),
                ("PID", models.IntegerField()),
                ("Index", models.CharField(max_length=3)),
                ("Rating", models.IntegerField(db_index=True, null=True)),
                ("Tags", models.CharField(max_length=600, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Counter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("tag_name", models.CharField(db_index=True, max_length=100)),
                (
                    "tier",
                    models.CharField(
                        choices=[
                            ("pupil", "Pupil"),
                            ("specialist", "Specialist"),
                            ("expert", "Expert"),
                            ("candidate_master", "Candidate Master"),
                            ("master", "Master"),
                            ("international_master", "International Master"),
                            ("grandmaster", "Grandmaster"),
                            ("international_grandmaster", "International Grandmaster"),
                            ("legendary_grandmaster", "Legendary Grandmaster"),
                        ],
                        db_index=True,
                        max_length=32,
                    ),
                ),
                ("count", models.IntegerField(default=0)),
            ],
        ),
        migrations.AddConstraint(
            model_name="problem",
            constraint=models.UniqueConstraint(
                fields=("tier", "PID", "Index"), name="unique_problem_per_tier"
            ),
        ),
        migrations.AddIndex(
            model_name="problem",
            index=models.Index(fields=["tier", "Rating"], name="dataset_pro_tier_rat_idx"),
        ),
        migrations.AddConstraint(
            model_name="counter",
            constraint=models.UniqueConstraint(
                fields=("tag_name", "tier"), name="unique_tag_per_tier"
            ),
        ),
    ]
