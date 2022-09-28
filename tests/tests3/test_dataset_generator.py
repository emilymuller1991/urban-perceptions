def test_dataset_generator(root_dir, test_data, study, params):
    """tests dataset iterator"""
    from deep_cnn.dataset_generator import dataloader_pp
    from deep_cnn.datautils import pp_process_input

    df_train, _, _ = pp_process_input(
        root_dir=root_dir,
        data_dir=test_data,
        oversample=False,
        verbose=False,
        perception_study=study,
    )
    train_dataloader = dataloader_pp(
        df_train, root_dir, test_data, "resnet", "train", params
    )

    for x, y in train_dataloader:
        print(y)
        y = y.numpy()
        a = x.numpy()
        # =================================
        # TEST SUITE
        # =================================
        # Check train and test images are of size 1
        assert ((-3 <= a) & (a <= 3)).all()
        assert ((0 <= y) & (y <= 10)).all()
    assert train_dataloader.__len__() != 0
