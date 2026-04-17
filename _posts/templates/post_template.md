<%*
const title = await tp.system.prompt("Title");
const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
await tp.file.rename(slug);
-%>
---
layout: post
title: "<% title %>"
date: <% tp.date.now("YYYY-MM-DD HH:mm:ss") %> +0000
categories: <% await tp.system.prompt("Categories (space-separated)") %>
permalink: /<% slug %>/
---