from django.contrib import admin
from .models import Container,DockerHost,ContainerIp,ImageName,Project,UserProfile,CpuInfo,Format


# Register your models here.
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('username','containerid','containername','dockerhost','imagename','containerhost','password','cpunumber','bz')
class DockerHostAdmin(admin.ModelAdmin):
    list_display = ('ip',)
class ContainerIPAdmin(admin.ModelAdmin):
    list_display = ('ip','used')
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('username','departmentname',)
class ImageNameAdmin(admin.ModelAdmin):
    list_display = ('username','imagename','bz','departmentname')
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name','departmentname')
class CpuInfoAdmin(admin.ModelAdmin):
    list_display = ('ip','cpunumber','used')
class FormatAdmin(admin.ModelAdmin):
    list_display = ('ip','cpunuclear','cnumber','usedcpu','ifexit')
#admin.site.register(User,UserAdmin)
#admin.site.register(Docker, DockerAdmin)
admin.site.register(Container,ContainerAdmin)
admin.site.register(DockerHost,DockerHostAdmin)
admin.site.register(ContainerIp,ContainerIPAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(ImageName,ImageNameAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(CpuInfo,CpuInfoAdmin)
admin.site.register(Format,FormatAdmin)