from django.urls import path

from views import GetTelegramView, ParsingTelegramView

urlpatterns = [
    path('post-telegram-channel/', ParsingTelegramView.as_view()),  # записать новости из телеграм канала
    path('get-telegram/', GetTelegramView.as_view({'get': 'list'})),  # просмотреть все записи из телеграм
]