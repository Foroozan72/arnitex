from datetime import datetime
from support.models import Ticket

class GenerateTrackingCode():
    def dictionary(model):
        model_dict = {Ticket: "T"}
        return model_dict[model]

    def generate_tracking_code(model):
        today = datetime.now().strftime("%Y%m%d")
        today_objects_count = model.objects.filter(
            created_at__year=datetime.now().year,
            created_at__month=datetime.now().month,
            created_at__day=datetime.now().day
        ).count() + 1
        return f"{GenerateTrackingCode.dictionary(model)}{today}{today_objects_count:04d}"