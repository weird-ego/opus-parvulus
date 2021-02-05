from decimal import Decimal

from .models import Account, Transaction
from django.db.transaction import atomic


def perform_deposit(user, amount: Decimal):  # for external typechecks

    # django views are atomic dy default, but it would be nice to ensure this
    # behaviour

    with atomic():
        account = Account.objects.get(user=user)
        account.balance += amount
        account.save()

        transaction = Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TRANSACTION_TYPE_DEPOSIT
        )

        return transaction


def perform_withdrawal(user, amount: Decimal):  # for external typechecks
    with atomic():
        account = Account.object.get(user=user)
        if account.balance < amount:
            raise ValueError('Not enough funds')  # debatable
                                                  # could also return bool
                                                  # marking success/fail
        account.balance -= amount
        account.save()

        transaction = Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TRANSACTION_TYPE_WITHDRAWAL
        )

        return transaction
