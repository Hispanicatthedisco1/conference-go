from django.http import JsonResponse
from .models import Attendee
from django.views.decorators.http import require_http_methods
import json

@require_http_methods({"GET", "POST"})
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
    )
    
    else:
        content = json.loads(request.body)
        try:
            conference = conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"messagfe": "Invalid conference id"},
                status=400,
            )
        
        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
            

@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, id):
    if request.method == "GET":
        attendee = attendee.objects.get(id=id)
        return JsonResponse({
            "email": attendee.email,
            "name": attendee.name,
            "company_name": attendee.company_name,
            "created": attendee.created,
            "conference": {
                "name": attendee.conference.name,
                "href": attendee.conference.get_api_url(),
            },
        }
    )

    elif request.method == "DELETE":
        count, = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"delete": count > 0})
    
    else:
        content = json.loads(request.body)
        try:
            if "conference" in content:
                conference = conference.objects.get(abbreviation=content["conference"])
                content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid Conference"}
                status=400,
            )
        Attendee.objects.filter(id=id).update(**content)

        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )