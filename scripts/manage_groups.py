from django.contrib.auth.models import User, Group, Permission

def run():
    # ADD permissions to a USER
    from django.contrib.auth.models import User, Group, Permission
    a = User.objects.get(id=1)
    permission = Permission.objects.get(name='Can view profile')
    a.user_permissions.add(permission)
    a.save()

    # ADD permissions to a GROUP
    from django.contrib.auth.models import User, Group, Permission
    mygroup, created = Group.objects.get_or_create(name='Medic')
    permission = Permission.objects.get(name='Can add profile')
    mygroup.permissions.add(permission)
    mygroup.save()

    # ADD USER to a GROUP
    from django.contrib.auth.models import User, Group, Permission
    mygroup, created = Group.objects.get_or_create(name='Medic')
    a = User.objects.get(id=5)
    mygroup.user_set.add(a)
    mygroup.save()