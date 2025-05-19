from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from registration.models import Patient, Insurance
from examination.models import Radionuclide, Pharmaceutical, Procedure, SPECT

username = 'admin'
password = 'admin'

# Buat superuser
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email='admin@mail.com')

if not Insurance.objects.filter(name="Personal").exists():
    Insurance.objects.create(name='Personal')

if not Insurance.objects.filter(name="BPJS").exists():
    Insurance.objects.create(name='BPJS')

if not Radionuclide.objects.filter(name="Tc-99m").exists():
    Radionuclide.objects.create(name='Tc-99m')

if not Pharmaceutical.objects.filter(name="MDP").exists():
    Pharmaceutical.objects.create(name='MDP')

if not Procedure.objects.filter(name="Bone scan").exists():
    Procedure.objects.create(name='Bone scan')

# Buat grup baru jika belum ada
group, created = Group.objects.get_or_create(name='Petugas Input Pasien')

# Ambil semua permission untuk model Pasien
content_type = ContentType.objects.get_for_model(Patient)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(Insurance)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(Pharmaceutical)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(Radionuclide)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(Procedure)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(SPECT)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]