---
layout: default
---

<section>
  {% for post in site.posts %}
    <article>
      <a href="{{ post.url }}"><h4>{{ post.title }}</h4></a>
      <p>{{ post.date | date: "%d/%m/%y" }}</p>
    </article>
  {% endfor %}
</section>
