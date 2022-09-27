import numpy as np
import torch
import torch.nn as nn


def test_training_epoch(root_dir, test_data, params):
    """tests dataset iterator"""
    import deep_cnn.train as train
    from deep_cnn.dataset_generator import dataloader
    from deep_cnn.model_builder import MyCNN

    train_dataloader, _, N = dataloader(
        test_data, root_dir, "resnet", "train", params, val_split=0
    )
    val_dataloader, _, N = dataloader(test_data, root_dir, "resnet", "val", params)
    model = MyCNN()

    optimizer = torch.optim.Adam(model.parameters(), 0.001)
    loss_fn = nn.CrossEntropyLoss()

    train_val_loss = train.train(
        model=model,
        train_dataloader=train_dataloader,
        val_dataloader=val_dataloader,
        optimizer=optimizer,
        scheduler=None,
        loss_fn=loss_fn,
        epochs=1,
        device="cpu",
        save_model=None,
        wb=False,
    )
    # =================================
    # TEST SUITE
    # =================================
    # Check train loss is not none and val loss is np.nan
    assert train_val_loss["train_loss"][0] != np.nan
    assert train_val_loss["val_loss"][0] != np.nan
    assert train_val_loss["train_precision@1"][0] != np.nan
    assert train_val_loss["val_precision@1"][0] != np.nan
