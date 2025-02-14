import asyncio
import json
import numpy as np
import mss
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame
print('running')

PEER_ID = "your_unique_peer_id"  # Set your peer ID for connection

class ScreenStreamTrack(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]  # Capture primary screen
    
    async def recv(self):
        frame = self.sct.grab(self.monitor)
        img = np.array(frame)[:, :, :3]  # Remove alpha channel
        img = VideoFrame.from_ndarray(img, format="rgb24")
        return img

async def run():
    pc = RTCPeerConnection()
    pc.addTrack(ScreenStreamTrack())
    
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    
    print(f"Send this offer to the receiver with ID {PEER_ID}:")
    print(json.dumps({"id": PEER_ID, "sdp": pc.localDescription.sdp, "type": pc.localDescription.type}))
    
    answer_str = input("Paste the answer here: ")
    answer = json.loads(answer_str)
    
    await pc.setRemoteDescription(RTCSessionDescription(sdp=answer["sdp"], type=answer["type"]))
    
    await asyncio.Future()  # Keep the connection open

if __name__ == "__main__":
    asyncio.run(run())
