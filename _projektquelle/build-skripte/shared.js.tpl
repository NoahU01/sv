// ---- Mobile nav ----
(function(){
  var burger = document.getElementById('burgerBtn');
  var nav = document.getElementById('mainNav');
  if (burger && nav) {
    burger.addEventListener('click', function(){ nav.classList.toggle('open'); });
    nav.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){ nav.classList.remove('open'); });
    });
  }
})();

// ---- Scroll reveal ----
(function(){
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { els.forEach(function(e){ e.classList.add('visible'); }); return; }
  var obs = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if (entry.isIntersecting) { entry.target.classList.add('visible'); obs.unobserve(entry.target); }
    });
  }, { threshold: 0.12 });
  els.forEach(function(e){ obs.observe(e); });
})();

// ---- Accordion ----
function initAccordions(root){
  (root || document).querySelectorAll('.accordion-item').forEach(function(item){
    var trigger = item.querySelector('.accordion-trigger');
    var panel = item.querySelector('.accordion-panel');
    if (!trigger || !panel) return;
    trigger.addEventListener('click', function(){
      var isOpen = item.classList.contains('open');
      item.closest('.accordion').querySelectorAll('.accordion-item').forEach(function(other){
        other.classList.remove('open');
        other.querySelector('.accordion-panel').style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add('open');
        panel.style.maxHeight = panel.scrollHeight + 40 + 'px';
      }
    });
  });
}
document.addEventListener('DOMContentLoaded', function(){ initAccordions(document); });

// ---- Modal helpers ----
function openModal(id){
  var m = document.getElementById(id);
  if (!m) return;
  m.classList.add('active');
  document.body.style.overflow = 'hidden';
}
function closeModal(id){
  var m = document.getElementById(id);
  if (!m) return;
  m.classList.remove('active');
  document.body.style.overflow = '';
}
document.addEventListener('click', function(e){
  if (e.target.classList && e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('active');
    document.body.style.overflow = '';
  }
});
document.addEventListener('keydown', function(e){
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active').forEach(function(m){ m.classList.remove('active'); });
    document.body.style.overflow = '';
  }
});

var LEGAL_TEXT = {
  impressum: '<h3>Impressum</h3><p class="small muted">Dies ist ein nicht-produktives Strategie-Mock-up der SV Akademie und dient ausschließlich der internen Visualisierung im Rahmen der Strategieentwicklung. Es handelt sich nicht um eine live geschaltete, öffentlich erreichbare Website. Ein rechtsgültiges Impressum wird im Zuge einer tatsächlichen Veröffentlichung ergänzt.</p>',
  datenschutz: '<h3>Datenschutz</h3><p class="small muted">Da dieses Dokument lokal als Mock-up betrachtet wird und keine Formulardaten tatsächlich übertragen oder gespeichert werden, sind an dieser Stelle keine Datenschutzhinweise wirksam. Für die spätere Live-Version ist eine vollständige, DSGVO-konforme Datenschutzerklärung zu ergänzen.</p>'
};
function openLegalModal(type){
  var el = document.getElementById('legalModalContent');
  if (el) el.innerHTML = LEGAL_TEXT[type] || '';
  openModal('legalModal');
}

// ---- Generic mock form submit ----
function mockSubmit(formEl, modalId){
  if (!formEl) return;
  formEl.addEventListener('submit', function(e){
    e.preventDefault();
    openModal(modalId);
    formEl.reset();
  });
}

// ---- Download helper (Blob) ----
function downloadDataUri(dataUri, filename){
  var a = document.createElement('a');
  a.href = dataUri;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// ---- ICS calendar generator ----
function downloadIcs(opts){
  var dt = opts.start; // Date object
  function fmt(d){
    return d.getUTCFullYear() + pad(d.getUTCMonth()+1) + pad(d.getUTCDate()) + 'T' + pad(d.getUTCHours()) + pad(d.getUTCMinutes()) + '00Z';
  }
  function pad(n){ return n < 10 ? '0'+n : ''+n; }
  var end = new Date(dt.getTime() + (opts.durationMinutes||60)*60000);
  var ics = [
    'BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//SV Akademie//Mockup//DE','CALSCALE:GREGORIAN',
    'BEGIN:VEVENT',
    'UID:' + Date.now() + '@sv-akademie.mockup',
    'DTSTAMP:' + fmt(new Date()),
    'DTSTART:' + fmt(dt),
    'DTEND:' + fmt(end),
    'SUMMARY:' + (opts.title||'SV Akademie Termin'),
    'DESCRIPTION:' + (opts.description||'').replace(/\\n/g,'\\\\n'),
    'LOCATION:' + (opts.location||'Online'),
    'END:VEVENT','END:VCALENDAR'
  ].join('\r\n');
  var blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
  var url = URL.createObjectURL(blob);
  downloadDataUri(url, (opts.filename||'termin') + '.ics');
  setTimeout(function(){ URL.revokeObjectURL(url); }, 4000);
}
