from django.contrib import admin
from .models import Container,DockerHost,ContainerIp


# Register your models here.
#class UserAdmin(admin.ModelAdmin):
    #list_display = ('username', 'password', 'email')
#    list_display = ('username', 'email')
#class DockerAdmin(admin.ModelAdmin):
#    list_display = ('name', 'user', 'describe')
class ContainerAdmin(admin.ModelAdmin):
    list_display = ('username','containerid','containername','dockerhost','imagename','containerhost','password')
class DockerHostAdmin(admin.ModelAdmin):
    list_display = ('ip','hostpassword')
class ContainerIPAdmin(admin.ModelAdmin):
    list_display = ('ip','used')

#admin.site.register(User,UserAdmin)
#admin.site.register(Docker, DockerAdmin)
admin.site.register(Container,ContainerAdmin)
admin.site.register(DockerHost,DockerHostAdmin)
admin.site.register(ContainerIp,ContainerIPAdmin)