from server import Router
from controllers import get_root, get_health_api
from controllers.tasks import get_tasks, get_task_by_id, add_task, update_task, delete_task

router = Router()

router.get('/', get_root)
router.get('/health', get_health_api)

router.get('/tasks', get_tasks)
router.get('/task', get_task_by_id)
router.post('/task', add_task)
router.patch('/task', update_task)
router.delete('/task', delete_task)
