# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import contextlib
import unittest
from io import StringIO

from azure.cli.core import get_default_cli
from azure.cli.core.azclierror import InvalidArgumentValueError
from azure.cli.core.aaz import AAZListArg, AAZDictType, AAZStrArg, AAZStrType

from azure.cli.command_modules.changesafety.aaz.latest.change_safety.change_state._create import Create
from azure.cli.command_modules.changesafety.aaz.latest.change_safety.change_state._update import Update


class ChangeSafetySchemaTests(unittest.TestCase):

    def test_create_targets_argument_schema(self):
        schema = Create._build_arguments_schema()
        self.assertTrue(hasattr(schema, "targets"))
        self.assertIsInstance(schema.targets, AAZListArg)
        self.assertIsInstance(schema.targets.Element, AAZStrArg)

    def test_update_targets_argument_schema(self):
        schema = Update._build_arguments_schema()
        self.assertTrue(hasattr(schema, "targets"))
        self.assertIsInstance(schema.targets, AAZListArg)
        self.assertIsInstance(schema.targets.Element, AAZStrArg)

    def test_create_targets_in_response_schema(self):
        response_schema = Create.ChangeStatesCreateOrUpdate._build_schema_on_200_201()
        self.assertTrue(hasattr(response_schema.properties, "targets"))
        self.assertIsInstance(response_schema.properties.targets, AAZDictType)
        self.assertIsInstance(response_schema.properties.targets.Element, AAZStrType)

    def test_parse_targets_format(self):
        result = Create._parse_targets(['key1=value1,key2=value2', 'keyA=valueA;keyB=valueB'])
        self.assertEqual(result, [
            {'key1': 'value1', 'key2': 'value2'},
            {'keyA': 'valueA', 'keyB': 'valueB'}
        ])

    def test_parse_targets_invalid_raises(self):
        with self.assertRaises(InvalidArgumentValueError):
            Create._parse_targets(['invalid'])

    def test_update_targets_in_response_schema(self):
        response_schema = Update.ChangeStatesCreateOrUpdate._build_schema_on_200_201()
        self.assertTrue(hasattr(response_schema.properties, "targets"))
        self.assertIsInstance(response_schema.properties.targets, AAZDictType)
        self.assertIsInstance(response_schema.properties.targets.Element, AAZStrType)


class ChangeSafetyHelpTests(unittest.TestCase):

    def _invoke_help(self, command):
        cli = get_default_cli()
        stdout = StringIO()
        stderr = StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as cm:
                cli.invoke(command)
        self.assertEqual(cm.exception.code, 0)
        return stdout.getvalue() + stderr.getvalue()

    def test_create_help_mentions_targets(self):
        output = self._invoke_help(['change-safety', 'change-state', 'create', '--help'])
        self.assertIn('--targets', output)

    def test_update_help_mentions_targets(self):
        output = self._invoke_help(['change-safety', 'change-state', 'update', '--help'])
        self.assertIn('--targets', output)
