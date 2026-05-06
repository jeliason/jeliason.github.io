---
title:
layout: default
permalink: /projects/
published: true
---

<div class="ProjectContainer">

<ul class="project-list">
  {% for project in site.projects %}
    {% if project.redirect %}
      {% assign href = project.redirect %}
    {% else %}
      {% capture href %}{{ project.url | prepend: site.baseurl | prepend: site.url }}{% endcapture %}
    {% endif %}
    <li class="project-item">
      <a href="{{ href }}"{% if project.redirect %} target="_blank"{% endif %}>
        <h2>{{ project.title }}</h2>
      </a>
      {% if project.description %}<p>{{ project.description }}</p>{% endif %}
    </li>
  {% endfor %}
</ul>

</div>
