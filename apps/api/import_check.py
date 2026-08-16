import sys
import traceback
print('Python', sys.version)
modules = [
    'app.models.user',
    'app.models.study_session',
    'app.models.notification',
    'app.models.assessment',
    'app.models.question',
    'app.models.assessment_result',
    'app.models.progress',
    'app.models.chat_history',
    'app.models.refresh_token',
    'app.repositories.session_repo',
    'app.repositories.notification_repo',
    'app.repositories.schedule_repo',
    'app.services.sessions_service',
    'app.api.deps',
    'app.api.v1.routers.sessions',
    'app.api.v1.routers.auth',
]

for m in modules:
    try:
        __import__(m)
        print(f"{m}: OK")
    except Exception:
        print(f"{m}: ERROR")
        traceback.print_exc()
