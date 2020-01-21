# Require TensorRT 6+

from tqdm import tqdm
import random

import tensorrt as trt
import numpy as np
import torch

DYNAMIC_SHAPE_INPUT = True
MAX_INPUT_SIZE = 103

def build_network(builder):
    if DYNAMIC_SHAPE_INPUT:
        network = builder.create_network(
            1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
        )
    else:
        network = builder.create_network()

    if DYNAMIC_SHAPE_INPUT:
        input_trt_tensor = network.add_input(
            name="input_0", shape=(1, 3, -1, -1), dtype=trt.float32,
        )
    else:
        input_trt_tensor = network.add_input(
            name="input_0", shape=(1, 3, MAX_INPUT_SIZE, MAX_INPUT_SIZE), dtype=trt.float32,
        )

    input_trt_tensor.location = trt.TensorLocation.DEVICE

    # add conv layer
    conv_out_channels = 8
    conv_in_channels = 3
    kernel = np.random.rand(conv_out_channels, conv_in_channels, 3, 3).astype(
        np.float32
    )
    bias = np.random.rand(conv_out_channels).astype(np.float32)
    conv_layer = network.add_convolution(
        input=input_trt_tensor,
        num_output_maps=conv_out_channels,
        kernel_shape=(3, 3),
        kernel=kernel,
        bias=bias,
    )
    conv_layer.stride = (1, 1)
    conv_layer.padding = (1, 1)
    conv_layer.dilation = (1, 1)

    output_trt_tensor = conv_layer.get_output(0)
    output_trt_tensor.name = "output_0"
    output_trt_tensor.location = trt.TensorLocation.DEVICE
    output_trt_tensor.dtype = trt.float32
    network.mark_output(output_trt_tensor)
    return network


def create_builder():
    trt_logger = trt.Logger(trt.Logger.ERROR)
    builder = trt.Builder(trt_logger)
    builder.max_workspace_size = 0
    builder.fp16_mode = False
    builder.max_batch_size = 1
    builder.strict_type_constraints = False
    return builder


if __name__ == "__main__":
    print("dynamic shape input: {}".format(DYNAMIC_SHAPE_INPUT))
    builder = create_builder()
    network = build_network(builder)

    if DYNAMIC_SHAPE_INPUT:
        binding_shape_cache = {}
        config = builder.create_builder_config()
        profile = builder.create_optimization_profile()
        profile.set_shape(
            "input_0", min=(1, 3, 100, 100), opt=(1, 3, 101, 101), max=(1, 3, MAX_INPUT_SIZE, MAX_INPUT_SIZE)
        )
        config.add_optimization_profile(profile)
        print("Build cuda engine with config")
        engine = builder.build_engine(network, config)
    else:
        print("Build cuda engine without config")
        engine = builder.build_cuda_engine(network)
    context = engine.create_execution_context()

    for it in tqdm(range(10000)):
        if DYNAMIC_SHAPE_INPUT:
            in_out_shape = (1, 3, random.randint(100, MAX_INPUT_SIZE), random.randint(100, MAX_INPUT_SIZE))
        else:
            in_out_shape = (1, 3, MAX_INPUT_SIZE, MAX_INPUT_SIZE)
        torch_input = torch.randn(in_out_shape, dtype=torch.float32).cuda()
        torch_output = torch.empty(
            size=in_out_shape, dtype=torch.float32, device=torch.device("cuda")
        )

        bindings = [None] * 2
        bindings[engine.get_binding_index("input_0")] = torch_input.data_ptr()
        bindings[engine.get_binding_index("output_0")] = torch_output.data_ptr()

        if DYNAMIC_SHAPE_INPUT:
            # context.execute_async_v2(bindings, torch.cuda.current_stream().cuda_stream)
            if torch_input.shape not in binding_shape_cache:
                # Cache is important to prevent CUDA GPU memory increase!!!!
                print(f"Set new binding shape: {torch_input.shape}")
                context.set_binding_shape(0, torch_input.shape)
                binding_shape_cache[torch_input.shape] = 0
            context.execute_v2(bindings)
        else:
            # context.execute_async(1, bindings, torch.cuda.current_stream().cuda_stream)
            context.execute(1, bindings)
