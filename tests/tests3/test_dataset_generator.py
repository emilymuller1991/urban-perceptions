def test_dataset_generator(root_dir, test_data, metadata, study, params):
    """tests dataset iterator"""
    from deep_cnn.dataset_generator import dataloader

    train_dataloader, _, N = dataloader(
        test_data, root_dir, "resnet", "train", params, val_split=0
    )

    for x, y in train_dataloader:
        print(y)
        a = x.numpy()
        # =================================
        # TEST SUITE
        # =================================
        # Check train and test images are of size 1
        assert ((-3 <= a) & (a <= 3)).all()
        assert ((0 <= y) & (y <= 4)).all()
    assert N == 5
