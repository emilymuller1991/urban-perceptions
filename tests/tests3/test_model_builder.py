import torch


def test_model_builder():
    from deep_cnn.model_builder import MyCNN

    """Test random input
    passes through resnet101 network
    returning a single prediction"""
    model = MyCNN()
    x = torch.randn(1, 3, 224, 224)
    out = model(x)
    print(out.shape)
    # =================================
    # TEST SUITE
    # =================================
    # Check the length of the returned object
    assert out.shape[1] == 365


def test_model_builder2():
    from deep_cnn.model_builder import MyCNN

    """Test random input
    passes through resnet18 network
    returning a single prediction"""
    model = MyCNN(model_base="resnet18")
    x = torch.randn(1, 3, 224, 224)
    out = model(x)
    # =================================
    # TEST SUITE
    # =================================
    # Check the length of the returned object
    assert out.shape[1] == 365
