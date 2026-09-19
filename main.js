/* Fuquay Fencing Pros — nav, lead forms, analytics events */
const LEAD_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/24209228/4dq1xf8/"; // Zapier Catch Hook. Blank = demo mode (logs, no send).

/* ---------- mobile nav ---------- */
(function(){
  const t=document.querySelector(".nav-toggle"), m=document.getElementById("mobile-nav");
  if(!t||!m) return;
  t.addEventListener("click",()=>{const o=m.classList.toggle("open");t.setAttribute("aria-expanded",String(o));});
  m.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{
    m.classList.remove("open");t.setAttribute("aria-expanded","false");}));
})();

/* ---------- footer year ---------- */
(function(){const y=document.getElementById("year");if(y)y.textContent=new Date().getFullYear();})();

/* ---------- call-click tracking (calls often outnumber form fills) ---------- */
(function(){
  document.querySelectorAll("a[data-call]").forEach(function(a){
    a.addEventListener("click",function(){
      try{ if(window.gtag) gtag("event","click_to_call",{event_category:"lead",
             event_label:location.pathname}); }catch(e){}
      try{ if(window.fbq) fbq("track","Contact",{content_name:"click_to_call",
             page:location.pathname}); }catch(e){}
    });
  });
})();

/* ---------- lead forms (one per page) ---------- */
(function(){
  const LOADED_AT = Date.now();
  document.querySelectorAll("form[data-lead-form]").forEach(function(form){
    const btn = form.querySelector('button[type="submit"]');
    const okBox = form.querySelector(".form-success");
    const errBox = form.querySelector(".form-error");

    form.addEventListener("submit", async function(e){
      e.preventDefault();
      errBox.hidden = true;
      if(!form.checkValidity()){ form.reportValidity(); return; }

      /* spam gates: honeypot + minimum dwell time */
      if(form.company && form.company.value){ okBox.hidden=false; return; }   // silent drop
      if(Date.now() - LOADED_AT < 3000){ okBox.hidden=false; return; }        // too fast to be human

      if(btn.getAttribute("aria-busy")==="true") return;
      btn.setAttribute("aria-busy","true");
      const label = btn.textContent; btn.textContent = "Sending…";

      const payload = {
        fullName: form.fullName.value.trim(),
        phone:    form.phone.value.trim(),
        email:    form.email.value.trim(),
        address:  form.address.value.trim(),
        zip:      form.zip.value.trim(),
        fenceType:form.fenceType.value,
        timeline: form.timeline.value,
        source:   "Website",
        pageSource: form.dataset.pageSource || location.pathname,
        submittedAt: new Date().toISOString(),
        pageUrl:  location.href
      };

      try{
        if(LEAD_WEBHOOK_URL){
          const r = await fetch(LEAD_WEBHOOK_URL,{method:"POST",
            headers:{"Content-Type":"application/json","Accept":"application/json"},
            body: JSON.stringify(payload)});
          if(!r.ok) throw new Error("HTTP "+r.status);
        } else {
          console.warn("No LEAD_WEBHOOK_URL set — demo mode.", payload);
          await new Promise(r=>setTimeout(r,400));
        }

        /* conversion events */
        try{ if(window.gtag) gtag("event","generate_lead",{event_category:"lead",
               event_label: payload.pageSource, fence_type: payload.fenceType}); }catch(e){}
        try{ if(window.fbq) fbq("track","Lead",{content_name: payload.pageSource,
               content_category: payload.fenceType}); }catch(e){}

        form.querySelectorAll(".field,.field-row,button[type=submit],.consent")
            .forEach(el=>el.style.display="none");
        okBox.hidden = false;
        okBox.scrollIntoView({behavior:"smooth",block:"center"});
      }catch(err){
        console.error("Lead submit failed:",err);
        errBox.hidden = false;
        btn.removeAttribute("aria-busy"); btn.textContent = label;
      }
    });
  });
})();
