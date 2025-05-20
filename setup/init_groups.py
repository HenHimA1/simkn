from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from registration.models import Patient, Insurance
from examination.models import PETRadionuclide, PETPharmaceutical, PETProcedure, PETDiagnosis, SPECTRadionuclide, SPECTPharmaceutical, SPECTProcedure, SPECTDiagnosis, SPECT, PET, Location, SequenceCT

username = 'admin'
password = 'admin'

# Buat superuser
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email='admin@mail.com')

if not Insurance.objects.filter(name="Personal").exists():
    Insurance.objects.create(name='Personal')

if not Insurance.objects.filter(name="BPJS").exists():
    Insurance.objects.create(name='BPJS')

if not SPECTRadionuclide.objects.filter(name="Tc-99m").exists():
    SPECTRadionuclide.objects.create(name='Tc-99m')

if not SPECTPharmaceutical.objects.filter(name="MDP").exists():
    SPECTPharmaceutical.objects.create(name='MDP')

if not SPECTProcedure.objects.filter(name="Bone scan").exists():
    SPECTProcedure.objects.create(name='Bone scan')

if not PETRadionuclide.objects.filter(name="F-18").exists():
    PETRadionuclide.objects.create(name='F-18')

if not PETPharmaceutical.objects.filter(name="FDG").exists():
    PETPharmaceutical.objects.create(name='FDG')

if not PETProcedure.objects.filter(name="Whole body scan").exists():
    PETProcedure.objects.create(name='Whole body scan')

# Buat grup baru jika belum ada
group, created = Group.objects.get_or_create(name='Petugas Input Pasien')

# Ambil semua permission untuk model Pasien
content_type = ContentType.objects.get_for_model(Patient)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(Insurance)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(PETPharmaceutical)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(PETRadionuclide)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(PETProcedure)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(PETDiagnosis)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(SPECTPharmaceutical)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(SPECTRadionuclide)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(SPECTProcedure)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(SPECTDiagnosis)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(SPECT)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(PET)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]


content_type = ContentType.objects.get_for_model(Location)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]

content_type = ContentType.objects.get_for_model(SequenceCT)
permissions = Permission.objects.filter(content_type=content_type)
[group.permissions.add(perm.id) for perm in permissions]