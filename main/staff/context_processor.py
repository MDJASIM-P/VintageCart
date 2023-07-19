from django.contrib.auth.models import User
from sellers.models import ClothModel, FeedbackModel, MessageModel, Report
def fun(request):
        users = User.objects.all()
        pros = ClothModel.objects.all()
        msgs = MessageModel.objects.all()
        feeds = FeedbackModel.objects.all()
        reports = Report.objects.all()
        return {"users":users, "pros":pros, "msgs":msgs, "feeds":feeds, "reports":reports}