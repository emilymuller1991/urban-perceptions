import logging
from unittest.mock import patch

from deep_cnn.utils import argument_parser


def test_train_model(root_dir, test_data, caplog):
    caplog.set_level(logging.INFO)
    from deep_cnn.train_model import main

    opt = argument_parser(
        [
            "--root_dir=" + str(root_dir) + "/",
            "--data_dir=" + str(test_data) + "/",
            "--epochs=1",
            "--batch_size=1",
            "--run_name=places",
        ]
    )

    with patch("torch.save") as mock_save:
        main(opt)

    # =================================
    # TEST SUITE
    # =================================
    # Check model has completed training for epoch
    # and output to save was called
    mock_save.assert_called()

    # =================================
    # TEST SUITE
    # =================================
    # Check model has completed training for epoch
    # and final losses printed
    assert "LOSS train" in str(caplog.records[-1])
