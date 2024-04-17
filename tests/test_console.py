#!/usr/bin/python3
"""Defines unittests for console.py."""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage


class TestHBNBCommand(unittest.TestCase):
    """Unittests for testing the HBNB command interpreter."""

    def setUp(self):
        """Set up test environment."""
        self.console = HBNBCommand()

    def tearDown(self):
        """Remove temporary file (file.json) created as a result."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_help_command(self):
        """Test the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        output = f.getvalue()
        self.assertIn('Documented commands', output)

    def test_create_command(self):
        """Test the create command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        output = f.getvalue()
        self.assertRegex(output, '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')

    def test_show_command(self):
        """Test the show command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            model_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show BaseModel {model_id}")
        output = f.getvalue()
        self.assertIn(model_id, output)

    def test_destroy_command(self):
        """Test the destroy command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            model_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"destroy BaseModel {model_id}")
        output = f.getvalue()
        self.assertEqual(output, "")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show BaseModel {model_id}")
        output = f.getvalue()
        self.assertEqual(output, "** no instance found **\n")

    def test_all_command(self):
        """Test the all command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create User")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
        output = f.getvalue()
        self.assertIn("BaseModel", output)
        self.assertIn("User", output)

    def test_update_command(self):
        """Test the update command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            model_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update BaseModel {model_id} name "My Model"')
        output = f.getvalue()
        self.assertEqual(output, "")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show BaseModel {model_id}")
        output = f.getvalue()
        self.assertIn("name", output)
        self.assertIn("My Model", output)

    def test_count_command(self):
        """Test the count command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create BaseModel")
            HBNBCommand().onecmd("create User")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count BaseModel")
        output = f.getvalue()
        self.assertEqual(output, "2\n")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count User")
        output = f.getvalue()
        self.assertEqual(output, "1\n")
