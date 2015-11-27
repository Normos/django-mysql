# -*- coding:utf-8 -*-
from unittest import skipIf

import django
from django.test import TransactionTestCase

from django_mysql.checks import check_variables
from django_mysql.test.utils import override_mysql_variables

requiresNoDBConnection = skipIf(
    django.VERSION[:2] < (1, 8),
    "Requires nodb_connection from Django 1.8+"
)


@requiresNoDBConnection
class VariablesTests(TransactionTestCase):

    def test_passes(self):
        assert check_variables() == []

    @override_mysql_variables(sql_mode="")
    def test_fails_if_no_strict(self):
        errors = check_variables()
        assert len(errors) == 1
        assert errors[0].id == 'django_mysql.W001'
        assert "MySQL Strict Mode" in errors[0].msg

    @override_mysql_variables(innodb_strict_mode=0)
    def test_fails_if_no_innodb_strict(self):
        errors = check_variables()
        assert len(errors) == 1
        assert errors[0].id == 'django_mysql.W002'
        assert "InnoDB Strict Mode" in errors[0].msg

    @override_mysql_variables(character_set_connection='utf8')
    def test_fails_if_not_utf8mb4(self):
        errors = check_variables()
        assert len(errors) == 1
        assert errors[0].id == 'django_mysql.W003'
        assert "utf8mb4" in errors[0].msg