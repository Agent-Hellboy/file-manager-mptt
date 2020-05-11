from django.db import models
from django.contrib.auth  import  get_user_model 
from mptt.models import MPTTModel, TreeForeignKey
from file_manager_mptt.utils.node_types import NODE_TYPE, FOLDER, FILE
from file_manager_mptt.exceptions.file_node_exception import FileNodeException
from file_manager_mptt.exceptions.errors import Errors
import uuid
# Create your models here.

## identifiers


class FileMpttModel(MPTTModel):

    id = models.UUIDField(verbose_name="File Node ID", primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, related_name='children', on_delete=models.CASCADE)
    type = models.IntegerField(choices=NODE_TYPE)
    slug = models.SlugField(max_length=100)
    owner = models.ForeignKey(get_user_model(), related_name='volumen', on_delete=models.PROTECT)
    deleted = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


    def is_folder(self):
        return self.type == FOLDER

    def is_file(self):
        return self.type == FILE


    def save(self, *args, **kwargs):

        if self.parent and self.parent.is_file():
            raise FileNodeException(Errors._FILE_CANNOT_HAVE_CHILDREN)

        super(FileMpttModel, self).save(*args, **kwargs) 