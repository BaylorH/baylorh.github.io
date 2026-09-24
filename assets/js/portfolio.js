// Content and navigation work without JavaScript; this layer adds filtering and image inspection.
const filters = document.querySelector(".filters");
if (filters) {
  filters.hidden = false;
  const cards = [...document.querySelectorAll("[data-category]")];
  const count = document.querySelector(".project-count");
  filters.addEventListener("click", (event) => {
    const button = event.target.closest("[data-filter]");
    if (!button) return;
    filters
      .querySelectorAll("button")
      .forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
    cards.forEach((card) => {
      card.hidden =
        button.dataset.filter !== "all" &&
        card.dataset.category !== button.dataset.filter;
    });
    const visible = cards.filter((card) => !card.hidden).length;
    count.textContent = `${visible} ${visible === 1 ? "project" : "projects"}`;
  });
}
const viewer = document.querySelector("#image-viewer");
if (viewer && typeof viewer.showModal === "function") {
  let trigger;
  document.querySelectorAll(".legacy-content img").forEach((image) => {
    if (image.closest("a")) return;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "image-expand";
    button.setAttribute("aria-label", `Expand ${image.alt || "project image"}`);
    image.replaceWith(button);
    button.append(image);
    button.addEventListener("click", () => {
      trigger = button;
      viewer.querySelector("img").src = image.src;
      viewer.querySelector("img").alt = image.alt;
      viewer.querySelector("p").textContent = image.alt;
      viewer.showModal();
    });
  });
  viewer
    .querySelector("button")
    .addEventListener("click", () => viewer.close());
  viewer.addEventListener("click", (event) => {
    if (event.target === viewer) viewer.close();
  });
  viewer.addEventListener("close", () => trigger?.focus());
}
