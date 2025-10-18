function scrollCars(direction, categoryId) {
  const slider = document.querySelector(`#${categoryId}-slider .car-slider`);
  const cardWidth = slider.querySelector('.car-view').offsetWidth + 25;
  slider.scrollBy({ left: direction === 'left' ? -cardWidth : cardWidth, behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', () => {
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
});
