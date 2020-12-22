import pytest
import brownie
from asserts import assert_true, assert_equal, assert_false
from brownie import Wei


def eth(amount):
    return Wei("{amount} ether".format(amount=amount))


@pytest.fixture
def setup1(module_isolation, vault, lido, user1, user2):
    lido.submit(user1, {"from": user1, "amount": eth(100)})
    lido.approve(vault, eth(50), {"from": user1})
    assert_equal(lido.allowance(user1, vault.address), eth(50))
    yield


class TestWrapUnwrap(object):
    @pytest.mark.usefixtures("setup1", scope="class")
    def test_initial_balances_are_correct(self, lido, vault, user1, user2):
        assert_equal(lido.balanceOf(user1), eth(100))
        assert_equal(vault.balanceOf(user1), eth(0))
        assert_equal(lido.balanceOf(user2), eth(0))
        assert_equal(vault.balanceOf(user2), eth(0))

    # not reverted

    # def test_cant_wrap_zero(self, setup1, vault, user1):
    #     with brownie.reverts('') : vault.deposit(eth(0), {"from": user1})

    def test_wrap_more_than_allowed(self, vault, user1, lido):
        with brownie.reverts(''): vault.deposit(eth(51), {"from": user1})

    # def test_wrap_if_sender_hasnt_stEth(self,setup1, lido,vault, user2):
    #     lido.approve(vault, eth(50), {"from": user2})
    #     with brownie.reverts(''): vault.deposit(eth(1), {"from": user2})


@pytest.fixture
def setup2(module_isolation, vault, lido, user1, user2):
    vault.deposit(eth(50), {"from": user1})
    vault.approve(lido, eth(25), {"from": user1})
    assert_equal(vault.allowance(user1, lido.address), eth(25))
    yield


class TestAfterSuccessfulWrap(object):
    @pytest.mark.usefixtures("setup2", scope="class")
    def test_initial_balances_are_correct(self, setup2, lido, vault, user1, user2):
        assert_equal(lido.balanceOf(user1), eth(50))
        assert_equal(vault.balanceOf(user1), eth(50))
        assert_equal(lido.balanceOf(user2), eth(0))
        assert_equal(lido.balanceOf(vault.address), eth(50))

    # not reverted

    # def test_cant_unwrap_zero(self, setup2, vault, user1):
    #     with brownie.reverts('') : vault.withdraw(eth(0), {"from": user1})
    #
    # def test_unwrap_more_than_allowed(self, setup2, vault, user1):
    #     with brownie.reverts(''): vault.withdraw(eth(51), {"from": user1})

    # def test_cant_wrap_if_hasnt_cstEth(self, setup2, vault, user1,user2):
    #     with brownie.reverts(''): vault.withdraw(eth(1), {"from": user2})

    # def test_wrap_if_sender_hasnt_stEth(self,setup2, lido,vault, user2):
    #     lido.approve(vault, eth(50), {"from": user2})
    #     with brownie.reverts(''): vault.deposit(eth(1), {"from": user2})


@pytest.fixture
def setup3(module_isolation, vault, lido, user1, user2):
    vault.approve(lido, eth(25), {"from": user1})
    assert_equal(vault.allowance(user1, lido.address), eth(25))
    yield


class TestBeforeRewardingSlashing(object):
    @pytest.mark.usefixtures("setup3", scope="class")
    def test_after_partial_unwrap(self, setup3, lido, vault, user1, user2):
        for x in range(6):
            vault.withdraw(eth(10), {"from": user1})
        assert_equal(lido.balanceOf(user1), eth(100))
        assert_equal(lido.balanceOf(vault.address), eth(0))
        assert_equal(vault.balanceOf(user1), eth(0))

    # not reverted

    # def test_cant_unwrap_zero(self, setup3, vault, user1):
    #     with brownie.reverts('') : vault.withdraw(eth(0), {"from": user1})
    #
    # def test_unwrap_more_than_allowed(self, setup3, vault, user1):
    #     with brownie.reverts(''): vault.withdraw(eth(51), {"from": user1})

    # def test_cant_wrap_if_hasnt_cstEth(self, setup3, vault, user1,user2):
    #     with brownie.reverts(''): vault.withdraw(eth(1), {"from": user2})

    # def test_wrap_if_sender_hasnt_stEth(self,setup3, lido,vault, user2):
    #     lido.approve(vault, eth(50), {"from": user2})
    #     with brownie.reverts(''): vault.deposit(eth(1), {"from": user2})
