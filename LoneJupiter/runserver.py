from lone_jupiter import app, config
import platform

if __name__ == '__main__':
    app.run(threaded=True,  host=config.get("Default", "Flask_tcp_ip"), use_reloader=False,
            port=int(config.get("Default", "Flask_tcp_port")))
