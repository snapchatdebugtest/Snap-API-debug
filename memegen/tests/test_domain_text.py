# pylint: disable=no-self-use,misplaced-comparison-constant

from memegen.domain import Text


class TestInit:

    def test_none(self):
        text = Text()

        assert "" == text.top
        assert "" == text.bottom

    def test_0_slashes(self):
        text = Text("foo")

        assert "FOO" == text.top
        assert "" == text.bottom

    def test_1_slash(self):
        text = Text("foo/bar")

        assert "FOO" == text.top
        assert "BAR" == text.bottom
        assert "" == text.get_line(2)

    def test_2_slashes(self):
        text = Text("foo/bar/qux")

        assert "FOO" == text.top
        assert "BAR" == text.bottom
        assert "QUX" == text.get_line(2)
        assert "" == text.get_line(3)


class TestBool:

    def test_content_is_truthy(self):
        assert True is bool(Text("Hello, world!"))

    def test_empty_is_falsey(self):
        assert False is bool(Text())

    def test_only_spaces_is_falsey(self):
        assert False is bool(Text("_/_/_"))


class TestLines:

    def test_split_underscore_as_spaces(self):
        text = Text("hello_world")

        assert ["HELLO WORLD"] == text.lines

    def test_split_dash_as_spaces(self):
        text = Text("hello-world")

        assert ["HELLO WORLD"] == text.lines

    def test_split_case_as_spaces(self):
        text = Text("helloWorld")

        assert ["HELLO WORLD"] == text.lines

    def test_keep_spaces(self):
        text = Text("hello world")

        assert ["HELLO WORLD"] == text.lines

    def test_case_ignored_after_space(self):
        text = Text("HELLO iOS")

        assert ["HELLO IOS"] == text.lines

    def test_ignore_initial_capital(self):
        text = Text("HelloWorld")

        assert ["HELLO WORLD"] == text.lines

    def test_ignore_capital_after_sep(self):
        text = Text("hello-World")

        assert ["HELLO WORLD"] == text.lines

    def test_ignore_capital_after_apostrophe(self):
        text = Text("Y'ALL")

        assert ["Y'ALL"] == text.lines

    def test_strip_spaces(self):
        text = Text("  hello  World /    ")

        assert ["HELLO  WORLD"] == text.lines

    def test_duplicate_capitals_treated_as_spaces(self):
        text = Text("IWantTHISPattern_to-Work")

        assert ["I WANT THIS PATTERN TO WORK"] == text.lines

    def test_no_space_after_apostrophe(self):
        text = Text("that'd be great")

        assert ["THAT'D BE GREAT"] == text.lines

    def test_double_dashes_are_escaped(self):
        text = Text("i'm----  /working 9--5")

        assert ["I'M--", "WORKING 9-5"] == text.lines

    def test_double_underscores_are_escaped(self):
        text = Text("Calls ____init____/with __args")

        assert ["CALLS __INIT__", "WITH _ARGS"] == text.lines

    def test_special_characters_are_kept(self):
        text = Text("special?")

        assert ["SPECIAL?"] == text.lines

    def test_question_marks_are_escaped(self):
        text = Text("special~q~Q")

        assert ["SPECIAL??"] == text.lines

    def test_percents_are_escaped(self):
        text = Text("99~p vs. 1~P")

        assert ["99% VS. 1%"] == text.lines

    def test_quotes_are_escaped(self):
        text = Text("the ''word'' said")

        assert ['THE "WORD" SAID'] == text.lines


class TestPath:

    def test_case_ignored(self):
        text = Text("hello/World")

        assert "hello/world" == text.path

    def test_single_underscores_kept(self):
        text = Text("with_underscores/in_it")

        assert "with_underscores/in_it" == text.path

    def test_dashes_become_underscores(self):
        text = Text("with-dashes/in-it")

        assert "with_dashes/in_it" == text.path

    def test_case_changes_become_underscores(self):
        text = Text("withCaseChanges/InIT")

        assert "with_case_changes/in_it" == text.path

    def test_extra_spaces_are_stripped(self):
        text = Text("  with  spaces/  in it   / ")

        assert "with__spaces/in_it" == text.path

    def test_single_underscore_is_kept(self):
        text = Text(" _     ")

        assert "_" == text.path

    def test_duplicate_capitals_are_ignored(self):
        text = Text("IWantTHISPattern_to-Work")

        assert "i_want_this_pattern_to_work" == text.path

    def test_double_dashes_are_escaped(self):
        text = Text("i'm----  /working 9--5")

        assert "i'm----/working_9--5" == text.path

    def test_double_underscores_are_escaped(self):
        text = Text("Calls ____init____/with args")

        assert "calls_____init____/with_args" == text.path

    def test_question_marks_are_escaped(self):
        text = Text("special?")

        assert "special~q" == text.path

    def test_percents_are_escaped(self):
        text = Text("50% off")

        assert "50~p_off" == text.path

    def test_quotes_are_escaped(self):
        text = Text('"quoted"')

        assert "''quoted''" == text.path

    def test_exact_input_can_be_used(self):
        text = Text("underscore_ dash-", translate_spaces=False)

        assert "underscore___dash--" == text.path
