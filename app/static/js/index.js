function scrollCars(direction, categoryId) {
  const slider = document.querySelector(`#${categoryId}-slider .car-slider`);
  const cardWidth = slider.querySelector('.car-view').offsetWidth + 25;
  slider.scrollBy({ left: direction === 'left' ? -cardWidth : cardWidth, behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', async () => {
  document.body.classList.add('loading');

  try {
    const response = await fetch('/api/stats');
    const data = await response.json();

    if (data.status === 'success') {
      const statsMap = {
        clients: data.clients,
        contracts: data.contracts,
        cars: data.cars,
        new: data.new
      };

      document.querySelectorAll('.statistic-value').forEach(el => {
        const title = el.parentElement.querySelector('.statistic-title').textContent;
        if (title.includes('clients served')) el.dataset.target = statsMap.clients;
        if (title.includes('active contracts')) el.dataset.target = statsMap.contracts;
        if (title.includes('cars in fleet')) el.dataset.target = statsMap.cars;
        if (title.includes('new clients')) el.dataset.target = statsMap.new;
      });
    }

    const stats = document.querySelectorAll('.statistic');
    const animateStatistic = el => {
      const counter = el.querySelector('.statistic-value');
      const target = parseInt(counter.dataset.target || 0, 10);
      const duration = parseInt(counter.dataset.duration || 2000, 10);
      let value = 0;
      const stepTime = 10;
      const increment = target / (duration / stepTime);
      const timer = setInterval(() => {
        value += increment;
        if (value >= target) {
          value = target;
          clearInterval(timer);
        }
        counter.textContent = Math.floor(value);
      }, stepTime);
    };

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;
          if (!el.classList.contains('visible')) {
            el.classList.add('visible');
            animateStatistic(el);
          }
        }
      });
    }, { threshold: 0.5 });

    stats.forEach(s => observer.observe(s));

  } catch (err) {
    console.error('Failed to load statistics:', err);
  } finally {
    document.body.classList.remove('loading');
  }
});
document.addEventListener('DOMContentLoaded', () => {
  const reviews = document.querySelector('#reviews');
  const cards = Array.from(reviews.children);

  reviews.innerHTML += reviews.innerHTML;

  let scrollPos = 0;
  const speed = 0.3;

  function smoothScroll() {
    scrollPos += speed;
    if (scrollPos >= reviews.scrollWidth / 2) scrollPos = 0;
    reviews.scrollLeft = scrollPos;
    requestAnimationFrame(smoothScroll);
  }

  smoothScroll();
});
