from django.contrib import admin
from .models import Container,DockerHost,ContainerIp,ImageName,Project,UserProfile


# Register your models here.
#class UserAdmin(admin.ModelAdmin):
    #list_display = ('username', 'password', 'email')
#    list_display = ('username', 'email')
#class DockerAdmin(admin.ModelAdmin):
#    list_display = ('name', 'user', 'describe')
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('username','containerid','containername','dockerhost','imagename','containerhost','password','bz')
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
#admin.site.register(User,UserAdmin)
#admin.site.register(Docker, DockerAdmin)
admin.site.register(Container,ContainerAdmin)
admin.site.register(DockerHost,DockerHostAdmin)
admin.site.register(ContainerIp,ContainerIPAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(ImageName,ImageNameAdmin)
admin.site.register(UserProfile,UserProfileAdmin)