# Generated by Django 2.0 on 2019-10-27 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_auto_20191026_2224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='yuyue',
            options={'ordering': ['yuyuetime']},
        ),
        migrations.AlterField(
            model_name='myuser',
            name='user_img',
            field=models.TextField(default='https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2781007512,3931003336&fm=26&gp=0.jpg', max_length=200, verbose_name='用户头像'),
        ),
    ]
