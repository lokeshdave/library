from django.http import JsonResponse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        public_urls = [
            'api/token/'
        ]

        if any(request.path.startswith(url) for url in public_urls):
            return self.get_response(request)

        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return JsonResponse(
                {"error": "Authentication required"},
                status=401
            )

        return self.get_response(request)