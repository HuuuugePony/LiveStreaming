from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)
gangmao = "8.138.224.98"

HLS_PATH = "/tmp/hls"
RTMP_SERVER = f"rtmp://{gangmao}/live"

# 模拟在线人数（真实场景可通过 Nginx RTMP status 或 WebSocket 统计）
ONLINE_VIEWERS = {
    "test": -1,
    "user2": -1
}

def get_streams():
    streams = []
    if os.path.exists(HLS_PATH):
        for f in os.listdir(HLS_PATH):
            if f.endswith(".m3u8"):
                name = f.replace(".m3u8","")
                streams.append({
                    "name": name,
                    "online": True,
                    "viewers": ONLINE_VIEWERS.get(name, 0)
                })
    return streams

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/streams")
def api_streams():
    return jsonify(get_streams())

@app.route("/watch/<stream_name>")
def watch(stream_name):
    hls_url = f"http://{gangmao}:8080/hls/{stream_name}.m3u8"
    rtmp_url = f"{RTMP_SERVER}/{stream_name}"
    return render_template("stream.html", hls_url=hls_url, rtmp_url=rtmp_url, stream_name=stream_name)

@app.route("/push_info")
def push_info():
    return render_template("push_info.html", rtmp_server=RTMP_SERVER)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
