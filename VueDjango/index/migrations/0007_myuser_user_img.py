# Generated by Django 2.0 on 2019-10-26 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_auto_20191014_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='user_img',
            field=models.CharField(default='https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1381398688,4084204307&fm=26&gp=0.jpg', max_length=100, verbose_name='用户头像'),
        ),
    ]