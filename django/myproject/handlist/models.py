from django.db import models

class Author(models.Model):
    author_id = models.IntegerField(primary_key=True)
    last_name = models.CharField(max_length=450)
    first_name = models.CharField(max_length=450)
    class Meta:
        db_table = u'Author'

class AuthorLiteratureId(models.Model):
    id = models.IntegerField(primary_key=True)
    author_id = models.IntegerField(unique=True)
    literature_id = models.IntegerField()
    class Meta:
        db_table = u'Author_literature_id'

class Characters(models.Model):
    characters_id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=30, blank=True)
    character = models.CharField(max_length=300, blank=True)
    definition = models.CharField(max_length=6000, blank=True)
    comment = models.CharField(max_length=6000, blank=True)
    class Meta:
        db_table = u'Characters'

class CharacterStates(models.Model):
    character_states_id = models.IntegerField(primary_key=True)
    characters = models.ForeignKey(Characters, null=True, blank=True)
    state = models.CharField(max_length=300, blank=True)
    accepted_values = models.CharField(max_length=150, blank=True)
    class Meta:
        db_table = u'Character_States'

# class Countries(models.Model):
#     country_id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=450)
#     class Meta:
#         db_table = u'Countries'

class Species(models.Model):
    species_id = models.IntegerField(primary_key=True)
    genus = models.CharField(max_length=450)
    species = models.CharField(max_length=450)
    subspecies = models.CharField(max_length=450)
    describer = models.CharField(max_length=450)
    class Meta:
        db_table = u'Species'

class Anatomy(models.Model):
    anatomy_id = models.IntegerField(primary_key=True)
    species_id_id = models.IntegerField()
    organ = models.CharField(max_length=450)
    literature_id = models.IntegerField(null=True, blank=True)
    notes = models.CharField(max_length=5000)
    class Meta:
        db_table = u'anatomy'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=240)
    class Meta:
        db_table = u'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group_id = models.IntegerField(unique=True)
    permission_id = models.IntegerField()
    class Meta:
        db_table = u'auth_group_permissions'

class AuthMessage(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    message = models.TextField()
    class Meta:
        db_table = u'auth_message'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    content_type_id = models.IntegerField()
    codename = models.CharField(unique=True, max_length=300)
    class Meta:
        db_table = u'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=90)
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=384)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    class Meta:
        db_table = u'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    group_id = models.IntegerField()
    class Meta:
        db_table = u'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(unique=True)
    permission_id = models.IntegerField()
    class Meta:
        db_table = u'auth_user_user_permissions'

class Behavior(models.Model):
    behavior_id = models.IntegerField(primary_key=True)
    species_id_id = models.IntegerField()
    literature_id_id = models.IntegerField()
    notes = models.CharField(max_length=45000)
    class Meta:
        db_table = u'behavior'

class Color(models.Model):
    color_id = models.IntegerField(primary_key=True)
    species_id_id = models.IntegerField()
    literature_id_id = models.IntegerField()
    organ = models.CharField(max_length=450)
    notes = models.CharField(max_length=5000)
    class Meta:
        db_table = u'color'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=300)
    app_label = models.CharField(unique=True, max_length=300)
    model = models.CharField(unique=True, max_length=300)
    class Meta:
        db_table = u'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=120, primary_key=True)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        db_table = u'django_session'

class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)
    domain = models.CharField(max_length=300)
    name = models.CharField(max_length=150)
    class Meta:
        db_table = u'django_site'

class Ecology(models.Model):
    ecology_id = models.IntegerField(primary_key=True)
    species_id_id = models.IntegerField()
    literature_id_id = models.IntegerField()
    notes = models.CharField(max_length=45000)
    class Meta:
        db_table = u'ecology'

class Literature(models.Model):
    literature_id = models.IntegerField(primary_key=True)
    species_id_id = models.IntegerField()
    title = models.CharField(max_length=9000)
    journal = models.CharField(max_length=4500)
    journal_code = models.CharField(max_length=450)
    volume = models.IntegerField(null=True, blank=True)
    issue = models.IntegerField(null=True, blank=True)
    start_page = models.IntegerField(null=True, blank=True)
    stop_page = models.IntegerField(null=True, blank=True)
    start_quote = models.IntegerField(null=True, blank=True)
    stop_quote = models.IntegerField(null=True, blank=True)
    temp_citation = models.CharField(max_length=5000)
    class Meta:
        db_table = u'literature'

class Range(models.Model):
    range_id = models.IntegerField(primary_key=True)
    species_id_id = models.IntegerField()
    two_letter_code = models.CharField(max_length=36)
    countries = models.CharField(max_length=1000)
    notes = models.CharField(max_length=45000)
    class Meta:
        db_table = u'range'

class Synonymy(models.Model):
    synonymy_id = models.IntegerField(primary_key=True)
    species_id_id = models.IntegerField()
    author = models.CharField(max_length=450)
    # literature_id_id = models.IntegerField()  # removed for the time being...
    type_locality = models.CharField(max_length=4500)
    subspecies = models.CharField(max_length=450)
    class Meta:
        db_table = u'synonymy'


class CharacterData(models.Model):
    character_data_id = models.IntegerField(primary_key=True)
    characters = models.ForeignKey(Characters, null=True, blank=True)
    species = models.ForeignKey(Species, null=True, blank=True)
    observed_state = models.CharField(max_length=60, blank=True)
    class Meta:
        db_table = u'Character_Data'

