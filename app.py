from flask import Flask, request, jsonify, Response
import os
import syncedlyrics

app = Flask(__name__)

# --- Reusable lyrics function ---
def fetch_and_save_lyrics(track_name: str, artist_name: str, save_folder: str = "."):
    """
    Fetch lyrics for a track and artist, save as .lrc file.
    Returns (filename, lyrics) or None if lyrics not found.
    """
    query = f"{track_name} {artist_name}"
    lrc = syncedlyrics.search(query)
    if not lrc:
        return None

    os.makedirs(save_folder, exist_ok=True)
    # Make filename safe for filesystem
    safe_track_name = "".join(c for c in track_name if c.isalnum() or c in " _-")
    filename = os.path.join(save_folder, f"{safe_track_name}.lrc")

    with open(filename, "w", encoding="utf-8") as file:
        file.write(lrc)

    return filename, lrc


# --- Endpoint to fetch and display lyrics ---
@app.route("/lyrics")
def get_lyrics():
    artist = request.args.get("artist", "").strip()
    track = request.args.get("track", "").strip()

    if not artist or not track:
        return jsonify({"error": "Missing artist or track parameter"}), 400

    result = fetch_and_save_lyrics(track, artist)
    if not result:
        return jsonify({"error": "Lyrics not found"}), 404

    _, lrc = result
    return jsonify({"track": track, "lyrics": lrc})


# --- Endpoint to download .lrc file ---
@app.route("/download")
def download_lyrics():
    artist = request.args.get("artist", "").strip()
    track = request.args.get("song", "").strip()  # matches frontend download link param

    if not artist or not track:
        return jsonify({"error": "Missing artist or song parameter"}), 400

    result = fetch_and_save_lyrics(track, artist)
    if not result:
        return jsonify({"error": "Lyrics not found"}), 404

    filename, lrc = result
    return Response(
        lrc,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment;filename={os.path.basename(filename)}"}
    )


if __name__ == "__main__":
    # Listen on all interfaces so Render can access it
    app.run(host="0.0.0.0", port=5000)
