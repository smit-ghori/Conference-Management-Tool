/* --------------------------------------------------------------------------
   Conference Management Tool (CMT) - Client-side Script with Zero-Reload In-Place Filtering
   -------------------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', function() {

  // Mobile Hamburger Navigation Toggle
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const navLinksMenu = document.getElementById('navLinksMenu');
  const menuIcon = document.getElementById('menuIcon');

  if (mobileMenuBtn && navLinksMenu) {
    mobileMenuBtn.addEventListener('click', function() {
      navLinksMenu.classList.toggle('hidden');
      if (menuIcon) {
        if (navLinksMenu.classList.contains('hidden')) {
          menuIcon.classList.remove('fa-xmark');
          menuIcon.classList.add('fa-bars');
        } else {
          menuIcon.classList.remove('fa-bars');
          menuIcon.classList.add('fa-xmark');
        }
      }
    });
  }

  // Auto-dismiss alerts after 6 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease';
      setTimeout(function() {
        alert.remove();
      }, 500);
    }, 6000);
  });

  // --- Instant Zero-Reload Live Filter for Author Submissions ---
  const subSearchInput = document.getElementById('subSearchInput');
  const subDeptFilter = document.getElementById('subDeptFilter');
  const subStatusFilter = document.getElementById('subStatusFilter');
  const subTypeFilter = document.getElementById('subTypeFilter');
  const subTableRows = document.querySelectorAll('#submissionsTable tbody tr.sub-row');
  const noSubmissionsRow = document.getElementById('noSubmissionsRow');
  const subCountBadge = document.getElementById('subCountBadge');
  const resetSubFiltersBtn = document.getElementById('resetSubFiltersBtn');

  function filterSubmissionsLive() {
    const qTerm = subSearchInput ? subSearchInput.value.toLowerCase().trim() : '';
    const deptTerm = subDeptFilter ? subDeptFilter.value.toLowerCase() : '';
    const statusTerm = subStatusFilter ? subStatusFilter.value.toLowerCase() : '';
    const typeTerm = subTypeFilter ? subTypeFilter.value.toLowerCase() : '';

    let visibleCount = 0;

    subTableRows.forEach(row => {
      const abstractId = row.getAttribute('data-abstract') || '';
      const author = row.getAttribute('data-author') || '';
      const email = row.getAttribute('data-email') || '';
      const title = row.getAttribute('data-title') || '';
      const dept = row.getAttribute('data-dept') || '';
      const status = row.getAttribute('data-status') || '';
      const type = row.getAttribute('data-type') || '';
      const text = row.textContent.toLowerCase();

      const matchQ = !qTerm || abstractId.includes(qTerm) || author.includes(qTerm) || email.includes(qTerm) || title.includes(qTerm) || text.includes(qTerm);
      const matchDept = !deptTerm || dept.toLowerCase() === deptTerm;
      const matchStatus = !statusTerm || status.toLowerCase() === statusTerm;
      const matchType = !typeTerm || type.toLowerCase() === typeTerm;

      if (matchQ && matchDept && matchStatus && matchType) {
        row.style.display = '';
        visibleCount++;
      } else {
        row.style.display = 'none';
      }
    });

    if (subCountBadge) {
      subCountBadge.textContent = `Showing ${visibleCount} Submissions`;
    }

    if (noSubmissionsRow) {
      if (visibleCount === 0) {
        noSubmissionsRow.classList.remove('hidden');
      } else {
        noSubmissionsRow.classList.add('hidden');
      }
    }
  }

  if (subSearchInput) subSearchInput.addEventListener('input', filterSubmissionsLive);
  if (subDeptFilter) subDeptFilter.addEventListener('change', filterSubmissionsLive);
  if (subStatusFilter) subStatusFilter.addEventListener('change', filterSubmissionsLive);
  if (subTypeFilter) subTypeFilter.addEventListener('change', filterSubmissionsLive);

  if (resetSubFiltersBtn) {
    resetSubFiltersBtn.addEventListener('click', function() {
      if (subSearchInput) subSearchInput.value = '';
      if (subDeptFilter) subDeptFilter.value = '';
      if (subStatusFilter) subStatusFilter.value = '';
      if (subTypeFilter) subTypeFilter.value = '';
      filterSubmissionsLive();
    });
  }

  // Run initial live filter on page load
  filterSubmissionsLive();

  // --- Instant Zero-Reload Live Filter for Conferences Table ---
  const confSearchInput = document.getElementById('confSearchInput');
  const confStateFilter = document.getElementById('confStateFilter');
  const confDeptFilter = document.getElementById('confDeptFilter');
  const confTableRows = document.querySelectorAll('#conferencesTable tbody tr');
  const confCountBadge = document.getElementById('confCountBadge');
  const resetConfFiltersBtn = document.getElementById('resetConfFiltersBtn');

  function filterConferencesLive() {
    const qTerm = confSearchInput ? confSearchInput.value.toLowerCase().trim() : '';
    const stateTerm = confStateFilter ? confStateFilter.value.toLowerCase() : '';
    const deptTerm = confDeptFilter ? confDeptFilter.value.toLowerCase() : '';

    let visibleCount = 0;

    confTableRows.forEach(row => {
      const acronym = row.getAttribute('data-acronym') || '';
      const title = row.getAttribute('data-title') || '';
      const state = row.getAttribute('data-state') || '';
      const dept = row.getAttribute('data-dept') || '';
      const text = row.textContent.toLowerCase();

      const matchQ = !qTerm || acronym.includes(qTerm) || title.includes(qTerm) || text.includes(qTerm);
      const matchState = !stateTerm || state.toLowerCase() === stateTerm;
      const matchDept = !deptTerm || dept.toLowerCase() === deptTerm;

      if (matchQ && matchState && matchDept) {
        row.style.display = '';
        visibleCount++;
      } else {
        row.style.display = 'none';
      }
    });

    if (confCountBadge) {
      confCountBadge.textContent = `Showing ${visibleCount} Conferences`;
    }
  }

  if (confSearchInput) confSearchInput.addEventListener('input', filterConferencesLive);
  if (confStateFilter) confStateFilter.addEventListener('change', filterConferencesLive);
  if (confDeptFilter) confDeptFilter.addEventListener('change', filterConferencesLive);

  if (resetConfFiltersBtn) {
    resetConfFiltersBtn.addEventListener('click', function() {
      if (confSearchInput) confSearchInput.value = '';
      if (confStateFilter) confStateFilter.value = '';
      if (confDeptFilter) confDeptFilter.value = '';
      filterConferencesLive();
    });
  }

  // Run initial live filter for conferences on page load
  filterConferencesLive();

  // Payment tab switcher
  const payTabs = document.querySelectorAll('.pay-tab');
  const payContents = document.querySelectorAll('.pay-method-content');

  if (payTabs.length > 0) {
    payTabs.forEach(tab => {
      tab.addEventListener('click', function() {
        const target = this.getAttribute('data-target');

        payTabs.forEach(t => t.classList.remove('active'));
        payContents.forEach(c => c.style.display = 'none');

        this.classList.add('active');
        const activeContent = document.getElementById(target);
        if (activeContent) {
          activeContent.style.display = 'block';
        }
        
        const hiddenMethodInput = document.getElementById('selected_payment_method');
        if (hiddenMethodInput) {
          hiddenMethodInput.value = target;
        }
      });
    });
  }

  // Format currency display helper
  window.formatINR = function(amount) {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0
    }).format(amount);
  };

});
