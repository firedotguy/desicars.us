const RANGESLIDER_MIN_SPACING = 20;
const RANGESLIDER_MIN_VALUE = 0;
const RANGESLIDER_MAX_VALUE = 1000;

// filter show/hide
document.addEventListener("DOMContentLoaded", () => {
  const filters = document.querySelectorAll(".filter");
  // Keep a reference to the price slider instance (vanilla-rangeslider)
  let priceSlider = null;

  filters.forEach((filter) => {
    const dropdown = filter.querySelector(".filter-dropdown");

    filter.addEventListener("mousedown", (e) => {
      e.stopPropagation();
      document.querySelectorAll(".filter.active").forEach((f) => {
        if (f !== filter) f.classList.remove("active");
      });
      filter.classList.toggle("active");

      // If opening Price dropdown, sync slider from inputs (empty -> 0)
      if (filter.id === 'filter-price' && filter.classList.contains('active')) {
        const minInput = document.getElementById('filter-price-min-input');
        const maxInput = document.getElementById('filter-price-max-input');
        if (minInput && maxInput && priceSlider && typeof priceSlider.update === 'function') {
          if (minInput.value === '') minInput.value = '0';
          if (maxInput.value === '') maxInput.value = '0';
          priceSlider.update({ from: +minInput.value, to: +maxInput.value });
        }
      }
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

  // defaults mean: no price filter
  const DEFAULT_MIN = RANGESLIDER_MIN_VALUE;
  const DEFAULT_MAX = RANGESLIDER_MAX_VALUE;

  const slider = ionRangeSlider(sliderInput, {
    type: "double",
    min: DEFAULT_MIN,
    max: DEFAULT_MAX,
    from: +minInput.value || DEFAULT_MIN,
    to: +maxInput.value || DEFAULT_MAX,
    step: 5,
    onChange: (data) => {
        minInput.value = data.from;
        maxInput.value = data.to;
        if (minInput.value == maxInput.value){
            minInput.value -= RANGESLIDER_MIN_SPACING;
        }
        if (minInput.value > parseInt(maxInput.value) + RANGESLIDER_MIN_SPACING){
            minInput.value = parseInt(maxInput.value) - RANGESLIDER_MIN_SPACING;
        } else if (parseInt(maxInput.value) === DEFAULT_MAX && parseInt(minInput.value) > DEFAULT_MAX - RANGESLIDER_MIN_SPACING) {
            minInput.value = DEFAULT_MAX - RANGESLIDER_MIN_SPACING;
        }
        if (maxInput.value < parseInt(minInput.value) - RANGESLIDER_MIN_SPACING){
        maxInput.value = parseInt(minInput.value) + RANGESLIDER_MIN_SPACING;
        } else if (parseInt(minInput.value) === DEFAULT_MIN && parseInt(maxInput.value) < RANGESLIDER_MIN_SPACING){
            maxInput.value = RANGESLIDER_MIN_SPACING;
        }
    }
  });
  priceSlider = slider;

  minInput.addEventListener("change", () => {
    minInput.value = minInput.value.replace(/\D/g, '');
    if (minInput.value === ''){
        minInput.value = DEFAULT_MIN;
    }
    if (minInput.value == maxInput.value){
        minInput.value -= RANGESLIDER_MIN_SPACING;
    }
    if (minInput.value > parseInt(maxInput.value) + RANGESLIDER_MIN_SPACING){
        minInput.value = parseInt(maxInput.value) - RANGESLIDER_MIN_SPACING;
    } else if (parseInt(maxInput.value) === DEFAULT_MAX && parseInt(minInput.value) > DEFAULT_MAX - RANGESLIDER_MIN_SPACING) {
        minInput.value = DEFAULT_MAX - RANGESLIDER_MIN_SPACING;
    }
    slider.update({ from: +minInput.value });
  });
  maxInput.addEventListener("change", () => {
    maxInput.value = maxInput.value.replace(/\D/g, '');
    if (maxInput.value === ''){
        maxInput.value = DEFAULT_MIN;
    }
    if (minInput.value == maxInput.value){
        maxInput.value = parseInt(maxInput.value) + RANGESLIDER_MIN_SPACING;
    }
    if (maxInput.value < parseInt(minInput.value) - RANGESLIDER_MIN_SPACING){
        maxInput.value = parseInt(minInput.value) + RANGESLIDER_MIN_SPACING;
    } else if (parseInt(minInput.value) === DEFAULT_MIN && parseInt(maxInput.value) < RANGESLIDER_MIN_SPACING){
        maxInput.value = RANGESLIDER_MIN_SPACING;
    } else if (parseInt(maxInput.value) > DEFAULT_MAX){
        maxInput.value = DEFAULT_MAX;
    }
    slider.update({ to: +maxInput.value });
  });
});


// filters -> URL -> API sync
document.addEventListener("DOMContentLoaded", () => {
  const listEl = document.getElementById("cars-list");
  const DEFAULT_MIN = RANGESLIDER_MIN_VALUE;
  const DEFAULT_MAX = RANGESLIDER_MAX_VALUE;
  let firstLoad = true;

  const getParams = () => new URLSearchParams(window.location.search);
  const setParam = (key, value) => {
    const params = getParams();
    if (value === null || value === undefined || value === "") params.delete(key);
    else params.set(key, value);
    const url = `${window.location.pathname}?${params.toString()}`;
    history.pushState({}, "", url);
    toggleCancelButtons(params);
    loadCars(params);
  };

  const toggleCancelButtons = (params) => {
    const typeCancel = document.querySelector("#filter-type .filter-cancel");
    const makeCancel = document.querySelector("#filter-make .filter-cancel");
    const priceCancel = document.querySelector("#filter-price .filter-cancel");
    if (typeCancel) typeCancel.style.display = params.has("type") ? "inline" : "none";
    if (makeCancel) makeCancel.style.display = params.has("make") ? "inline" : "none";
    const min = parseInt(params.get('price_min') || `${DEFAULT_MIN}`);
    const max = parseInt(params.get('price_max') || `${DEFAULT_MAX}`);
    if (priceCancel) priceCancel.style.display = (min === DEFAULT_MIN && max === DEFAULT_MAX) ? 'none' : 'inline';
  };

  const renderCars = (cars) => {
    if (!listEl) return;
    if (!cars || !cars.length) {
      listEl.innerHTML = '<div id="cars-not-found">No cars found</div>';
      return;
    }
    const html = cars
      .map((c) => {
        const title = (c.vehicle && (c.vehicle.name || `${c.vehicle.make || ''} ${c.vehicle.model || ''}`.trim())) || c.nickname;
        const price = c.price != null ? `$${c.price}` : "";
        const year = c.vehicle && c.vehicle.year ? c.vehicle.year : "";
        return `<div class="car-item"><div class="car-title">${title}</div><div class="car-meta">${year} ${price}</div></div>`;
      })
      .join("");
    listEl.innerHTML = html;
  };

  const updateCurrentClasses = (params) => {
    // Sort
    document.querySelectorAll('.filter-dropdown-item[data-sort]').forEach((a) => {
      a.classList.remove('filter-dropdown-item-current');
    });
    const sort = params.get('sort') || 'model';
    const currentSortEl = document.querySelector(`.filter-dropdown-item[data-sort="${sort}"]`);
    if (currentSortEl) currentSortEl.classList.add('filter-dropdown-item-current');

    // Type
    document.querySelectorAll('.filter-dropdown-item[data-type]').forEach((a) => a.classList.remove('filter-dropdown-item-current'));
    const type = params.get('type');
    if (type) {
      const currentTypeEl = document.querySelector(`.filter-dropdown-item[data-type="${type}"]`);
      if (currentTypeEl) currentTypeEl.classList.add('filter-dropdown-item-current');
    }

    // Make
    document.querySelectorAll('.filter-dropdown-item[data-make]').forEach((a) => a.classList.remove('filter-dropdown-item-current'));
    const make = params.get('make');
    if (make) {
      const currentMakeEl = document.querySelector(`.filter-dropdown-item[data-make="${make}"]`);
      if (currentMakeEl) currentMakeEl.classList.add('filter-dropdown-item-current');
    }
  };

  const setLoaderVisible = (visible) => {
    document.body.classList.toggle('loading', !!visible);
    const el = document.getElementById('loader');
    if (el) el.style.display = visible ? 'flex' : 'none';
  };

  const inlineLoader = document.getElementById('inline-loader');

const showInlineLoader = () => {
  if (inlineLoader) inlineLoader.hidden = false;
  if (listEl) listEl.innerHTML = '';
};
const hideInlineLoader = () => {
  if (inlineLoader) inlineLoader.hidden = true;
};

  const loadCars = (params = getParams()) => {
    const p = new URLSearchParams(params);
    if (!p.has('active')) p.set('active', 'false');
    const qs = p.toString();

    if (firstLoad) {
      setLoaderVisible(true);
    } else {
      showInlineLoader();
    }
    fetch(`/api/cars${qs ? `?${qs}` : ""}`)
      .then((r) => r.json())
      .then((data) => renderCars(data))
      .catch(() => {
        if (listEl) listEl.innerHTML = '<div id="cars-error">Failed to load cars</div>';
      })
      .finally(() => {
        if (firstLoad) {
          setLoaderVisible(false);
          firstLoad = false;
        } else {
          hideInlineLoader();
        }
      });
  };


  // Sync price UI from URL params on load/popstate
  const syncPriceUIFromParams = (params) => {
    const min = parseInt(params.get('price_min') || `${DEFAULT_MIN}`);
    const max = parseInt(params.get('price_max') || `${DEFAULT_MAX}`);
    const minInput = document.getElementById("filter-price-min-input");
    const maxInput = document.getElementById("filter-price-max-input");
    const sliderInput = document.getElementById("filter-price-slider");
    if (minInput) minInput.value = `${min}`;
    if (maxInput) maxInput.value = `${max}`;
    if (priceSlider && typeof priceSlider.update === 'function') { priceSlider.update({ from: min, to: max }); }
  };

  // Click handlers for dropdown items
  const priceApplyBtn = document.getElementById('filter-price-button');
  if (priceApplyBtn) {
    priceApplyBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const params = getParams();
      const min = parseInt(document.getElementById('filter-price-min-input').value || `${DEFAULT_MIN}`);
      const max = parseInt(document.getElementById('filter-price-max-input').value || `${DEFAULT_MAX}`);
      if (min === DEFAULT_MIN && max === DEFAULT_MAX) {
        params.delete('price_min');
        params.delete('price_max');
      } else {
        params.set('price_min', String(min));
        params.set('price_max', String(max));
      }
      history.pushState({}, '', `${window.location.pathname}?${params.toString()}`);
      toggleCancelButtons(params);
      syncPriceUIFromParams(params);
      loadCars(params);
    });
  }
  document.querySelectorAll('.filter-dropdown-item[data-sort]').forEach((a) => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      setParam('sort', a.dataset.sort);
      updateCurrentClasses(getParams());
    });
  });
  document.querySelectorAll('.filter-dropdown-item[data-type]').forEach((a) => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      setParam('type', a.dataset.type);
      updateCurrentClasses(getParams());
    });
  });
  document.querySelectorAll('.filter-dropdown-item[data-make]').forEach((a) => {
    a.addEventListener('click', (e) => {
      e.preventDefault();
      setParam('make', a.dataset.make);
      updateCurrentClasses(getParams());
    });
  });

  // Cancel buttons to clear filters
  const typeCancel = document.querySelector("#filter-type .filter-cancel");
  if (typeCancel) typeCancel.addEventListener('click', (e) => {
    e.preventDefault();
    setParam('type', null);
    updateCurrentClasses(getParams());
  });
  const makeCancel = document.querySelector("#filter-make .filter-cancel");
  if (makeCancel) makeCancel.addEventListener('click', (e) => {
    e.preventDefault();
    setParam('make', null);
    updateCurrentClasses(getParams());
  });
  const priceCancel = document.querySelector("#filter-price .filter-cancel");
  if (priceCancel) priceCancel.addEventListener('click', (e) => {
    e.preventDefault();
    const params = getParams();
    params.delete('price_min');
    params.delete('price_max');
    history.pushState({}, '', `${window.location.pathname}?${params.toString()}`);
    // Reset inputs and slider to defaults explicitly
    const minInputEl = document.getElementById('filter-price-min-input');
    const maxInputEl = document.getElementById('filter-price-max-input');
    if (minInputEl) minInputEl.value = `${DEFAULT_MIN}`;
    if (maxInputEl) maxInputEl.value = `${DEFAULT_MAX}`;
    if (priceSlider && typeof priceSlider.update === 'function') {
      priceSlider.update({ from: DEFAULT_MIN, to: DEFAULT_MAX });
    }
    syncPriceUIFromParams(params);
    toggleCancelButtons(params);
    updateCurrentClasses(params);
    loadCars(params);
  });

  // Initial state sync
  toggleCancelButtons(getParams());
  updateCurrentClasses(getParams());
  syncPriceUIFromParams(getParams());
  // Fetch initial list on load
  loadCars(getParams());

  window.addEventListener('popstate', () => {
    toggleCancelButtons(getParams());
    updateCurrentClasses(getParams());
    syncPriceUIFromParams(getParams());
    loadCars(getParams());
  });
});

