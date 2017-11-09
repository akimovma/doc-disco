broker_url = 'redis://localhost:6379'
result_backend = 'redis://localhost:6379'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

# for common tasks, not belonging to any app
imports = ('doc_disco.tasks',)

enable_utc = True
