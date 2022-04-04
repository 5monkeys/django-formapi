try:
    from south.db import db
    from south.v2 import SchemaMigration

except ImportError:
    try:
        from django.db import migrations
    except ImportError:
        raise Exception("South or Django>=1.8 is required")

    class Migration(migrations.Migration):
        dependencies = [("formapi", "0001_initial")]
        operations = []

else:
    pass

    class Migration(SchemaMigration):
        def forwards(self, orm):
            # Adding field 'APIKey.revoked'
            db.add_column(
                "formapi_apikey",
                "revoked",
                self.gf("django.db.models.fields.BooleanField")(default=False),
                keep_default=False,
            )

            # Adding field 'APIKey.test'
            db.add_column(
                "formapi_apikey",
                "test",
                self.gf("django.db.models.fields.BooleanField")(default=False),
                keep_default=False,
            )

        def backwards(self, orm):
            # Deleting field 'APIKey.revoked'
            db.delete_column("formapi_apikey", "revoked")

            # Deleting field 'APIKey.test'
            db.delete_column("formapi_apikey", "test")

        models = {
            "formapi.apikey": {
                "Meta": {"object_name": "APIKey"},
                "comment": (
                    "django.db.models.fields.TextField",
                    [],
                    {"null": "True", "blank": "True"},
                ),
                "created": (
                    "django.db.models.fields.DateTimeField",
                    [],
                    {"auto_now_add": "True", "blank": "True"},
                ),
                "email": (
                    "django.db.models.fields.EmailField",
                    [],
                    {"max_length": "75"},
                ),
                "id": (
                    "django.db.models.fields.AutoField",
                    [],
                    {"primary_key": "True"},
                ),
                "key": (
                    "formapi.fields.UUIDField",
                    [],
                    {"unique": "True", "max_length": "32", "blank": "True"},
                ),
                "revoked": (
                    "django.db.models.fields.BooleanField",
                    [],
                    {"default": "False"},
                ),
                "secret": (
                    "formapi.fields.UUIDField",
                    [],
                    {"unique": "True", "max_length": "32", "blank": "True"},
                ),
                "test": (
                    "django.db.models.fields.BooleanField",
                    [],
                    {"default": "False"},
                ),
            }
        }

        complete_apps = ["formapi"]
