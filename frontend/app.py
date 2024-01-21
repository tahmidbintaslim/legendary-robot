import time
import redis
from flask import Flask, render_template, Response

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return render_template('status.html')

@app.route('/stream')
def stream():
    def event_stream():
        # Send existing events
        existing_events = redis_client.lrange('events', 0, -1)
        for event in existing_events:
            yield f"data: {event.decode('utf-8')}\n\n"

        # Subscribe to new events
        pubsub = redis_client.pubsub()
        pubsub.subscribe('events')
        while True:
            message = pubsub.get_message()
            if message and message['type'] == 'message':
                yield f"data: {message['data'].decode('utf-8')}\n\n"
            time.sleep(1)
    return Response(event_stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)
