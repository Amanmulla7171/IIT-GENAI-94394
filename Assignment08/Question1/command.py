import os
import time

from youtube_automataion import (
    create_driver,
    search_and_open_first_video,
    force_play_video,
    try_skip_ad,
    close_driver,
)

COMMANDS_FILE = "commands.txt"


def process_commands():
    """
    Single function that:
      - Reads commands.txt
      - For each line:
          PLAY_VIDEO <query...> -> run YouTube automation with only query
          CLOSE_VIDEO           -> call close_driver()
      - Clears commands.txt after executing
      - Keeps looping every 2 seconds to see new commands
    """
    driver = None
    print(f"[Watcher] Watching {COMMANDS_FILE}...")

    try:
        while True:
            if not os.path.exists(COMMANDS_FILE):
                time.sleep(2)
                continue

            # read all lines
            with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

            if lines:
                print(f"[Watcher] Found {len(lines)} command(s).")

                for line in lines:
                    # PLAY_VIDEO: ignore the word PLAY_VIDEO, use only query
                    if line.upper().startswith("PLAY_VIDEO"):
                        # split once: "PLAY_VIDEO", "query..."
                        parts = line.split(maxsplit=1)
                        if len(parts) < 2:
                            print(f"[Watcher] PLAY_VIDEO has no query: {line}")
                            continue

                        query = parts[1]  # ONLY the query
                        print(f"[Watcher] Playing query: {query!r}")

                        if driver is None:
                            driver = create_driver()

                        # call youtube_automation functions
                        search_and_open_first_video(driver, query)
                        force_play_video(driver)

                        # simple ad skip loop
                        for _ in range(20):
                            try_skip_ad(driver)
                            time.sleep(1)

                    # CLOSE_VIDEO: call close_driver from youtube_automation
                    elif line.upper().startswith("CLOSE_VIDEO"):
                        print("[Watcher] Closing video/browser")
                        close_driver(driver)
                        driver = None

                    else:
                        # unknown command
                        print(f"[Watcher] Unknown command: {line}")

                # clear file after processing all commands
                try:
                    open(COMMANDS_FILE, "w").close()
                    print("[Watcher] Cleared commands.txt.")
                except Exception as e:
                    print(f"[Watcher] Failed to clear file: {e}")

            time.sleep(2)
    finally:
        close_driver(driver)


if __name__ == "__main__":
    process_commands()
