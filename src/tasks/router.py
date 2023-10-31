from fastapi import APIRouter, BackgroundTasks, Depends

from src.auth.base_config import current_user
from src.tasks.tasks import send_email_report_dashboard

router = APIRouter(prefix="/report", tags=["Report"])


@router.get("/dashboard")
def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
    # ~1400 ms -На компе ментора - Клиент ждет - если просто выполняем синхронно задачу
    # send_email_report_dashboard(user.username)
    # ~500 ms - Задача выполняется на фоне FastAPI в event loop'е или в другом треде
    # background_tasks.add_task(send_email_report_dashboard, user.username)
    # ~600 ms - Задача выполняется воркером Celery в отдельном процессе (у меня 6сек-why?)
    send_email_report_dashboard.delay(user.username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }
