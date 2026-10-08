// Resize charts after hidden pages/filters become visible. No data or network writes.
document.addEventListener('DOMContentLoaded', function () {
  let pending;
  function resize() {
    clearTimeout(pending);
    pending = setTimeout(() => window.dispatchEvent(new Event('resize')), 120);
  }
  new MutationObserver(function (changes) {
    if (changes.some(change => change.target.id && change.target.id.startsWith('page-'))) resize();
  }).observe(document.body, {subtree: true, attributes: true, attributeFilter: ['style']});
  document.addEventListener('toggle', resize, true);
});
