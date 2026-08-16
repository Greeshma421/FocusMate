# Import all models so they are registered on Base.metadata for Alembic and SQLAlchemy
from .user import User  # noqa: F401
from .goal import StudyGoal  # noqa: F401
from .topic import Topic  # noqa: F401
from .schedule import Schedule  # noqa: F401
from .study_session import StudySession  # noqa: F401
from .assessment import Assessment  # noqa: F401
from .question import Question  # noqa: F401
from .notification import Notification  # noqa: F401
from .progress import Progress  # noqa: F401
from .chat_history import ChatHistory  # noqa: F401
from .refresh_token import RefreshToken  # noqa: F401
from .assessment_result import AssessmentResult  # noqa: F401
