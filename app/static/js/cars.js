const RANGESLIDER_MIN_SPACING = 20;
const RANGESLIDER_MIN_VALUE = 0;
const RANGESLIDER_MAX_VALUE = 1000;

// filter show/hide
document.addEventListener("DOMContentLoaded", () => {
  const filters = document.querySelectorAll(".filter");

  filters.forEach((filter) => {
    const dropdown = filter.querySelector(".filter-dropdown");

    filter.addEventListener("mousedown", (e) => {
      e.stopPropagation();
      document.querySelectorAll(".filter.active").forEach((f) => {
        if (f !== filter) f.classList.remove("active");
      });
      filter.classList.toggle("active");
    });

    if (dropdown) {
      dropdown.addEventListener("mousedown", (e) => e.stopPropagation());
    }
  });

  document.addEventListener("mousedown", (e) => {
    if (!e.target.closest(".filter")) {
      document.querySelectorAll(".filter.active").forEach((f) =>
        f.classList.remove("active")
      );
    }
  });
});


// price filter (vanilla-rangeslider)
document.addEventListener("DOMContentLoaded", () => {
  const sliderInput = document.getElementById("filter-price-slider");
  const minInput = document.getElementById("filter-price-min-input");
  const maxInput = document.getElementById("filter-price-max-input");

  const slider = ionRangeSlider(sliderInput, {
    type: "double",
    min: RANGESLIDER_MIN_VALUE,
    max: RANGESLIDER_MAX_VALUE,
    from: +minInput.value || RANGESLIDER_MIN_VALUE,
    to: +maxInput.value || RANGESLIDER_MAX_VALUE,
    step: 5,
    onChange: (data) => {
        minInput.value = data.from;
        maxInput.value = data.to;
        if (minInput.value == maxInput.value){
            minInput.value -= RANGESLIDER_MIN_SPACING;
        }
        if (minInput.value > parseInt(maxInput.value) + RANGESLIDER_MIN_SPACING){
            minInput.value = parseInt(maxInput.value) - RANGESLIDER_MIN_SPACING;
        } else if (parseInt(maxInput.value) === RANGESLIDER_MAX_VALUE && parseInt(minInput.value) > RANGESLIDER_MAX_VALUE - RANGESLIDER_MIN_SPACING) {
            minInput.value = RANGESLIDER_MAX_VALUE - RANGESLIDER_MIN_SPACING;
        }
        if (maxInput.value < parseInt(minInput.value) - RANGESLIDER_MIN_SPACING){
        maxInput.value = parseInt(minInput.value) + RANGESLIDER_MIN_SPACING;
        } else if (parseInt(minInput.value) === 0 && parseInt(maxInput.value) < RANGESLIDER_MIN_SPACING){
            maxInput.value = RANGESLIDER_MIN_SPACING;
        }
    }
  });

  minInput.addEventListener("change", () => {
    minInput.value = minInput.value.replace(/\D/g, '');
    if (minInput.value === ''){
        minInput.value = RANGESLIDER_MIN_VALUE;
    }
    if (minInput.value == maxInput.value){
        minInput.value -= RANGESLIDER_MIN_SPACING;
    }
    if (minInput.value > parseInt(maxInput.value) + RANGESLIDER_MIN_SPACING){
        minInput.value = parseInt(maxInput.value) - RANGESLIDER_MIN_SPACING;
    } else if (parseInt(maxInput.value) === RANGESLIDER_MAX_VALUE && parseInt(minInput.value) > RANGESLIDER_MAX_VALUE - RANGESLIDER_MIN_SPACING) {
        minInput.value = RANGESLIDER_MAX_VALUE - RANGESLIDER_MIN_SPACING;
    }
    slider.update({ from: +minInput.value });
  });
  maxInput.addEventListener("change", () => {
    maxInput.value = maxInput.value.replace(/\D/g, '');
    if (maxInput.value === ''){
        maxInput.value = 0;
    }
    if (minInput.value == maxInput.value){
        maxInput.value = parseInt(maxInput.value) + RANGESLIDER_MIN_SPACING;
    }
    if (maxInput.value < parseInt(minInput.value) - RANGESLIDER_MIN_SPACING){
        maxInput.value = parseInt(minInput.value) + RANGESLIDER_MIN_SPACING;
    } else if (parseInt(minInput.value) === 0 && parseInt(maxInput.value) < RANGESLIDER_MIN_SPACING){
        maxInput.value = RANGESLIDER_MIN_SPACING;
    } else if (parseInt(maxInput.value) > RANGESLIDER_MAX_VALUE){
        maxInput.value = RANGESLIDER_MAX_VALUE;
    }
    slider.update({ to: +maxInput.value });
  });
});
