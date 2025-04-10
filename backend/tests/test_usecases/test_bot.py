import sys

sys.path.insert(0, ".")
import unittest

from app.repositories.common import RecordNotFoundError
from app.repositories.custom_bot import (
    alias_exists,
    delete_alias_by_id,
    delete_bot_by_id,
    find_bot_by_id,
    store_bot,
    update_bot_shared_status,
)
from app.routes.schemas.admin import (
    PushBotInput,
    PushBotInputPinned,
    PushBotInputUnpinned,
)
from app.routes.schemas.bot import (
    AllVisibilityInput,
    PartialVisibilityInput,
    PrivateVisibilityInput,
)
from app.usecases.bot import (
    fetch_all_bots,
    fetch_all_pinned_bots,
    fetch_bot,
    fetch_bot_summary,
    issue_presigned_url,
    modify_bot_visibility,
    modify_pinning_status,
    modify_star_status,
    remove_bot_by_id,
)
from tests.test_repositories.utils.bot_factory import (
    create_test_partial_shared_bot,
    create_test_pinned_partial_share_bot,
    create_test_pinned_public_bot,
    create_test_private_bot,
    create_test_public_bot,
)
from tests.test_usecases.utils.user_factory import (
    create_test_admin_user,
    create_test_user,
    delete_cognito_user,
    store_user_in_cognito,
)


class TestIssuePresignedUrl(unittest.TestCase):
    def test_issue_presigned_url(self):
        user = create_test_user("test_user")
        url = issue_presigned_url(
            user, "test_bot", "test_file", content_type="image/png"
        )
        self.assertEqual(type(url), str)
        self.assertTrue(url.startswith("https://"))


class TestModifyBotVisibility(unittest.TestCase):
    user = create_test_user("user1")

    def setUp(self) -> None:
        self.bot = create_test_private_bot(
            id="1", is_starred=False, owner_user_id="user1"
        )
        store_bot(self.bot)

    def tearDown(self) -> None:
        delete_bot_by_id("user1", "1")

    def test_modify_visibility_to_private(self):
        input_data = PrivateVisibilityInput(target_shared_scope="private")

        modify_bot_visibility(self.user, "1", input_data)
        updated_bot = find_bot_by_id("1")

        self.assertEqual(updated_bot.shared_scope, "private")
        self.assertEqual(updated_bot.shared_status, "unshared")
        self.assertEqual(updated_bot.allowed_cognito_users, [])
        self.assertEqual(updated_bot.allowed_cognito_groups, [])

    def test_modify_visibility_to_partial(self):
        input_data = PartialVisibilityInput(
            target_shared_scope="partial",
            target_allowed_user_ids=["user2", "user3"],
            target_allowed_group_ids=["group1"],
        )

        modify_bot_visibility(self.user, "1", input_data)
        updated_bot = find_bot_by_id("1")

        self.assertEqual(updated_bot.shared_scope, "partial")
        self.assertEqual(updated_bot.shared_status, "shared")
        self.assertEqual(updated_bot.allowed_cognito_users, ["user2", "user3"])
        self.assertEqual(updated_bot.allowed_cognito_groups, ["group1"])

    def test_modify_visibility_to_all(self):
        input_data = AllVisibilityInput(target_shared_scope="all")

        modify_bot_visibility(self.user, "1", input_data)
        updated_bot = find_bot_by_id("1")

        self.assertEqual(updated_bot.shared_scope, "all")
        self.assertEqual(updated_bot.shared_status, "shared")
        self.assertEqual(updated_bot.allowed_cognito_users, [])
        self.assertEqual(updated_bot.allowed_cognito_groups, [])

    def test_modify_visibility_permission_denied(self):
        input_data = PrivateVisibilityInput(target_shared_scope="private")
        user = create_test_user("user2")

        with self.assertRaises(PermissionError) as context:
            modify_bot_visibility(user, "1", input_data)

    def test_cannot_modify_visibility_to_pinned_without_permission(self):
        input_data = AllVisibilityInput(target_shared_scope="all")
        user = create_test_user("user2")

        with self.assertRaises(PermissionError) as context:
            modify_bot_visibility(user, "1", input_data)

    def test_can_modify_visibility_by_admin(self):
        input_data = AllVisibilityInput(target_shared_scope="all")
        user = create_test_admin_user("admin")

        modify_bot_visibility(user, "1", input_data)
        updated_bot = find_bot_by_id("1")

        self.assertEqual(updated_bot.shared_scope, "all")
        self.assertEqual(updated_bot.shared_status, "shared")
        self.assertEqual(updated_bot.allowed_cognito_users, [])
        self.assertEqual(updated_bot.allowed_cognito_groups, [])


class TestModifyPinnedBotVisibilityNarrowing(unittest.TestCase):
    user = create_test_user("user1")

    def setUp(self) -> None:
        self.partial_bot = create_test_pinned_partial_share_bot(
            id="1", is_starred=False, owner_user_id="user1"
        )
        self.public_bot = create_test_pinned_public_bot(
            id="2", is_starred=False, owner_user_id="user1"
        )
        store_bot(self.partial_bot)
        store_bot(self.public_bot)

    def tearDown(self) -> None:
        delete_bot_by_id("user1", "1")
        delete_bot_by_id("user1", "2")

    def test_modify_visibility_pinned_bot_scope_narrowing_to_private(self):
        input_data = PrivateVisibilityInput(target_shared_scope="private")

        with self.assertRaises(ValueError) as context:
            modify_bot_visibility(self.user, "1", input_data)

        with self.assertRaises(ValueError) as context:
            modify_bot_visibility(self.user, "2", input_data)

    def test_modify_visibility_pinned_bot_scope_narrowing_to_partial(self):
        input_data = PartialVisibilityInput(
            target_shared_scope="partial",
            target_allowed_user_ids=["user2", "user3"],
            target_allowed_group_ids=["group1"],
        )

        with self.assertRaises(ValueError) as context:
            modify_bot_visibility(self.user, "2", input_data)


class TestModifyPinningStatus(unittest.TestCase):
    def setUp(self) -> None:
        self.public_bot = create_test_public_bot(
            id="1", is_starred=False, owner_user_id="user1"
        )
        store_bot(self.public_bot)

        self.private_bot = create_test_private_bot(
            id="2", is_starred=False, owner_user_id="user1"
        )
        store_bot(self.private_bot)

    def tearDown(self) -> None:
        delete_bot_by_id("user1", "1")
        delete_bot_by_id("user1", "2")

    def test_pinning_status_pinned(self):
        input_data = PushBotInputPinned(to_pinned=True, order=1)
        modify_pinning_status("1", input_data)

        updated_bot = find_bot_by_id("1")
        self.assertEqual(updated_bot.shared_status, "pinned@001")

    def test_pinning_status_unpinned(self):
        input_data = PushBotInputPinned(to_pinned=True, order=1)
        modify_pinning_status("1", input_data)

        input_unpin = PushBotInputUnpinned(to_pinned=False)
        modify_pinning_status("1", input_unpin)

        updated_bot = find_bot_by_id("1")
        self.assertEqual(updated_bot.shared_status, "shared")

    def test_pinning_status_private_bot(self):
        input_data = PushBotInputPinned(to_pinned=True, order=1)

        with self.assertRaises(ValueError) as context:
            modify_pinning_status("2", input_data)

    def test_unpinning_status_private_bot(self):
        input_data = PushBotInputUnpinned(to_pinned=False)

        with self.assertRaises(ValueError) as context:
            modify_pinning_status("2", input_data)


class TestScenario(unittest.TestCase):
    user1 = create_test_user("user1")
    user2 = create_test_user("user2")
    admin = create_test_admin_user("admin")

    @classmethod
    def setUpClass(cls) -> None:
        store_user_in_cognito(cls.user1)
        store_user_in_cognito(cls.user2)
        store_user_in_cognito(cls.admin)

    @classmethod
    def tearDownClass(cls) -> None:
        delete_cognito_user(cls.user1)
        delete_cognito_user(cls.user2)
        delete_cognito_user(cls.admin)

    def setUp(self) -> None:
        # Create user1 bots. Both are private
        self.user1_bot1 = create_test_private_bot("1", False, "user1")
        self.user1_bot2 = create_test_private_bot("2", False, "user1")

        # Create user2 partial shared bots
        # bot3 is not shared to user1
        self.user2_bot1 = create_test_partial_shared_bot(
            "3", False, "user2", ["user10"]
        )
        # bot4 is shared to user1
        self.user2_bot2 = create_test_partial_shared_bot("4", False, "user2", ["user1"])

        store_bot(self.user1_bot1)
        store_bot(self.user1_bot2)
        store_bot(self.user2_bot1)
        store_bot(self.user2_bot2)

    def tearDown(self) -> None:
        delete_bot_by_id("user1", "1")
        delete_bot_by_id("user1", "2")
        delete_bot_by_id("user2", "4")

        try:
            delete_bot_by_id("user2", "3")
        except RecordNotFoundError:
            pass

        try:
            delete_alias_by_id("user1", "3")
        except Exception:
            print("Alias not found")
            pass

        try:
            delete_alias_by_id("user1", "4")
        except Exception:
            print("Alias not found")
            pass

    def test_scenario1(self):
        # Step 1: Try to fetch user2's bot (should fail)
        with self.assertRaises(PermissionError):
            fetch_bot_summary(self.user1, "3")

        # Step 2: Change user2's bot3 visibility to partial
        input_data = PartialVisibilityInput(
            target_shared_scope="partial",
            target_allowed_user_ids=["user1"],
            target_allowed_group_ids=[],
        )
        modify_bot_visibility(self.user2, "3", input_data)

        # Step 3: user1 fetches user2's bot3 (should succeed)
        # Alias is created at this point
        summary = fetch_bot_summary(self.user1, "3")
        self.assertEqual(summary.id, "3")

        # Step 4: user1 fetches user2's bot4 (should succeed)
        user1_private_bots = fetch_all_bots(self.user1, kind="private", limit=10)
        self.assertEqual(len(user1_private_bots), 2)

        # Step 5: fetch_all_bots as mixed (should include alias for user2's bot3)
        user1_mixed_bots = fetch_all_bots(self.user1, kind="mixed", limit=10)
        self.assertEqual(
            len(user1_mixed_bots), 3
        )  # 2 private + 1 alias. Note that bot4's alias is not created yet

        # Step 6: fetch_all_pinned_bots (should not include user2's bot3)
        pinned_bots = fetch_all_pinned_bots(self.user1)
        self.assertNotIn("3", [bot.id for bot in pinned_bots])

        # Step 7: user1 star user2's bot3 and bot4
        modify_star_status(self.user1, "1", True)
        bot1_summary = fetch_bot_summary(self.user1, "1")
        self.assertTrue(bot1_summary.is_starred)
        modify_star_status(self.user1, "3", True)

        bot3_summary = fetch_bot_summary(self.user1, "3")
        self.assertTrue(bot3_summary.is_starred)
        starred_bots = fetch_all_bots(self.user1, starred=True, kind="mixed")
        self.assertEqual(len(starred_bots), 2)

        # Step 8: Admin pins user2's bot3
        modify_bot_visibility(
            self.admin,
            "3",
            AllVisibilityInput(target_shared_scope="all"),
        )
        modify_pinning_status("3", PushBotInputPinned(to_pinned=True, order=1))

        # Step 9: fetch_all_pinned_bots (should include user2's bot3)
        pinned_bots = fetch_all_pinned_bots(self.user1)
        self.assertIn("3", [bot.id for bot in pinned_bots])

        # Step 10: user1 fetches mixed bots after pinning
        mixed_bots_after_pin = fetch_all_bots(self.user1, kind="mixed", limit=10)
        self.assertEqual(len(mixed_bots_after_pin), 3)

        # Step 11: modifies user2's bot4 visibility to private
        summary = fetch_bot_summary(self.user1, "4")
        self.assertEqual(summary.id, "4")
        bots = fetch_all_bots(self.user1, kind="mixed", limit=10)
        self.assertEqual(len(bots), 4)

        modify_bot_visibility(
            self.user2,
            "4",
            PrivateVisibilityInput(target_shared_scope="private"),
        )

        # Step 12: user1 fetches user2's bot4 (should fail)
        with self.assertRaises(PermissionError):
            fetch_bot(self.user1, "4")

        # Step 13: fetch_all_bots as mixed
        user1_mixed_bots = fetch_all_bots(self.user1, kind="mixed", limit=10)
        for bot_meta in user1_mixed_bots:
            if bot_meta.id == "4":
                self.assertFalse(bot_meta.available)  # bot4 is not available

        # Step 14: try to remove bot3
        with self.assertRaises(ValueError):
            remove_bot_by_id(self.user1, "3")

        # Step 15: Unpin bot3
        modify_pinning_status("3", PushBotInputUnpinned(to_pinned=False))

        # Step 16: remove bot3 by admin
        remove_bot_by_id(self.admin, "3")

        # Step 17: fetch_all_pinned_bots (should be empty)
        pinned_bots = fetch_all_pinned_bots(self.user1)
        self.assertNotIn("3", [bot.id for bot in pinned_bots])

        # Step 18: Try access bot3 by user1
        with self.assertRaises(RecordNotFoundError):
            fetch_bot(self.user1, "3")

        # Step 19: fetch_all_bots as mixed
        user1_mixed_bots = fetch_all_bots(self.user1, kind="mixed", limit=10)
        for bot_meta in user1_mixed_bots:
            if bot_meta.id == "3":
                self.assertFalse(bot_meta.available)


class TestSharing(unittest.TestCase):
    def setUp(self) -> None:
        self.publisher = create_test_user("test_user_pub")
        self.subscriber = create_test_user("test_user_sub")

        self.bot = create_test_public_bot("test_bot", True, self.publisher.id)
        store_bot(self.bot)

    def tearDown(self) -> None:
        delete_bot_by_id(self.publisher.id, self.bot.id)
        try:
            delete_alias_by_id(self.subscriber.id, self.bot.id)
        except:
            print("Alias not found")

    def test_share_and_subscribe(self):
        # Subscribe (equal to open shared URL on browser)
        bot_summary = fetch_bot_summary(self.subscriber, self.bot.id)
        self.assertEqual(bot_summary.id, self.bot.id)

        # Assert that alias successfully created
        self.assertTrue(alias_exists(self.subscriber.id, self.bot.id))


if __name__ == "__main__":
    unittest.main()
