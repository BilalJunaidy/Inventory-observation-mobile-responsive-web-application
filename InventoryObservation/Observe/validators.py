import os 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# The following validation function is only to help validate that the extension of the uploaded file is within our allowed extensions.
# However, as research suggests, file extensions can be easily changed and this validation function should not be used to validate the file type.
# In the next iteration of this project, I need to look into ensuring that the file type is also valid.
# Check the following links to see how this can be implemented:
# 1. https://stackoverflow.com/questions/20272579/django-validate-file-type-of-uploaded-file
# 2. https://medium.com/@literallywords/server-side-file-extension-validation-in-django-2-1-b8c8bc3245a0

def validate_file_extension(value):
    ext = (value.name).split('.')[-1]
    allowed_extensions = ['xlsx', 'xlsm', 'csv', 'xls']
    if not ext.lower() in allowed_extensions:
        raise ValidationError(
            _(f'You have uploaded a {ext}, which is not an allowed file type for the Inventory listing. Please upload the uploaded inventory listing that has either one of the extensions (xlsx, xlsm or csv).')
        ) 
    