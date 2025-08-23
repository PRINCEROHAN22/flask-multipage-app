// Bulletproof: animates even if "reduced motion" is set (we force it here)
document.addEventListener('DOMContentLoaded', () => {
  const items = Array.from(document.querySelectorAll('[data-reveal]'));
  if (!items.length) return;

  // Set initial style explicitly in case CSS didn’t load yet
  items.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(80px)';
    el.style.willChange = 'opacity, transform';
  });

  const reveal = (el) => {
    if (el.classList.contains('is-in')) return;
    // flip class next frame so initial styles are committed
    requestAnimationFrame(() => el.classList.add('is-in'));
  };

  const alreadyInView = (el) => {
    const r = el.getBoundingClientRect();
    return r.top < window.innerHeight * 0.9 && r.bottom > 0;
  };

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { reveal(e.target); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -10% 0px' });

    items.forEach(el => (alreadyInView(el) ? reveal(el) : io.observe(el)));
  } else {
    const tick = () => items.forEach(el => { if (alreadyInView(el)) reveal(el); });
    tick(); window.addEventListener('scroll', tick, { passive: true });
    window.addEventListener('resize', tick);
  }

  // Safety nudge in case nothing fired
  setTimeout(() => window.dispatchEvent(new Event('scroll')), 50);
});

document.addEventListener('DOMContentLoaded', () => {
  // ...existing code...
  const load = async () => { /* same as before */ };

  btn.addEventListener('click', load);
  load(); // <-- fetch one on first load
});
