"""Written by - Rafal Kowalski"""
from ..models.version import Version
from ..models import db


class VersionUpdater(object):
    def __init__(self, is_created, event_id, column_to_increment):
        self.is_created = is_created
        self.column_to_increment = column_to_increment
        self.event_id = event_id

    def update(self):
        if self.is_created:
            version = Version(event_id=self.event_id)
            db.session.add(version)
            db.session.commit()
        else:
            previous_version = Version.query.filter_by(event_id=self.event_id).order_by(Version.id.desc()).first()
            if not previous_version:
                version = Version(event_id=self.event_id)
                db.session.add(version)
                db.session.commit()
            self._create_new_version(previous_version)

    def _create_new_version(self, previous_version):
        previous_version_dict = self._previous_version_to_dict(previous_version)
        previous_version_dict[self.column_to_increment] += 1
        new_version = Version(event_id=previous_version_dict["event_id"],
                              event_ver=previous_version_dict["event_ver"],
                              session_ver=previous_version_dict["session_ver"],
                              speakers_ver=previous_version_dict["speakers_ver"],
                              tracks_ver=previous_version_dict["tracks_ver"],
                              sponsors_ver=previous_version_dict["sponsors_ver"],
                              microlocations_ver=previous_version_dict["microlocations_ver"])
        db.session.add(new_version)
        db.session.commit()

    def _previous_version_to_dict(self, previous_version):
        return {"event_id": self.event_id,
                "event_ver": previous_version.event_ver,
                "session_ver": previous_version.session_ver,
                "speakers_ver": previous_version.speakers_ver,
                "tracks_ver": previous_version.tracks_ver,
                "sponsors_ver":previous_version.sponsors_ver,
                "microlocations_ver": previous_version.microlocations_ver}
