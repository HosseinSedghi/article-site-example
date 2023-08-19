from django.urls import path

from admin_panel import views

urlpatterns = [
    path('', views.AdminHomeView.as_view(), name='admin-home-page'),
    # Article URLs
    path('article-list', views.AdminArticleListView.as_view(), name='admin-article-list-page'),
    path('article-create', views.AdminArticleCreateView.as_view(), name='admin-article-create-page'),
    # Category URLs
    path('category-list', views.AdminCategoryListView.as_view(), name='admin-category-list-page'),
    path('category-create', views.AdminCategoryCreateView.as_view(), name='admin-category-create-page'),
    path('category-edit/<pk>', views.AdminCategoryEditView.as_view(), name='admin-category-edit-page'),
    # Users URLs
    path('user-list', views.AdminUserListView.as_view(), name='admin-user-list-page'),
    path('user-detail/<pk>', views.AdminUserDetailView.as_view(), name='admin-user-detail-page'),
    path('user-change-password/<pk>', views.AdminChangePasswordView.as_view(), name='admin-user-change-password-page'),
    # Comments URLs
    path('comments', views.AdminCommentListView.as_view(), name='admin-comment-page'),
    path('comment-delete', views.delete_comment, name='admin-comment-delete-page'),
    path('convert-comment-to-publish', views.convert_comment_publish),
    path('convert-comment-to-draft', views.convert_comment_draft),
    # Ticket URLs
    path('ticket-list', views.TicketListView.as_view(), name='admin-ticket-list-page'),
    path('delete-ticket', views.delete_ticket),
]
