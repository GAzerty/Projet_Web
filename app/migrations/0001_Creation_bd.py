# Generated by Django 2.2.1 on 2019-05-10 23:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Joueur',
            fields=[
                ('idJoueur', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'joueur',
            },
        ),
        migrations.CreateModel(
            name='Quartier',
            fields=[
                ('idQuartier', models.AutoField(primary_key=True, serialize=False)),
                ('nomQuartier', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'quartier',
            },
        ),
        migrations.CreateModel(
            name='Stade',
            fields=[
                ('idStade', models.AutoField(primary_key=True, serialize=False)),
                ('nomStade', models.CharField(max_length=255)),
                ('rueStade', models.CharField(max_length=255)),
                ('villeStade', models.CharField(max_length=255)),
                ('codepostalStade', models.IntegerField()),
                ('nombreTerrain', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('imageStade', models.ImageField(upload_to='stades/')),
                ('quartierStade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Quartier')),
            ],
            options={
                'db_table': 'stade',
            },
        ),
        migrations.CreateModel(
            name='Rencontre',
            fields=[
                ('idRencontre', models.AutoField(primary_key=True, serialize=False)),
                ('scoreLocaux', models.IntegerField(blank=True, default=0)),
                ('scoreVisiteurs', models.IntegerField(blank=True, default=0)),
                ('dateRencontre', models.DateField()),
                ('heureRencontre', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2359)])),
                ('lieuRencontre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Stade')),
            ],
            options={
                'db_table': 'rencontre',
            },
        ),
        migrations.CreateModel(
            name='Participer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreButs', models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('equipe', models.CharField(choices=[('LOC', 'Locaux'), ('VIS', 'Visiteurs')], max_length=3)),
                ('idJoueur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Joueur')),
                ('idRencontre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Rencontre')),
            ],
            options={
                'db_table': 'participer',
            },
        ),
        migrations.AddField(
            model_name='joueur',
            name='quartierJoueur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Quartier'),
        ),
        migrations.CreateModel(
            name='Inviter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idJoueur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joueur_guest', to='app.Joueur')),
                ('idRencontre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Rencontre')),
                ('joueurDemandeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joueur_invite', to='app.Joueur')),
            ],
            options={
                'db_table': 'inviter',
            },
        ),
        migrations.CreateModel(
            name='Amis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etatJoueur1', models.CharField(choices=[('AT', 'Attente'), ('AC', 'Accepter')], default='AC', max_length=2)),
                ('etatJoueur2', models.CharField(choices=[('AT', 'Attente'), ('AC', 'Accepter')], default='AT', max_length=2)),
                ('joueur1Amis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joueur_sender', to='app.Joueur')),
                ('joueur2Amis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='joueur_recipient', to='app.Joueur')),
            ],
            options={
                'db_table': 'amis',
            },
        ),
        migrations.AddConstraint(
            model_name='participer',
            constraint=models.UniqueConstraint(fields=('idJoueur', 'idRencontre'), name='participer_unique'),
        ),
        migrations.AddConstraint(
            model_name='inviter',
            constraint=models.UniqueConstraint(fields=('idJoueur', 'idRencontre'), name='inviter_unique'),
        ),
        migrations.AddConstraint(
            model_name='amis',
            constraint=models.UniqueConstraint(fields=('joueur1Amis', 'joueur2Amis'), name='amis_unique'),
        ),
    ]
