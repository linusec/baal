import numpy as np
import torch
from scipy.special import softmax


def to_prob(probabilities: np.ndarray):
    """
    If the probabilities array is not a distrubution will softmax it.

    Args:
        probabilities (array): [batch_size, num_classes, ...]

    Returns:
        Same as probabilities.
    """
    bounded = np.min(probabilities) < 0 or np.max(probabilities) > 1.0
    if bounded or not np.allclose(probabilities.sum(1), 1):
        probabilities = softmax(probabilities, 1)
    return probabilities


def stack_in_memory(data, iterations):
    """
    Stack `data` `iterations` times on the batch axis.
    Args:
        data (Tensor): Data to stack
        iterations (int): Number of time to stack.

    Raises:
        RuntimeError when CUDA is out of memory.

    Returns:
        Tensor with shape [batch_size * iterations, ...]
    """
    input_shape = data.size()
    batch_size = input_shape[0]
    try:
        data = torch.stack([data] * iterations)
    except RuntimeError as e:
        raise RuntimeError(
            '''CUDA ran out of memory while BaaL tried to replicate data. See the exception above.
        Use `replicate_in_memory=False` in order to reduce the memory requirements.
        Note that there will be some speed trade-offs''') from e
    data = data.view(batch_size * iterations, *input_shape[1:])
    return data
