# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ExternalIdentifierSchemes(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField()
    url = models.CharField()
    description = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'external_identifier_schemes'


class FileExtensions(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    extension = models.CharField()
    type_name = models.CharField(blank=True, null=True)
    media_type = models.CharField(blank=True, null=True)
    description_url = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file_extensions'


class Funders(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    abbreviation = models.CharField()
    name = models.CharField()
    url = models.CharField()

    class Meta:
        managed = False
        db_table = 'funders'


class Licenses(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    abbreviation = models.CharField()
    name = models.CharField()
    url = models.CharField()

    class Meta:
        managed = False
        db_table = 'licenses'


class NameEntities(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    full_name = models.CharField()
    name_type = models.CharField()
    family_name = models.CharField(blank=True, null=True)
    given_name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'name_entities'


class NameEntityIdentifiers(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    identifier = models.CharField()
    external_identifier_scheme = models.ForeignKey(ExternalIdentifierSchemes, models.DO_NOTHING)
    name_entity = models.ForeignKey(NameEntities, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'name_entity_identifiers'


class RecordContributors(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    contributor_type = models.CharField(blank=True, null=True)
    name_entity = models.ForeignKey(NameEntities, models.DO_NOTHING)
    record = models.ForeignKey('Records', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'record_contributors'


class RecordCreators(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name_entity = models.ForeignKey(NameEntities, models.DO_NOTHING)
    record = models.ForeignKey('Records', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'record_creators'


class RecordFiles(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField()
    checksum = models.CharField(blank=True, null=True)
    size_bytes = models.BigIntegerField(blank=True, null=True)
    general_type = models.CharField()
    specific_type = models.CharField(blank=True, null=True)
    extension = models.ForeignKey(FileExtensions, models.DO_NOTHING)
    record = models.ForeignKey('Records', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'record_files'


class RecordFundings(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    award_number = models.CharField()
    award_title = models.CharField(blank=True, null=True)
    award_url = models.CharField(blank=True, null=True)
    funder = models.ForeignKey(Funders, models.DO_NOTHING, blank=True, null=True)
    record = models.ForeignKey('Records', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'record_fundings'


class RecordLicenses(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    license = models.ForeignKey(Licenses, models.DO_NOTHING)
    record = models.ForeignKey('Records', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'record_licenses'


class RecordRelations(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    related_identifier_type = models.CharField()
    relation_type = models.CharField()
    related_metadata_scheme = models.CharField(blank=True, null=True)
    scheme_uri = models.CharField(blank=True, null=True)
    scheme_type = models.CharField(blank=True, null=True)
    resource_type_general = models.CharField()
    source_record = models.ForeignKey('Records', models.DO_NOTHING)
    target_record = models.ForeignKey('Records', models.DO_NOTHING, related_name='recordrelations_target_record_set')

    class Meta:
        managed = False
        db_table = 'record_relations'
        unique_together = (('source_record', 'target_record'),)


class RecordSubjects(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    subject = models.JSONField()
    record = models.ForeignKey('Records', models.DO_NOTHING)
    subject_schema = models.ForeignKey('SubjectSchemas', models.DO_NOTHING)
    source_file = models.ForeignKey(RecordFiles, models.DO_NOTHING, blank=True, null=True)
    associated_file = models.ForeignKey(RecordFiles, models.DO_NOTHING, related_name='recordsubjects_associated_file_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'record_subjects'


class RecordTrails(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField()
    status_on = models.DateTimeField()
    record = models.ForeignKey('Records', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'record_trails'


class Records(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    title = models.CharField()
    description = models.CharField(blank=True, null=True)
    submission_type = models.CharField()
    general_type = models.CharField()
    specific_type = models.CharField(blank=True, null=True)
    doi = models.CharField(blank=True, null=True)
    days_until_release = models.IntegerField()
    doi_issued_date = models.DateField(blank=True, null=True)
    doi_status = models.CharField(blank=True, null=True)
    process_status = models.CharField()
    process_message = models.CharField(blank=True, null=True)
    publication_date = models.DateTimeField(blank=True, null=True)
    funding_description = models.CharField(blank=True, null=True)
    process_path = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records'


class SubjectSchemas(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    name = models.CharField(unique=True)
    json_schema = models.JSONField()
    description = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject_schemas'



####  tables in ADA database not needed for metadata


class RestFrameworkApiKeyApikey(models.Model):
    id = models.CharField(primary_key=True, max_length=150)
    created = models.DateTimeField()
    name = models.CharField(max_length=50)
    revoked = models.BooleanField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    hashed_key = models.CharField(max_length=150)
    prefix = models.CharField(unique=True, max_length=8)

    class Meta:
        managed = False
        db_table = 'rest_framework_api_key_apikey'


class AstromatApiBundleprocesslog(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    source_file = models.CharField()
    log = models.CharField()

    class Meta:
        managed = False
        db_table = 'astromat_api_bundleprocesslog'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Jobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    job_status = models.CharField()
    job_details = models.CharField(blank=True, null=True)
    processing_record = models.ForeignKey('Records', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'jobs'

