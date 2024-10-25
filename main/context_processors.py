from joinpartner.models import Partner

def store_owner_status(request):
    is_store_owner = False
    if request.user.is_authenticated:
        is_store_owner = Partner.objects.filter(
            user=request.user,
            status='Approved'
        ).exists()
    return {'is_store_owner': is_store_owner}