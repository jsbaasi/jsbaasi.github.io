---
layout: default
---

<section>
    {% assign posts = site.posts | sort: "last_modified_at"%}
    {% for post in posts %}
    <article>
      <a href="{{ post.url }}"><h4>{{ post.title }}</h4></a>
      <p>{{ post.date | date: "Published: %d/%m/%y" }}</p>
      <p>{{ post.last_modified_at | date: "Edited: %d/%m/%y" }}</p>
    </article>
  {% endfor %}
</section>
