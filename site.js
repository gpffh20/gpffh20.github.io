const dialog = document.querySelector('#image-dialog');
if (dialog) {
  const target = dialog.querySelector('img');
  document.querySelectorAll('[data-enlarge]').forEach(button => {
    button.addEventListener('click', () => {
      const source = button.querySelector('img');
      target.src = source.src;
      target.alt = source.alt;
      dialog.showModal();
      dialog.scrollTop = 0;
    });
  });
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  }});
}
const sections = [...document.querySelectorAll('main section[id]')];
const links = [...document.querySelectorAll('.main-nav a[href^="#"], .article-nav a[href^="#"]')];
if ('IntersectionObserver' in window && links.length) {
  const observer = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting).sort((a,b) => a.boundingClientRect.top-b.boundingClientRect.top);
    if (!visible.length) return;
    const sectionId = visible[0].target.id;
    const activeId = ['network', 'scaling', 'chatops', 'delivery'].includes(sectionId) ? 'cases' : sectionId;
    links.forEach(link => {
      if (link.hash === '#' + activeId) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, {rootMargin:'-15% 0px -55% 0px',threshold:0});
  sections.forEach(section => observer.observe(section));
}
