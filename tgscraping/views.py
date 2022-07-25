import time

from rest_framework import viewsets, generics, permissions

from models import TelegramChatsView
import scraping
from serializers import GetTelegramSerializer, ParsingTelegramSerializer


class ParsingTelegramView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ParsingTelegramSerializer

    def get(self, request):

        start_time = time.time()

        while True:
            data = []
            content = TgChat()
            get_topics = content.get_content(number_of_page=6)

            print('number of articles = ', len(get_topics))

            # i = 1
            for item in get_topics:

                queryset = TelegramChatsView.objects.filter(title=str(item['title']))

                if not queryset:
                    serializer = self.get_serializer(data=item)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    data.append(serializer.data)

            time.sleep(7200.0 - ((time.time() - start_time) % 7200.0))


class GetTelegramView(viewsets.ModelViewSet):
    queryset = TelegramChatsView.objects.all()
    serializer_class = GetTelegramSerializer
    permissions = [permissions.AllowAny]

