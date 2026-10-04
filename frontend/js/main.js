document.addEventListener("DOMContentLoaded", () => {
  const theftTypeSelect = document.getElementById("theft_type");
  const walletSection = document.getElementById("wallet-section");
  const mobileSection = document.getElementById("mobile-section");
  const theftForm = document.getElementById("theft-form");
  const resultCard = document.getElementById("result-card");
  const caseIdDisplay = document.getElementById("case-id-display");
  const riskBadges = document.getElementById("risk-badges");
  const checklistContainer = document.getElementById("checklist-container");
  const complaintDraftText = document.getElementById("complaint-draft-text");

  let currentGeneratedCaseId = "";

  if (theftTypeSelect) {
    theftTypeSelect.addEventListener("change", (e) => {
      const val = e.target.value;
      if (val === "wallet") {
        walletSection.classList.remove("hidden");
        mobileSection.classList.add("hidden");
      } else if (val === "mobile") {
        walletSection.classList.add("hidden");
        mobileSection.classList.remove("hidden");
      } else {
        walletSection.classList.remove("hidden");
        mobileSection.classList.remove("hidden");
      }
    });
  }

  if (theftForm) {
    theftForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const theftType = theftTypeSelect.value;
      const payload = {
        user_name: document.getElementById("user_name").value,
        incident_location: document.getElementById("incident_location").value,
        incident_date: document.getElementById("incident_date").value,
        description: document.getElementById("description").value,
        theft_type: theftType,
        wallet_details: {
          has_aadhaar: document.getElementById("has_aadhaar")?.checked || false,
          has_pan: document.getElementById("has_pan")?.checked || false,
          has_driving_licence: document.getElementById("has_dl")?.checked || false,
          has_voter_id: document.getElementById("has_voter")?.checked || false,
          has_debit_card: document.getElementById("has_debit")?.checked || false,
          has_credit_card: document.getElementById("has_credit")?.checked || false,
          has_cash: false,
          other_documents: []
        },
        mobile_details: {
          device_type: document.getElementById("device_type")?.value || "Android",
          sim_present: document.getElementById("sim_present")?.checked || false,
          has_banking_apps: document.getElementById("has_banking_apps")?.checked || false,
          has_upi: document.getElementById("has_upi")?.checked || false,
          has_email_access: true,
          tracking_enabled: true
        }
      };

      try {
        const response = await fetch("/api/v1/cases/report", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Failed to create case");

        const data = await response.json();
        currentGeneratedCaseId = data.case_id;
        renderCaseResults(data);
      } catch (err) {
        alert("Error submitting case: " + err.message);
      }
    });
  }

  function renderCaseResults(data) {
    document.getElementById("form-card").classList.add("hidden");
    resultCard.classList.remove("hidden");

    caseIdDisplay.innerText = data.case_id;

    const risk = data.risk_assessment;
    riskBadges.innerHTML = `
      <span class="badge badge-${risk.financial_risk}">Financial Risk: ${risk.financial_risk}</span>
      <span class="badge badge-${risk.identity_risk}">Identity Risk: ${risk.identity_risk}</span>
      <span class="badge badge-${risk.digital_risk}">Digital Risk: ${risk.digital_risk}</span>
    `;

    checklistContainer.innerHTML = "";
    data.checklist.forEach((task, index) => {
      const item = document.createElement("div");
      item.className = "checklist-card";

      let actionModuleHTML = getActionModuleForTask(task.category, task.title);

      item.innerHTML = `
        <div class="checklist-header">
          <div class="task-title-group">
            <span class="step-number">Step ${index + 1}</span>
            <div>
              <h3>[${task.category}] ${task.title}</h3>
              <p class="task-instruction">${task.instructions}</p>
            </div>
          </div>
          <span class="badge badge-${task.priority}">${task.priority}</span>
        </div>
        ${actionModuleHTML}
      `;
      checklistContainer.appendChild(item);
    });

    fetchComplaintDraft(data.case_id);
  }

  function getActionModuleForTask(category, title) {
    const cat = category.toLowerCase();
    const t = title.toLowerCase();

    if (cat.includes("banking") || t.includes("bank") || t.includes("card") || t.includes("upi")) {
      return `
        <div class="action-box">
          <div class="action-box-title">⚡ Immediate Action Steps & Bank Hotlines</div>
          <ol class="action-steps">
            <li><strong>Block UPI Access:</strong> Call your bank's toll-free number or call <strong>1930</strong> (National Cybercrime Helpline) to freeze connected payment handles.</li>
            <li><strong>Freeze Cards:</strong> Call your bank hotline immediately or log in via net banking to disable international/online transactions.</li>
          </ol>
          <div class="contact-chips">
            <a href="tel:1930" class="chip-btn red">📞 Cybercrime Helpline: 1930</a>
            <a href="tel:1800112211" class="chip-btn">📞 SBI: 1800-11-2211</a>
            <a href="tel:18602662666" class="chip-btn">📞 HDFC: 1860-266-2666</a>
            <a href="tel:18001080" class="chip-btn">📞 ICICI: 1800-1080</a>
            <a href="tel:18002584455" class="chip-btn">📞 Axis: 1800-258-4455</a>
          </div>
        </div>
      `;
    }

    if (cat.includes("sim") || t.includes("sim") || t.includes("telecom")) {
      return `
        <div class="action-box">
          <div class="action-box-title">📱 SIM Deactivation Hotlines (24x7)</div>
          <ol class="action-steps">
            <li>Call customer care from any alternative phone to block the stolen SIM card immediately and prevent OTP interception.</li>
            <li>Visit the nearest operator store with your ID proof to issue a duplicate SIM card with the same phone number.</li>
          </ol>
          <div class="contact-chips">
            <a href="tel:198" class="chip-btn">📞 Jio: 198 / 1800-889-9999</a>
            <a href="tel:121" class="chip-btn">📞 Airtel: 121 / 9810012345</a>
            <a href="tel:199" class="chip-btn">📞 Vi (Vodafone Idea): 199</a>
            <a href="tel:1503" class="chip-btn">📞 BSNL: 1503</a>
          </div>
        </div>
      `;
    }

    if (cat.includes("device") || t.includes("imei") || t.includes("ceir") || t.includes("lock")) {
      return `
        <div class="action-box">
          <div class="action-box-title">🔒 Remote Device Locking & Central IMEI Blocking</div>
          <ol class="action-steps">
            <li><strong>Remote Lock:</strong> Use Find My Device / iCloud Find My to remotely lock the device and trigger a logout.</li>
            <li><strong>Block IMEI Nationwide:</strong> Block your phone's IMEI on the official Government CEIR portal so it cannot be used on any SIM network in India.</li>
          </ol>
          <div class="contact-chips">
            <a href="https://ceir.gov.in/Request/CeirUserBlockRequestDirect.execution" target="_blank" class="chip-btn gold">🌐 Official CEIR IMEI Block Portal &rarr;</a>
            <a href="https://www.google.com/android/find/" target="_blank" class="chip-btn">🌐 Google Find My Device &rarr;</a>
            <a href="https://www.icloud.com/find" target="_blank" class="chip-btn">🌐 Apple iCloud Find My &rarr;</a>
          </div>
        </div>
      `;
    }

    if (cat.includes("legal") || t.includes("police") || t.includes("report") || t.includes("fir")) {
      return `
        <div class="action-box">
          <div class="action-box-title">📄 File FIR or Lost Article Report</div>
          <ol class="action-steps">
            <li>Copy the pre-filled police complaint draft generated below.</li>
            <li>Submit it to your nearest jurisdictional police station or file an online Lost Article Report on your state police web portal.</li>
            <li>Keep the stamped FIR copy / Lost Article Acknowledgement receipt number safely for issuing duplicate IDs.</li>
          </ol>
          <div class="contact-chips">
            <a href="https://cybercrime.gov.in" target="_blank" class="chip-btn red">🌐 National Cyber Crime Portal &rarr;</a>
            <a href="tel:112" class="chip-btn">📞 Police Emergency: 112</a>
          </div>
        </div>
      `;
    }

    if (cat.includes("document") || t.includes("aadhaar") || t.includes("pan") || t.includes("licence") || t.includes("digilocker")) {
      return `
        <div class="action-box">
          <div class="action-box-title">🪪 Identity Re-issuance & Official Digital Copies</div>
          <ol class="action-steps">
            <li>Access instant, legally valid digital identity documents via DigiLocker.</li>
            <li>Apply for physical duplicate reprints on official government portals using your police report reference number.</li>
          </ol>
          <div class="contact-chips">
            <a href="https://www.digilocker.gov.in/" target="_blank" class="chip-btn gold">🏛️ Official DigiLocker Portal &rarr;</a>
            <a href="https://myaadhaar.uidai.gov.in/" target="_blank" class="chip-btn">📄 myAadhaar Official Portal &rarr;</a>
            <a href="https://www.onlineservices.nsdl.com/paam/ReprintEPan.html" target="_blank" class="chip-btn">📄 PAN Duplicate Reprint &rarr;</a>
            <a href="https://parivahan.gov.in/" target="_blank" class="chip-btn">🚗 Parivahan Driving Licence &rarr;</a>
          </div>
        </div>
      `;
    }

    return "";
  }

  async function fetchComplaintDraft(caseId) {
    try {
      const res = await fetch("/api/v1/complaint/draft", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ case_id: caseId, police_station_name: "Local Jurisdiction Police Station" })
      });
      if (res.ok) {
        const data = await res.json();
        complaintDraftText.innerText = data.draft_text;
      }
    } catch (e) {
      console.error("Draft generation failed", e);
    }
  }

  // GLOBAL UTILITY FUNCTIONS FOR TRACKER & POLICE DISPATCH

  window.copyDraftText = function() {
    const text = document.getElementById("complaint-draft-text").innerText;
    navigator.clipboard.writeText(text);
    alert("Police Complaint Draft copied to clipboard!");
  };

  window.trackCaseById = async function() {
    const caseId = document.getElementById("lookup_case_id").value.trim().toUpperCase();
    if (!caseId) {
      alert("Please enter a valid Case ID (e.g. CASE-123456)");
      return;
    }

    try {
      const res = await fetch(`/api/v1/cases/${caseId}`);
      if (!res.ok) {
        alert("Case ID not found in database.");
        return;
      }

      const data = await res.json();
      document.getElementById("tracker-results").classList.remove("hidden");
      document.getElementById("tracked-case-header").innerText = `Case Reference: ${data.case_id}`;
      document.getElementById("tracked-status").innerText = data.status || "ACTIVE";
      document.getElementById("tracked-date").innerText = new Date(data.created_at).toLocaleString();

      const risk = data.risk_assessment;
      document.getElementById("tracked-risk-badges").innerHTML = `
        <span class="badge badge-${risk.financial_risk}">Financial: ${risk.financial_risk}</span>
        <span class="badge badge-${risk.identity_risk}">Identity: ${risk.identity_risk}</span>
        <span class="badge badge-${risk.digital_risk}">Digital: ${risk.digital_risk}</span>
      `;

      const checklistContainer = document.getElementById("tracked-checklist-container");
      checklistContainer.innerHTML = "";
      data.checklist.forEach(task => {
        const div = document.createElement("div");
        div.className = "checklist-card";
        div.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <strong>[${task.category}] ${task.title}</strong>
              <p style="font-size: 0.9rem; color: #6d5d53;">${task.instructions}</p>
            </div>
            <span class="badge badge-${task.priority}">${task.priority}</span>
          </div>
        `;
        checklistContainer.appendChild(div);
      });
    } catch (err) {
      alert("Error retrieving case: " + err.message);
    }
  };

  window.searchNearbyPolice = async function() {
    const query = document.getElementById("search_location").value.trim();
    if (!query) {
      alert("Please enter a location name or PIN code.");
      return;
    }

    try {
      const res = await fetch(`/api/v1/police/routing?location=${encodeURIComponent(query)}`);
      const data = await res.json();

      const container = document.getElementById("police-stations-list");
      container.innerHTML = `
        <div class="info-card" style="grid-column: 1 / -1;">
          <h3>Jurisdictional Station: ${data.station_name || "Central Police Station"}</h3>
          <p><strong>Primary Contact Helpline:</strong> <a href="tel:${data.contact_number || '112'}">${data.contact_number || '112'}</a></p>
          <p><strong>Station Address:</strong> ${data.address || query}</p>
          <p><strong>Online Portal:</strong> <a href="${data.online_portal || 'https://cybercrime.gov.in'}" target="_blank">State Police Cyber Portal &rarr;</a></p>
          <div class="contact-chips" style="margin-top: 12px;">
            <a href="tel:${data.contact_number || '112'}" class="chip-btn red">📞 Call Station Direct</a>
            <button onclick="autofillEmail('${data.station_email || 'sho.' + query.toLowerCase().replace(/[^a-z0-0]/g, '') + '@police.gov.in'}')" class="chip-btn gold">📧 Select for Email Dispatch</button>
          </div>
        </div>
      `;
    } catch (e) {
      alert("Error looking up police stations: " + e.message);
    }
  };

  window.autofillEmail = function(email) {
    document.getElementById("dispatch_email").value = email;
    alert(`Station email set to: ${email}`);
  };

  window.autofillStationFromCase = function() {
    const loc = document.getElementById("incident_location").value;
    if (loc) {
      document.getElementById("search_location").value = loc;
      searchNearbyPolice();
    }
  };

  window.dispatchDraftEmail = function() {
    const email = document.getElementById("dispatch_email").value.trim();
    const draft = document.getElementById("complaint-draft-text").innerText;

    if (!email) {
      alert("Please enter or select a police station email address.");
      return;
    }

    const subject = encodeURIComponent("EMERGENCY: Post-Theft Police Report / Loss Complaint");
    const body = encodeURIComponent(draft);
    window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
  };
});