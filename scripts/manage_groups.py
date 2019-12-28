from django.contrib.auth.models import User, Group, Permission

def run():

    # Create GROUPS and set permissions
    from django.contrib.auth.models import User, Group, Permission
    mygroup, created = Group.objects.get_or_create(name='Admin')
    permission1 = Permission.objects.get(name='Can add profile')
    permission2 = Permission.objects.get(name='Can change profile')
    permission3 = Permission.objects.get(name='Can view profile')
    permission4 = Permission.objects.get(name='Can add pacient')
    permission5 = Permission.objects.get(name='Can change pacient')
    permission6 = Permission.objects.get(name='Can view pacient')
    mygroup.permissions.add(permission1, permission2, permission3, permission4, permission5, permission6)
    mygroup.save()

    mygroup, created = Group.objects.get_or_create(name='Medic')
    permission1 = Permission.objects.get(name='Can view pacient')
    permission2 = Permission.objects.get(name='Can view drug')

    permission3 = Permission.objects.get(name='Can add exam')
    permission4 = Permission.objects.get(name='Can change exam')
    permission5 = Permission.objects.get(name='Can view exam')

    permission6 = Permission.objects.get(name='Can add prescription')
    permission7 = Permission.objects.get(name='Can change prescription')
    permission8 = Permission.objects.get(name='Can view prescription')

    permission9 = Permission.objects.get(name='Can view appointment')

    mygroup.permissions.add(permission1, permission2, permission3, permission4, permission5, permission6, permission7,
                            permission8, permission9)
    mygroup.save()

    mygroup, created = Group.objects.get_or_create(name='Secretary')
    permission1 = Permission.objects.get(name='Can view profile')

    permission2 = Permission.objects.get(name='Can add pacient')
    permission3 = Permission.objects.get(name='Can change pacient')
    permission4 = Permission.objects.get(name='Can view pacient')

    permission6 = Permission.objects.get(name='Can add drug')
    permission7 = Permission.objects.get(name='Can change drug')
    permission8 = Permission.objects.get(name='Can view drug')

    permission9 = Permission.objects.get(name='Can add exam')
    permission10 = Permission.objects.get(name='Can change exam')
    permission11 = Permission.objects.get(name='Can view exam')

    permission12 = Permission.objects.get(name='Can add appointment')
    permission13 = Permission.objects.get(name='Can change appointment')
    permission14 = Permission.objects.get(name='Can view appointment')

    mygroup.permissions.add(permission1, permission2, permission3, permission4, permission5, permission6, permission7,
                            permission8, permission9, permission10, permission11, permission12, permission13,
                            permission14)
    mygroup.save()


    '''
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
    '''