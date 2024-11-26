from src.shared.domain.notification import Notification


class TestNotification:
    def test_add_error(self):
        notification = Notification()
        notification.add_error("Error 1")
        assert notification.has_errors
        assert notification.messages == "Error 1"
        assert str(notification) == "Error 1"

    def test_add_errors(self):
        notification = Notification()
        notification.add_errors(["Error 1", "Error 2"])
        assert notification.has_errors
        assert notification.messages == "Error 1,Error 2"
        assert str(notification) == "Error 1,Error 2"

    def test_no_errors(self):
        notification = Notification()
        assert not notification.has_errors
        assert notification.messages == ""
        assert str(notification) == ""

    def test_mixed_errors(self):
        notification = Notification()
        notification.add_error("Error 1")
        notification.add_errors(["Error 2", "Error 3"])
        assert notification.has_errors
        assert notification.messages == "Error 1,Error 2,Error 3"
        assert str(notification) == "Error 1,Error 2,Error 3"
