<script setup>

import Search from "@/components/Search.vue";
</script>

<template>
  <div class="hackalod">
    <header>
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
        </ul>
      </nav>
    </header>
    <main>
      <Search />
    </main>
    <footer>
      <ul>
        <li><a href="/disclaimer">Disclaimer</a></li>
      </ul>
    </footer>
  </div>
</template>

<style scoped>
.hackalod {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* ensure it takes up the full viewport height */
  min-width: 100vw; /* ensure it takes up the full viewport width */
}

header {
  background: #333;
  color: #fff;
  padding: 1rem 0;
  position: sticky;
  top: 0; /* this makes the header sticky at the top */
  z-index: 10; /* raise header above other content, if needed */
  width: 100vw; /* ensure it takes up the full width */
  box-sizing: border-box; /* ensure padding does not affect width */
}

main {
  flex: 1; /* this allows the main content to grow and take up all available space */
  padding: 1rem 2rem;
}

footer {
  background: #333;
  color: #fff;
  padding: 1rem 0;
}

nav ul {
  list-style-type: none; /* remove bullet points */
  padding: 0; /* reset default padding */
  margin: 0; /* reset default margin */
  display: flex; /* make it a flex container */
  align-items: center; /* vertically align the links in case they are of different heights */
}

nav li {
  margin: 0 15px; /* spacing between each list item */
}

nav a {
  text-decoration: none; /* remove underlines from links */
  color: #fff; /* white color text for links */
  transition: color 0.3s; /* smooth color transition for hover effect */
}

nav a:hover {
  color: #ddd; /* slightly dimmed color for hover effect */
}
</style>