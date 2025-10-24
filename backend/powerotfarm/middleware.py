from django.conf import settings


class NoCacheForDevMiddleware:
    """Middleware to disable caching for HTML and static responses during development.

    When DEBUG is True, this sets Cache-Control, Pragma and Expires headers so browsers
    won't cache HTML/static files and you'll see edits immediately without needing
    to run collectstatic or hard-refresh.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not settings.DEBUG:
            return response

        content_type = response.get('Content-Type', '')
        # apply to HTML responses or requests for top-level .html/.js/.css files
        if content_type.startswith('text/html') or request.path.endswith('.html') or request.path.endswith(('.js', '.css')) or request.path.startswith('/static/'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response
