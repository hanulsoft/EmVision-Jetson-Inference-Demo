import sys
from pathlib import Path

sys.path.append(Path(__file__).parent.parent.as_posix())
print(sys.path)
from src.config import MODEL_COMMENDS

from jetson_inference import (
    actionNet,
    backgroundNet,
    depthNet,
    detectNet,
    imageNet,
    poseNet,
    segNet,
)

if __name__ == "__main__":
    for cmds in MODEL_COMMENDS:
        try:
            name, network = cmds.split(" ")
            if name == "actionnet":
                net = actionNet(network)
                del net
            elif name == "backgroundnet":
                net = backgroundNet(network)
                del net
            elif name == "depthnet":
                net = depthNet(network)
                del net
            elif name == "detectnet":
                net = detectNet(network)
                del net
            elif name == "imagenet":
                net = imageNet(network)
                del net
            elif name == "posenet":
                net = poseNet(network)
                del net
            elif name == "segnet":
                net = segNet(network)
                del net
            else:
                print(f"unknown model name: {name}")
                continue
            print(f"{name} {network} loaded")
        except Exception as e:
            print(e)
            print(f"failed to load {name} {network}")
            continue
