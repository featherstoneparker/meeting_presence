import time
from presence import TeamsPresence
from effects import BlynclightEffect
from effects.govee import GoveeLanEffect

POLL_INTERVAL = 2  # seconds

GOVEE_IP = "192.168.x.x"  # set to your Govee bulb's IP or local hostname


def main() -> None:
    provider = TeamsPresence()
    effects = [
        BlynclightEffect(),
        GoveeLanEffect(ip=GOVEE_IP, brightness=5),
    ]

    last_availability = None

    print("Watching Teams presence... (Ctrl+C to stop)")
    while True:
        try:
            status = provider.get_status()
            if status.availability != last_availability:
                print(f"{status}")
                for effect in effects:
                    effect.apply(status)
                last_availability = status.availability
        except Exception as e:
            print(f"Error reading presence: {e}")
            if last_availability is not None:
                for effect in effects:
                    effect.on_unavailable()
                last_availability = None

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
