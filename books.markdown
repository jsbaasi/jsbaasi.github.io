---
layout: default
---

<script>
  document.addEventListener("DOMContentLoaded", async () => {
    let locations = {};
    try {
      const res = await fetch("/locations.json");
      locations = await res.json();
    } catch (err) {
      console.error("Failed to load locations:", err);
    }
    document.querySelectorAll(".book-item, .featured-book").forEach(item => {
      const file = item.getAttribute("data-file");
      const target = item.querySelector(".file-number");
      if (file && target) {
        target.textContent = locations[file] !== undefined
          ? locations[file] + "%"
          : "N/A";
      }
    });
  });
</script>

<books class="books-page">
  <div class="featured-books-container">
    {% assign current_key = site.data.books.current %}
    {% assign b = site.data.books.books[current_key] %}
    <section class="featured-book" data-file="{{ current_key }}">
      <img src="covers/{{ b.cover }}" alt="{{ b.title }}" class="featured-img">
      <h2>{{ b.title }}</h2>
      <p>by {{ b.author }}</p>
      <p class="book-metric">
        <span class="loading-dots--dot"></span>
        Location: <span class="file-number">...</span>
      </p>
    </section>
  </div>

  <section class="book-carousel">
    <h3>Books I've Read</h3>
    <div class="carousel">
      {% for book in site.data.books.books %}
        {% assign b = book[1] %}
        {% if book[0] != current_key %}
        <div class="book-item" data-file="{{ book[0] }}">
          <img src="covers/{{ b.cover }}" alt="{{ b.title }}" class="featured-img">
          <p><strong>{{ b.title }}</strong><br>{{ b.author }}</p>
          {% if b.started %}<p>Started: {{ b.started }}</p>{% endif %}
          {% if b.ttr %}<p>TTR: {{ b.ttr }}</p>{% endif %}
          {% if b.rating %}<div class="rating">{{ b.rating }}</div>{% endif %}
          <p class="book-metric">Location: <span class="file-number">...</span></p>
        </div>
        {% endif %}
      {% endfor %}
    </div>
  </section>
</books>
