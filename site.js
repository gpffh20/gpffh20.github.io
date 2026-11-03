const tabs = [...document.querySelectorAll('[role="tab"]')];
if (tabs.length) {
  const selectTab = (selected, updateUrl = false) => {
    tabs.forEach(tab => {
      const active = tab === selected;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
    });
    if (updateUrl) history.replaceState(null, '', '#' + selected.getAttribute('aria-controls'));
  };
  const selectFromHash = () => {
    const target = document.getElementById(location.hash.slice(1));
    const panel = target?.closest('[role="tabpanel"]');
    const tab = panel && tabs.find(item => item.getAttribute('aria-controls') === panel.id);
    if (tab) selectTab(tab);
    return Boolean(tab);
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab, true));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
      if (event.key === 'ArrowLeft') next = tabs[(index - 1 + tabs.length) % tabs.length];
      if (event.key === 'Home') next = tabs[0];
      if (event.key === 'End') next = tabs[tabs.length - 1];
      if (!next) return;
      event.preventDefault();
      selectTab(next, true);
      next.focus();
    });
  });
  if (!selectFromHash()) selectTab(tabs[0]);
  addEventListener('hashchange', selectFromHash);
}

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
    links.forEach(link => {
      if (link.hash === '#' + visible[0].target.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, {rootMargin:'-15% 0px -55% 0px',threshold:0});
  sections.forEach(section => observer.observe(section));
}
