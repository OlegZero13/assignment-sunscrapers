from django.conf.urls import url

from . import views

app_name = 'pipeline'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^borrower/(?P<member_id>[0-9]+)/$', views.borrower, name='borrower'),
    url(r'^loan/(?P<loan_id>[0-9]+)/$', views.loan, name='loan'),
]
