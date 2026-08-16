"""update constraints and add indexes
Revision ID: 0002_update_constraints_and_indexes
Revises: 0001_initial_create_tables
Create Date: 2026-08-16
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002_update_constraints_and_indexes'
down_revision = '0001_initial_create_tables'
branch_labels = None
depends_on = None


def upgrade():
    # Add foreign key constraints to enforce referential integrity
    op.create_foreign_key('fk_study_goals_user', 'study_goals', 'users', ['user_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_topics_user', 'topics', 'users', ['user_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_topics_parent', 'topics', 'topics', ['parent_topic_id'], ['id'], ondelete='SET NULL')

    op.create_foreign_key('fk_schedules_user', 'schedules', 'users', ['user_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_schedules_goal', 'schedules', 'study_goals', ['goal_id'], ['id'], ondelete='SET NULL')

    op.create_foreign_key('fk_sessions_schedule', 'study_sessions', 'schedules', ['schedule_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_sessions_user', 'study_sessions', 'users', ['user_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_sessions_topic', 'study_sessions', 'topics', ['topic_id'], ['id'], ondelete='SET NULL')

    op.create_foreign_key('fk_notifications_user', 'notifications', 'users', ['user_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_notifications_session', 'notifications', 'study_sessions', ['session_id'], ['id'], ondelete='CASCADE')

    op.create_foreign_key('fk_assessments_user', 'assessments', 'users', ['user_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_assessments_topic', 'assessments', 'topics', ['topic_id'], ['id'], ondelete='SET NULL')

    op.create_foreign_key('fk_questions_assessment', 'questions', 'assessments', ['assessment_id'], ['id'], ondelete='CASCADE')

    op.create_foreign_key('fk_assessment_results_assessment', 'assessment_results', 'assessments', ['assessment_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('fk_assessment_results_user', 'assessment_results', 'users', ['user_id'], ['id'], ondelete='RESTRICT')

    op.create_foreign_key('fk_progress_user', 'progress', 'users', ['user_id'], ['id'], ondelete='RESTRICT')
    op.create_foreign_key('fk_progress_topic', 'progress', 'topics', ['topic_id'], ['id'], ondelete='SET NULL')

    op.create_foreign_key('fk_chat_history_user', 'chat_history', 'users', ['user_id'], ['id'], ondelete='RESTRICT')

    op.create_foreign_key('fk_refresh_tokens_user', 'refresh_tokens', 'users', ['user_id'], ['id'], ondelete='RESTRICT')

    # Convert text JSON/text columns to JSONB where appropriate
    try:
        op.alter_column('assessments', 'metadata', type_=postgresql.JSONB, postgresql_using="metadata::jsonb")
    except Exception:
        # If conversion fails (e.g., empty data), fallback to simple type alter
        op.alter_column('assessments', 'metadata', type_=postgresql.JSONB)

    try:
        op.alter_column('questions', 'choices', type_=postgresql.JSONB, postgresql_using='choices::jsonb')
        op.alter_column('questions', 'correct_answer', type_=postgresql.JSONB, postgresql_using='correct_answer::jsonb')
        op.alter_column('questions', 'metadata', type_=postgresql.JSONB, postgresql_using='metadata::jsonb')
    except Exception:
        op.alter_column('questions', 'choices', type_=postgresql.JSONB)
        op.alter_column('questions', 'correct_answer', type_=postgresql.JSONB)
        op.alter_column('questions', 'metadata', type_=postgresql.JSONB)

    try:
        op.alter_column('assessment_results', 'answers', type_=postgresql.JSONB, postgresql_using='answers::jsonb')
    except Exception:
        op.alter_column('assessment_results', 'answers', type_=postgresql.JSONB)

    try:
        op.alter_column('chat_history', 'metadata', type_=postgresql.JSONB, postgresql_using='metadata::jsonb')
    except Exception:
        op.alter_column('chat_history', 'metadata', type_=postgresql.JSONB)

    # Add missing max_score column to assessment_results
    with op.batch_alter_table('assessment_results') as batch_op:
        batch_op.add_column(sa.Column('max_score', sa.Numeric(), nullable=False, server_default='0'))

    # Create indexes for efficient scheduling/notification queries
    op.create_index('ix_study_sessions_start_at', 'study_sessions', ['start_at'])
    op.create_index('ix_notifications_scheduled_at', 'notifications', ['scheduled_at'])
    op.create_index('ix_study_sessions_user_start', 'study_sessions', ['user_id', 'start_at'])


def downgrade():
    # Drop indexes
    op.drop_index('ix_study_sessions_user_start', table_name='study_sessions')
    op.drop_index('ix_notifications_scheduled_at', table_name='notifications')
    op.drop_index('ix_study_sessions_start_at', table_name='study_sessions')

    # Remove max_score
    with op.batch_alter_table('assessment_results') as batch_op:
        batch_op.drop_column('max_score')

    # Revert JSONB conversions back to JSON/Text when possible
    try:
        op.alter_column('chat_history', 'metadata', type_=postgresql.JSON, postgresql_using='metadata::json')
    except Exception:
        pass
    try:
        op.alter_column('assessment_results', 'answers', type_=postgresql.JSON, postgresql_using='answers::json')
    except Exception:
        pass
    try:
        op.alter_column('questions', 'choices', type_=postgresql.JSON, postgresql_using='choices::json')
        op.alter_column('questions', 'correct_answer', type_=postgresql.JSON, postgresql_using='correct_answer::json')
        op.alter_column('questions', 'metadata', type_=postgresql.JSON, postgresql_using='metadata::json')
    except Exception:
        pass
    try:
        op.alter_column('assessments', 'metadata', type_=sa.Text, postgresql_using='metadata::text')
    except Exception:
        pass

    # Drop foreign keys (names used above)
    op.drop_constraint('fk_refresh_tokens_user', 'refresh_tokens', type_='foreignkey')
    op.drop_constraint('fk_chat_history_user', 'chat_history', type_='foreignkey')
    op.drop_constraint('fk_progress_topic', 'progress', type_='foreignkey')
    op.drop_constraint('fk_progress_user', 'progress', type_='foreignkey')
    op.drop_constraint('fk_assessment_results_user', 'assessment_results', type_='foreignkey')
    op.drop_constraint('fk_assessment_results_assessment', 'assessment_results', type_='foreignkey')
    op.drop_constraint('fk_questions_assessment', 'questions', type_='foreignkey')
    op.drop_constraint('fk_assessments_topic', 'assessments', type_='foreignkey')
    op.drop_constraint('fk_assessments_user', 'assessments', type_='foreignkey')
    op.drop_constraint('fk_notifications_session', 'notifications', type_='foreignkey')
    op.drop_constraint('fk_notifications_user', 'notifications', type_='foreignkey')
    op.drop_constraint('fk_sessions_topic', 'study_sessions', type_='foreignkey')
    op.drop_constraint('fk_sessions_user', 'study_sessions', type_='foreignkey')
    op.drop_constraint('fk_sessions_schedule', 'study_sessions', type_='foreignkey')
    op.drop_constraint('fk_schedules_goal', 'schedules', type_='foreignkey')
    op.drop_constraint('fk_schedules_user', 'schedules', type_='foreignkey')
    op.drop_constraint('fk_topics_parent', 'topics', type_='foreignkey')
    op.drop_constraint('fk_topics_user', 'topics', type_='foreignkey')
    op.drop_constraint('fk_study_goals_user', 'study_goals', type_='foreignkey')

    # Note: This downgrade won't restore data conversions perfectly; review manually if needed.
