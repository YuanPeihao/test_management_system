# Generated by Django 3.2.3 on 2021-05-20 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mgmt_sys', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testmgmtcase',
            name='case_log',
        ),
        migrations.CreateModel(
            name='TestMgmtCaseLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_log_pub_date', models.DateTimeField(verbose_name='date published')),
                ('case_log_error_msg', models.CharField(max_length=500)),
                ('case_log_file_name', models.CharField(max_length=100)),
                ('case_log_file_url', models.CharField(max_length=100)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mgmt_sys.testmgmtcase')),
            ],
        ),
    ]
