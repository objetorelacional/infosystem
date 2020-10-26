from typing import Dict

from infosystem.common import utils
from infosystem.common.subsystem import Subsystem
from infosystem.subsystem.application.resource import Application


class BootstrapApplication(object):

    def __init__(self, subsystems: Dict[str, Subsystem]):
        self.application_manager = subsystems['applications'].manager

    def execute(self) -> Application:
        application = self._get_application_default()
        return self._save_application(application)

    def _get_application_default(self) -> Application:
        return Application(id=utils.random_uuid(),
                           name=Application.DEFAULT,
                           description="Application Default")

    def _save_application(self, application: Application) -> Application:
        return self.application_manager.create(**application.to_dict())
