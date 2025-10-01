---
layout: default
title: "Contact"
permalink: /contact/
---

## Contact

Have a question, recipe suggestion, or just want to say hi?

{% raw %}
<form action="https://formspree.io/f/yourformid" method="POST" class="contact-form">

  <label for="name">Name:</label><br />
  <input type="text" id="name" name="name" required /><br />

  <label for="email">Email:</label><br />
  <input type="email" id="email" name="_replyto" required /><br />

  <label for="message">Message:</label><br />
  <textarea id="message" name="message" required></textarea><br />

  <button type="submit">Send Message</button>
</form>
{% endraw %}

