import flask

from infosystem.common import exception
from infosystem.common.exception import BadRequest
from infosystem.subsystem.file import controller
from infosystem.subsystem.image.resource import QualityImage


class Controller(controller.Controller):

    @classmethod
    def get_bad_request(cls, cause=None):
        bad_request = BadRequest()
        bad_request.message = cause if not None else bad_request.message

        return flask.Response(response=bad_request.message,
                              status=bad_request.status)

    def get(self, id, **kwargs):
        try:
            quality = flask.request.args.get('quality', None)
            kwargs['quality'] = \
                QualityImage[quality] if quality else QualityImage.min
            folder, filename = self.manager.get(id=id, **kwargs)
            return flask.send_from_directory(folder, filename)
        except KeyError:
            return self.get_bad_request('Unknown Quality')
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)
