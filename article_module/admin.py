from django.contrib import admin

from article_module.models import Article, ArticleCategory, ArticleComments, ArticleView


# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status']
    list_editable = ['status']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'is_active']
    list_editable = ['is_active']


class ArticleCommentsAdmin(admin.ModelAdmin):
    list_display = ['author', 'is_publish', 'replay', 'article']
    list_editable = ['is_publish']


class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ['ip', 'user', 'article']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(ArticleComments, ArticleCommentsAdmin)
admin.site.register(ArticleView, ArticleViewAdmin)
