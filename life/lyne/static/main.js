// ========== LifeLyne – film-strip slider + help tabs ==========
document.addEventListener("DOMContentLoaded", () => {
    // -------- 1) HOME FILM-STRIP SLIDER --------
    const track = document.querySelector(".slider-track");

    if (track) {
        // Get all images that are already in HTML
        const imgs = Array.from(track.querySelectorAll("img"));

        if (imgs.length > 0) {
            // Shuffle images (Fisher–Yates)
            for (let i = imgs.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [imgs[i], imgs[j]] = [imgs[j], imgs[i]];
            }

            // Clear track and append shuffled images once
            track.innerHTML = "";
            imgs.forEach(img => track.appendChild(img));

            // Append one more copy for smooth infinite scroll
            imgs.forEach(img => {
                const clone = img.cloneNode(true);
                track.appendChild(clone);
            });

            // CSS animation lifelyneScroll will now
            // move through 2x images and loop with no gap
        }
    }

    
    // -------- 2) HELP PAGE TABS --------
    const tabButtons = document.querySelectorAll(".help-tab-button");
    const panels = document.querySelectorAll(".help-panel");

    if (tabButtons.length > 0 && panels.length > 0) {
        tabButtons.forEach((btn) => {
            btn.addEventListener("click", () => {
                const tabName = btn.getAttribute("data-tab");
                if (!tabName) return;

                tabButtons.forEach((b) => b.classList.remove("active"));
                btn.classList.add("active");

                panels.forEach((panel) => {
                    panel.classList.toggle(
                        "active",
                        panel.id === `tab-${tabName}`
                    );
                });
            });
        });
    }
});




// floating profile toggle
const floatBtn = document.querySelector('.floating-profile');
const floatPanel = document.querySelector('.floating-panel');

if (floatBtn && floatPanel) {
    floatBtn.addEventListener('click', () => {
        floatPanel.classList.toggle('active');
    });

    // click-outside to close
    document.addEventListener('click', (e) => {
        if (!floatPanel.contains(e.target) && !floatBtn.contains(e.target)) {
            floatPanel.classList.remove('active');
        }
    });
}


document.addEventListener('DOMContentLoaded', ()=> {

  // quick modal for avatar
  const topAvatar = document.getElementById('topAvatar');
  const modal = document.getElementById('profileQuickModal');
  const closeQuick = document.getElementById('closeQuick');
  const quickInner = document.getElementById('quickInner');

  if(topAvatar) {
    topAvatar.addEventListener('click', ()=> {
      modal.classList.add('show');
      // demo content — replace with fetch/ajax later
      quickInner.innerHTML = `
        <div style="display:flex;gap:14px;align-items:center">
          <img src="${topAvatar.src}" style="width:120px;height:120px;border-radius:10px;object-fit:cover">
          <div>
            <div style="font-weight:800;font-size:18px">Demo Profile</div>
            <div style="color:#C7D2DE;margin-top:6px">24 • Hyderabad • Software Engineer</div>
            <p style="margin-top:10px;color:#DCEFFB">This is a quick view. Click 'View profile' to open full page.</p>
            <div style="margin-top:10px"><a class="btn-sm" href="/profile/1/">View profile</a></div>
          </div>
        </div>
      `;
    });
  }
  if(closeQuick) closeQuick.addEventListener('click', ()=> modal.classList.remove('show'));

  // filters (demo) — just filter by data-match attribute
  document.querySelectorAll('[data-filter]').forEach(btn=>{
    btn.addEventListener('click', ()=> {
      const key = btn.getAttribute('data-filter');
      const all = document.querySelectorAll('#matchesGrid .match-card');
      all.forEach(card=>{
        if(key === 'all') card.style.display = '';
        else if(key === 'high') {
          const val = parseInt(card.getAttribute('data-match')||0,10);
          card.style.display = val >= 80 ? '' : 'none';
        } else if(key === 'near') {
          // demo: show all for now
          card.style.display = '';
        }
      });
    });
  });

  // view toggle compact/detailed (demo)
  const vt = document.getElementById('viewToggle');
  if(vt){
    vt.addEventListener('click', ()=>{
      const grid = document.getElementById('matchesGrid');
      if(grid.classList.toggle('compact')) vt.textContent = grid.classList.contains('compact') ? 'Detailed view' : 'Compact view';
    });
  }

  // mouse tilt on match cards (subtle)
  document.querySelectorAll('.match-card').forEach(card=>{
    card.addEventListener('mousemove', e=>{
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      const rotateY = x * 6;
      const rotateX = -y * 6;
      card.style.transform = `perspective(900px) translateZ(6px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
    });
    card.addEventListener('mouseleave', ()=> {
      card.style.transform = '';
    });
  });

});


// === Profile click fallback & avatar modal (safe) ===
document.addEventListener('DOMContentLoaded', () => {
  // 1) Universal handler for view-profile elements
  document.querySelectorAll('[data-profile-id], .view-profile, .view-profile-btn').forEach(el => {
    el.addEventListener('click', (ev) => {
      // if element is an <a href="...">, let default behavior happen
      if (el.tagName.toLowerCase() === 'a' && el.getAttribute('href')) return;

      // try data-profile-id attribute
      const id = el.getAttribute('data-profile-id') || el.dataset.profileId;
      if (id) {
        // navigate to profile url (non-namespaced)
        const url = `/profile/${id}/`;
        window.location.href = url;
        return;
      }

      // if there's an onclick attribute already that uses location.href, let it run
      const onclick = el.getAttribute('onclick');
      if (onclick && onclick.includes('location.href')) {
        // allow default
        return;
      }

      // fallback: find an <a> inside the card
      const anchor = el.closest('.match-card')?.querySelector('a[href]');
      if (anchor && anchor.getAttribute('href')) {
        window.location.href = anchor.getAttribute('href');
        return;
      }

      // else show a tiny message (dev)
      console.warn('No profile id found on element', el);
    });
  });

  // 2) top avatar quick modal fallback (if not present)
  const topAvatar = document.getElementById('topAvatar');
  const modal = document.getElementById('profileQuickModal');
  const closeQuick = document.getElementById('closeQuick');

  if (topAvatar && modal) {
    topAvatar.addEventListener('click', () => {
      modal.classList.add('show');
      // If quickInner exists fill with demo content if empty
      const quickInner = document.getElementById('quickInner');
      if (quickInner && quickInner.innerHTML.trim() === '') {
        quickInner.innerHTML = `
          <div style="display:flex;gap:12px;align-items:center">
            <img src="${topAvatar.src}" style="width:120px;height:120px;object-fit:cover;border-radius:10px;">
            <div>
              <div style="font-weight:700">Your profile</div>
              <div class="muted">Click view to open full profile</div>
              <div style="margin-top:10px"><a href="/profile/1/" class="btn-sm">View profile</a></div>
            </div>
          </div>
        `;
      }
    });
    if (closeQuick) closeQuick.addEventListener('click', () => modal.classList.remove('show'));
  }
});



// dashboard.js - improved search + actions
(function(){

  window.shortlist = function(id, btn){
    if(btn){ btn.disabled = true; btn.textContent = "Shortlisted ✓"; }
    // TODO: add fetch() POST to persist on server
  };

  window.sendInterest = function(id){
    alert('Interest sent (demo) to profile ' + id);
  };

  document.addEventListener('DOMContentLoaded', function(){
    const applyBtn = document.getElementById('applyFilters');
    const searchInput = document.getElementById('searchInput');
    const selHeight = document.getElementById('filterHeight');
    const selCity = document.getElementById('filterCity');
    const selJob = document.getElementById('filterJob');
    const grid = document.getElementById('matchesGrid');

    function runFilter(){
      const q = (searchInput && searchInput.value || '').trim().toLowerCase();
      const fHeight = (selHeight && selHeight.value || '').trim().toLowerCase();
      const fCity = (selCity && selCity.value || '').trim().toLowerCase();
      const fJob = (selJob && selJob.value || '').trim().toLowerCase();

      if(!grid) return;
      Array.from(grid.children).forEach(card => {
        const prof = (card.dataset.profession || '').toLowerCase();
        const loc = (card.dataset.location || '').toLowerCase();
        const preferred = (card.dataset.preferred || '').toLowerCase();
        const text = (card.innerText || '').toLowerCase();

        const matchesQuery = !q || text.indexOf(q) !== -1 || prof.indexOf(q) !== -1 || loc.indexOf(q) !== -1 || preferred.indexOf(q) !== -1;
        const matchesHeight = !fHeight || (card.dataset.age && card.dataset.age.indexOf(fHeight) !== -1) || (card.dataset.preferred && card.dataset.preferred.indexOf(fHeight) !== -1);
        const matchesCity = !fCity || loc.indexOf(fCity) !== -1;
        const matchesJob  = !fJob  || prof.indexOf(fJob) !== -1;

        const show = matchesQuery && matchesHeight && matchesCity && matchesJob;
        card.style.display = show ? '' : 'none';
      });
    }

    if(applyBtn) applyBtn.addEventListener('click', runFilter);
    if(searchInput) searchInput.addEventListener('keydown', function(e){
      if(e.key === 'Enter'){ e.preventDefault(); runFilter(); }
    });
  });
})();

