# Bitstocks coding test

This is a Django coding/knowledge test.  You can run this either in docker, or not.  This test is not about Docker, so if you are not familar, please just setup your environment however you normally would.

Please spend no more than 30 minutes on this test.  Task 4 is optional, only do it if you have time left over.  In all tasks, consider that this is in the context of a financial system, and data integrity and precision is of key importance.

### Docker

The Dockerfile includes running of migrations, and then performing the test suite.  So simply be in the root directory of the project, and run:

```shell
docker build .
```

## Tasks

The project is simple, containing only 1 app with 2 models.  It is a basic implementaion of a system where users can have accounts.  Those accounts can have balances, and we wish to be able to track changes to balances by storing transactions.

There is already a basic deposit service written, allowing for an amount to be added to an Account, and a deposit Transaction created.

### Task 1

The Transaction model is fairly basic, and some important information is missing.  Make sure that whenever a Transaction is created, we store the time it was created.

### Task 2

The accounts app has a tests.py, which has 2 tests, one of which fails.

Why does the test fail?
How can you change the application to fix the test?

### Task 3

The deposit service is quite basic right now, and not much could go wrong.  But what risks are there with the way it's written? Imagine that it's possible for the creation of the Transaction to fail, what would happen in this case? What could you do to improve it?

### Task 4

The perform_withdrawal service is unwritten.  Implement a basic version of this service - no extra models should be required.  What considerations might you need to make for this service, and how might you approach preventing any issues it might raise?
