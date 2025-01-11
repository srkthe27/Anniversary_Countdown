from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["POST"])
def calculate_anniversaries(request):
    try:
        data = json.loads(request.body)
        user_anniversary = data.get("user_anniversary")
        user_proposed_anniversary = data.get("user_proposed_anniversary")

        now = datetime.now()

        # Function to calculate the next anniversary date
        def get_next_date(date_str):
            date_obj = datetime.strptime(date_str, "%m-%d-%Y")
            while date_obj < now:
                date_obj += relativedelta(years=1)
            return date_obj

        # Calculate the next anniversary and proposed anniversary dates
        next_anniversary_date = get_next_date(user_anniversary)
        next_proposed_anniversary_date = get_next_date(user_proposed_anniversary)

        return JsonResponse({
            "server_time": now.strftime("%Y-%m-%d %H:%M:%S"),  # Send server time to sync with the frontend
            "next_anniversary_date": next_anniversary_date.strftime("%Y-%m-%d %H:%M:%S"),
            "next_proposed_anniversary_date": next_proposed_anniversary_date.strftime("%Y-%m-%d %H:%M:%S"),
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
