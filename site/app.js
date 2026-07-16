const grid = document.querySelector("#sticker-grid");
const template = document.querySelector("#sticker-template");
const selectionBar = document.querySelector("#selection-bar");
const selectionCount = document.querySelector("#selection-count");
const selectAll = document.querySelector("#select-all");
const clearSelection = document.querySelector("#clear-selection");
const downloadSelection = document.querySelector("#download-selection");
const downloadNotice = document.querySelector("#download-notice");
const stickerCount = document.querySelector("#sticker-count");
const loadError = document.querySelector("#load-error");

const selected = new Set();
let stickers = [];
let noticeTimer;

const displayNames = {
  facepalm: "Face Palm",
  fingerguns: "Finger Guns",
  handraise: "Hand Raise",
  intenseglare: "Intense Glare",
  sixseven: "Six Seven",
  thumbsup: "Thumbs Up",
};

const formatDate = (date) =>
  new Intl.DateTimeFormat("en-SG", {
    day: "numeric",
    month: "short",
    year: "numeric",
  }).format(new Date(`${date}T00:00:00Z`));

const titleCase = (slug) =>
  displayNames[slug] || slug
    .replace(/[-_]+/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());

const showNotice = (message) => {
  window.clearTimeout(noticeTimer);
  downloadNotice.textContent = message;
  downloadNotice.hidden = false;
  noticeTimer = window.setTimeout(() => {
    downloadNotice.hidden = true;
  }, 3600);
};

const updateSelectionUI = () => {
  const count = selected.size;
  selectionCount.textContent = count;
  selectionBar.hidden = count === 0;
  downloadSelection.querySelector("span").textContent =
    count === 1 ? "Download 1" : `Download ${count}`;

  selectAll.checked = stickers.length > 0 && count === stickers.length;
  selectAll.indeterminate = count > 0 && count < stickers.length;
};

const triggerDownload = (sticker) => {
  const link = document.createElement("a");
  link.href = sticker.path;
  link.download = sticker.filename;
  link.hidden = true;
  document.body.append(link);
  link.click();
  link.remove();
};

const downloadMany = async () => {
  const files = stickers.filter((sticker) => selected.has(sticker.slug));
  if (files.length === 0) return;

  showNotice(
    files.length === 1
      ? "Your sticker is downloading."
      : `${files.length} stickers are downloading separately. Your browser may ask for permission.`,
  );

  for (const sticker of files) {
    triggerDownload(sticker);
    await new Promise((resolve) => window.setTimeout(resolve, 180));
  }
};

const renderSticker = (sticker, index) => {
  const fragment = template.content.cloneNode(true);
  const item = fragment.querySelector(".sticker-item");
  const image = fragment.querySelector("img");
  const checkbox = fragment.querySelector("input");
  const checkboxLabel = fragment.querySelector(".sticker-select .sr-only");
  const download = fragment.querySelector(".item-download");
  const heading = fragment.querySelector("h3");
  const time = fragment.querySelector("time");
  const name = titleCase(sticker.slug);

  item.style.setProperty("--item-index", index);
  item.dataset.slug = sticker.slug;
  image.src = sticker.path;
  image.alt = `${name} T Krobot sticker`;
  checkbox.setAttribute("aria-label", `Select ${name}`);
  checkboxLabel.textContent = `Select ${name}`;
  download.href = sticker.path;
  download.download = sticker.filename;
  download.setAttribute("aria-label", `Download ${name} PNG`);
  heading.textContent = name;
  time.dateTime = sticker.updated_at;
  time.textContent = formatDate(sticker.updated_at);

  checkbox.addEventListener("change", () => {
    if (checkbox.checked) selected.add(sticker.slug);
    else selected.delete(sticker.slug);
    updateSelectionUI();
  });

  download.addEventListener("click", () => {
    showNotice(`${name} is downloading.`);
  });

  grid.append(fragment);
};

selectAll.addEventListener("change", () => {
  selected.clear();
  if (selectAll.checked) stickers.forEach((sticker) => selected.add(sticker.slug));
  grid.querySelectorAll(".sticker-select input").forEach((checkbox) => {
    checkbox.checked = selectAll.checked;
  });
  updateSelectionUI();
});

clearSelection.addEventListener("click", () => {
  selected.clear();
  grid.querySelectorAll(".sticker-select input").forEach((checkbox) => {
    checkbox.checked = false;
  });
  updateSelectionUI();
});

downloadSelection.addEventListener("click", downloadMany);

fetch("/stickers.json")
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then((data) => {
    stickers = data.items;
    stickerCount.textContent = stickers.length;
    stickers.forEach(renderSticker);
  })
  .catch((error) => {
    console.error("Unable to load stickers", error);
    loadError.hidden = false;
  });
