<%*
const title = await tp.system.prompt("Title");
const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const date = tp.date.now("YYYY-MM-DD");
const time = tp.date.now("HH:mm:ss");
await tp.file.rename(`${date}-${slug}`);
-%>
---
layout: post
title: "<% title %>"
date: <% date %> <% time %> +0000
categories: <% await tp.system.prompt("Categories (space-separated)") %>
permalink: /<% slug %>/
---