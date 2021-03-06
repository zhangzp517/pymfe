"""Test module for MFE class errors and warnings."""
import pytest

from pymfe.mfe import MFE
from pymfe import _internal
from tests.utils import load_xy

GNAME = "errors-warnings"


class TestErrorsWarnings:
    """TestClass dedicated to test General metafeatures."""
    def test_error_empty_data_1(self):
        with pytest.raises(TypeError):
            MFE().fit(X=None, y=None)

    def test_error_empty_data_2(self):
        with pytest.raises(TypeError):
            X, y = load_xy(0)
            model = MFE().fit(X=X.values, y=y.values)
            model.X = None
            model.extract()

    def test_error_empty_data_3(self):
        with pytest.raises(ValueError):
            MFE().fit(X=[], y=[])

    def test_error_empty_data_4(self):
        with pytest.raises(TypeError):
            X, y = load_xy(0)
            model = MFE().fit(X=X.values, y=y.values)
            model.y = None
            model.extract()

    def test_error_data_wrong_shape(self):
        with pytest.raises(ValueError):
            X, y = load_xy(0)
            MFE().fit(X=X.values, y=y.values[:-1])

    @pytest.mark.parametrize(
        "group_name",
        [
            "land-marking",
            "infotheo",
            "generalgeneral",
            "generalstatistical",
            ("general", "statistical", "invalid"),
            ("invalid", ),
            0,
            None,
            [],
            set(),
            tuple(),
        ])
    def test_error_invalid_groups_1(self, group_name):
        with pytest.raises(ValueError):
            MFE(groups=group_name)

    @pytest.mark.parametrize(
        "group_name",
        [
            1,
            lambda x: x,
            range(1, 5),
        ])
    def test_error_invalid_groups_2(self, group_name):
        with pytest.raises(TypeError):
            MFE(groups=group_name)

    def test_error_random_state(self):
        with pytest.raises(ValueError):
            MFE(random_state=1.5)

    def test_error_folds(self):
        with pytest.raises(ValueError):
            MFE(folds=1.5)

    def test_error_cat_cols_1(self):
        with pytest.raises(ValueError):
            X, y = load_xy(0)
            MFE().fit(X=X.values, y=y.values, cat_cols=1)

    def test_error_cat_cols_2(self):
        with pytest.raises(ValueError):
            X, y = load_xy(0)
            MFE().fit(X=X.values, y=y.values, cat_cols="all")

    def test_error_invalid_timeopt(self):
        with pytest.raises(ValueError):
            X, y = load_xy(0)
            MFE(measure_time="invalid").fit(X=X.values, y=y.values)

    @pytest.mark.parametrize(
        "value, group_name, allow_none, allow_empty",
        [
            (None, "groups", False, True),
            (None, "groups", False, False),
            ("", "group", False, False),
            ("", "group", True, False),
            ("invalid", "groups", False, False),
            ("all", "invalid", False, False),
            ("invalid", "groups", False, True),
            ("invalid", "groups", True, False),
            ("invalid", "groups", True, True),
            ("mean", "summary", True, True),
            ("all", "summary", True, True),
            ("num_inst", "features", True, True),
            ("all", "features", True, True),
        ])
    def test_error_process_generic_option_1(self,
                                            value,
                                            group_name,
                                            allow_none,
                                            allow_empty):
        with pytest.raises(ValueError):
            _internal.process_generic_option(
                    value=value,
                    group_name=group_name,
                    allow_none=allow_none,
                    allow_empty=allow_empty)

    def test_error_process_generic_option_2(self):
        with pytest.raises(TypeError):
            _internal.process_generic_option(
                    values=[1, 2, 3],
                    group_name=None)

    def test_error_process_generic_option_3(self):
        with pytest.raises(TypeError):
            _internal.process_generic_option(
                    values=[1, 2, 3],
                    group_name="timeopt")

    @pytest.mark.parametrize(
        "values, group_name, allow_none, allow_empty",
        [
            (None, "groups", False, True),
            (None, "groups", False, False),
            ("", "group", False, False),
            ([], "groups", True, False),
            ([], "groups", False, False),
            ("invalid", "groups", False, False),
            ("all", "invalid", False, False),
            ("invalid", "groups", False, True),
            ("invalid", "groups", True, False),
            ("invalid", "groups", True, True),
            ("mean", "summary", True, True),
            ("all", "summary", True, True),
            ("num_inst", "features", True, True),
            ("all", "features", True, True),
        ])
    def test_error_process_generic_set_1(self,
                                         values,
                                         group_name,
                                         allow_none,
                                         allow_empty):
        with pytest.raises(ValueError):
            _internal.process_generic_set(
                    values=values,
                    group_name=group_name,
                    allow_none=allow_none,
                    allow_empty=allow_empty)

    def test_error_process_generic_set_2(self):
        with pytest.raises(TypeError):
            _internal.process_generic_set(
                    values=[1, 2, 3],
                    group_name=None)

    @pytest.mark.parametrize(
        "summary",
        [
            "meanmean",
            "invalid",
        ])
    def test_error_unknown_summary(self, summary):
        with pytest.raises(ValueError):
            MFE(summary=summary)

    @pytest.mark.parametrize(
        "features",
        [
            None,
            [],
            "",
        ])
    def test_error_invalid_features(self, features):
        with pytest.raises(ValueError):
            MFE(features=features)

    @pytest.mark.parametrize(
        "score",
        [
            None,
            [],
            "",
            "invalid",
            "accuracyaccuracy",
        ])
    def test_error_invalid_score(self, score):
        with pytest.raises(ValueError):
            MFE(score=score)

    @pytest.mark.parametrize(
        "rescale",
        [
            "",
            "invalid",
            "minmax",
        ])
    def test_error_invalid_rescale_1(self, rescale):
        with pytest.raises(ValueError):
            X, y = load_xy(0)
            MFE().fit(X=X.values, y=y.values, rescale=rescale)

    def test_error_invalid_rescale_2(self):
        with pytest.raises(TypeError):
            X, y = load_xy(0)
            MFE().fit(X=X.values, y=y.values, rescale=[])

    @pytest.mark.parametrize(
        "features, groups",
        [
            ("invalid", "all"),
            ("invalid", "general"),
            ("mean", "info-theory"),
            ("nr_instt", "general"),
        ])
    def test_warning_invalid_features(self, features, groups):
        with pytest.warns(UserWarning):
            X, y = load_xy(0)
            model = MFE(features=features,
                        groups=groups).fit(X=X.values, y=y.values)
            model.extract()

    @pytest.mark.parametrize(
        "groups, precomp_groups",
        [
            ("all", "invalid"),
            ("general", "statistical"),
            ("info-theory", "general"),
            (["general", "statistical"], ["general", "info-theory"]),
        ])
    def test_warning_invalid_precomp(self, groups, precomp_groups):
        with pytest.warns(UserWarning):
            X, y = load_xy(0)
            MFE(groups=groups).fit(X=X.values,
                                   y=y.values,
                                   precomp_groups=precomp_groups)

    def test_warning_invalid_argument(self):
        with pytest.warns(UserWarning):
            X, y = load_xy(0)
            model = MFE(features="sd").fit(X=X.values, y=y.values)
            model.extract(sd={"ddof": 1, "invalid": "value?"})

    def test_verbose(self, capsys):
        X, y = load_xy(0)
        model = MFE(features=["freq_class",
                              "mean",
                              "class_conc",
                              "one_nn",
                              "nodes"]).fit(X=X.values, y=y.values)
        model.extract(verbose=True)
        captured = capsys.readouterr().out

        # Expected number of messages in verbose mode of mtf extraction
        expected_msg_num = 21

        assert captured.count("\n") == expected_msg_num
