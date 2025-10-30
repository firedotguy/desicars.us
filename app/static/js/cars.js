document.addEventListener("DOMContentLoaded", () => {
  const filters = document.querySelectorAll(".filter");

  filters.forEach((filter) => {
    const dropdown = filter.querySelector(".filter-dropdown");

    filter.addEventListener("click", (e) => {
      e.stopPropagation();
      document.querySelectorAll(".filter.active").forEach((f) => {
        if (f !== filter) f.classList.remove("active");
      });
      filter.classList.toggle("active");
    });

    if (dropdown) {
      dropdown.addEventListener("click", (e) => e.stopPropagation());
    }
  });

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".filter")) {
      document.querySelectorAll(".filter.active").forEach((f) =>
        f.classList.remove("active")
      );
    }
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const minRange = document.getElementById("filter-price-range-min");
  const maxRange = document.getElementById("filter-price-range-max");
  const minInput = document.getElementById("filter-price-min-input");
  const maxInput = document.getElementById("filter-price-max-input");
  const track = document.getElementById("filter-price-track");

  const maxValue = 1000;
  const minGap = 10;

  const clamp = (v) => Math.min(Math.max(0, v), maxValue);

  function updateTrack() {
    const minVal = parseInt(minRange.value);
    const maxVal = parseInt(maxRange.value);
    const percentMin = (minVal / maxValue) * 100 + 1; // +1 prevents extra orange pixel after thumb
    const percentMax = (maxVal / maxValue) * 100;

    track.style.background = `
      linear-gradient(to right,
        #2a2a2a ${percentMin}%,
        #EB5E1B ${percentMin}%,
        #EB5E1B ${percentMax}%,
        #2a2a2a ${percentMax}%)
    `;
  }
const slider = document.getElementById("filter-price-slider");

slider.addEventListener("pointerdown", (e) => {
  const rect = slider.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const totalWidth = rect.width;
  const valueAtClick = Math.round((clickX / totalWidth) * maxValue);

  const distToMin = Math.abs(valueAtClick - minRange.value);
  const distToMax = Math.abs(valueAtClick - maxRange.value);

  if (distToMin < distToMax) {
    minRange.style.zIndex = 5;
    maxRange.style.zIndex = 4;
    minRange.value = valueAtClick;
  } else {
    maxRange.style.zIndex = 5;
    minRange.style.zIndex = 4;
    maxRange.value = valueAtClick;
  }

  syncFromRange();
});

  function syncFromRange() {
    let minVal = +minRange.value;
    let maxVal = +maxRange.value;

    if (maxVal - minVal < minGap) {
      if (minVal < maxValue / 2) minRange.value = maxVal - minGap;
      else maxRange.value = minVal + minGap;
    }

    minInput.value = minRange.value;
    maxInput.value = maxRange.value;
    updateTrack();
  }

  function syncFromInputs() {
    let minVal = parseInt(minInput.value);
    let maxVal = parseInt(maxInput.value);

    if (isNaN(minVal)) minVal = 0;
    if (isNaN(maxVal)) maxVal = 0;

    minRange.value = clamp(minVal);
    maxRange.value = clamp(maxVal);

    if (+maxRange.value - +minRange.value < minGap) {
      if (+minRange.value + minGap <= maxValue)
        maxRange.value = +minRange.value + minGap;
      else minRange.value = +maxRange.value - minGap;
    }

    minInput.value = minRange.value;
    maxInput.value = maxRange.value;
    updateTrack();
  }

  [minInput, maxInput].forEach((input) => {
    input.addEventListener("keypress", (e) => {
      if (!/[0-9]/.test(e.key)) e.preventDefault();
    });
  });

  minRange.addEventListener("input", syncFromRange);
  maxRange.addEventListener("input", syncFromRange);
  minInput.addEventListener("input", syncFromInputs);
  maxInput.addEventListener("input", syncFromInputs);

  updateTrack();
});

document.querySelectorAll("#filter-price-slider input[type='range']").forEach((range) => {
  range.addEventListener("mousedown", (e) => {
    const rect = range.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const percent = (clickX / rect.width) * 100;
    const minPercent = (minRange.value / maxValue) * 100;
    const maxPercent = (maxRange.value / maxValue) * 100;

    const closerToMin = Math.abs(percent - minPercent) < Math.abs(percent - maxPercent);
    if (closerToMin) {
      minRange.style.zIndex = 5;
      maxRange.style.zIndex = 4;
    } else {
      maxRange.style.zIndex = 5;
      minRange.style.zIndex = 4;
    }
  });
});