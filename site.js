function setLang(l) {
  var de = l === 'de';
  document.querySelectorAll('.lang-de').forEach(function (e) { e.hidden = !de; });
  document.querySelectorAll('.lang-en').forEach(function (e) { e.hidden = de; });
  var bde = document.getElementById('b-de'), ben = document.getElementById('b-en');
  if (bde) bde.setAttribute('aria-pressed', de);
  if (ben) ben.setAttribute('aria-pressed', !de);
  document.documentElement.lang = l;
  document.body.dataset.lang = l;
}
document.addEventListener('DOMContentLoaded', function () {
  var de = (navigator.language || '').toLowerCase().indexOf('de') === 0;
  setLang(de ? 'de' : 'en');
});
