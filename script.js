    // Replace with your Render backend URL
    const backendURL = "https://lrc-scraper.onrender.com";

    document.getElementById("fetch").onclick = async () => {
      const artist = document.getElementById("artist").value.trim();
      const track = document.getElementById("track").value.trim();
      const resultsDiv = document.getElementById("results");
      resultsDiv.innerHTML = "";

      if (!artist || !track) {
        resultsDiv.innerHTML = "<p>Please enter both artist and track name.</p>";
        return;
      }

      resultsDiv.innerHTML = "<p>Fetching lyrics...</p>";

      try {
        const res = await fetch(`${backendURL}/download?song=${encodeURIComponent(track)}&artist=${encodeURIComponent(artist)}`);
        if (!res.ok) {
          const errorData = await res.json();
          resultsDiv.innerHTML = `<p>Error: ${errorData.error}</p>`;
          return;
        }

        const lyrics = await res.text();
        resultsDiv.innerHTML = "";

        const trackTitle = document.createElement("h3");
        trackTitle.textContent = track;
        resultsDiv.appendChild(trackTitle);

        const pre = document.createElement("pre");
        pre.textContent = lyrics;
        resultsDiv.appendChild(pre);

        // Add download link
        const link = document.createElement("a");
        link.href = `${backendURL}/download?song=${encodeURIComponent(track)}&artist=${encodeURIComponent(artist)}`;
        link.innerText = "Download .lrc";
        resultsDiv.appendChild(link);

      } catch (err) {
        resultsDiv.innerHTML = `<p>Error fetching lyrics: ${err}</p>`;
      }
    };