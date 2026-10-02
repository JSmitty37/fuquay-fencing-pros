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
  document.querySelectorAll("form[data-lead-form]").forEach(function(form){
    const btn = form.querySelector('button[type="submit"]');
    const okBox = form.querySelector(".form-success");
    const errBox = form.querySelector(".form-error");
    /* No dwell timer. Autofill fires input on every field and the visitor
       often clicks Submit within a second. Drop only a submit that never had
       a field focus/input/change or a click, touch, or keydown in the form. */
    let interacted = false;
    function markField(ev){
      if(interacted) return;
      const t = ev.target;
      if(!t || !t.matches || !t.matches("input, select, textarea")) return;
      interacted = true;
    }
    function markGesture(){ interacted = true; }
    form.addEventListener("focusin", markField);
    form.addEventListener("input", markField);
    form.addEventListener("change", markField);
    form.addEventListener("click", markGesture);
    form.addEventListener("touchstart", markGesture, {passive:true});
    form.addEventListener("keydown", markGesture);

    function dropSubmit(reason){
      console.warn("Lead submit dropped:", reason);
      try{ if(window.gtag) gtag("event","form_submit_dropped",{event_category:"lead",
             event_label: form.dataset.pageSource || location.pathname,
             drop_reason: reason}); }catch(err){}
      okBox.hidden = false;
    }

    function zipFromAddress(address){
      const text = String(address || "");
      const zipRe = /\b(\d{5})(?:-\d{4})?\b/g;
      const stateRe = /\b(?:NC|North Carolina)\b/gi;
      let stateMatch, followed = "";
      while((stateMatch = stateRe.exec(text))){
        const after = text.slice(stateMatch.index + stateMatch[0].length);
        const z = after.match(/\b(\d{5})(?:-\d{4})?\b/);
        if(z) followed = z[1];
      }
      if(followed) return followed;
      const all = [];
      let m;
      while((m = zipRe.exec(text))) all.push(m[1]);
      for(let i = all.length - 1; i >= 0; i--) if(all[i].indexOf("27") === 0) return all[i];
      return all.length ? all[all.length - 1] : "";
    }

    form.addEventListener("submit", async function(e){
      e.preventDefault();
      errBox.hidden = true;
      if(!form.checkValidity()){ form.reportValidity(); return; }

      /* spam gates: honeypot stays a silent drop; no-interaction drops are logged */
      if(form.company && form.company.value){ okBox.hidden=false; return; }
      if(!interacted){
        dropSubmit("no_user_interaction");
        return;
      }

      if(btn.getAttribute("aria-busy")==="true") return;
      btn.setAttribute("aria-busy","true");
      const label = btn.textContent; btn.textContent = "Sending…";

      const address = form.address.value.trim();
      const payload = {
        fullName: form.fullName.value.trim(),
        phone:    form.phone.value.trim(),
        email:    (form.email && form.email.value ? form.email.value : "").trim(),
        address:  address,
        zip:      zipFromAddress(address),
        fenceType:form.fenceType.value,
        timeline: form.timeline.value,
        source:   "Website",
        pageSource: form.dataset.pageSource || location.pathname,
        submittedAt: new Date().toISOString(),
        pageUrl:  location.href
      };

      try{
        if(LEAD_WEBHOOK_URL){
          /* Form-urlencoded is CORS-safelisted, so the browser POSTs without a
             preflight. application/json is not: Zapier's Catch Hook omits
             Access-Control-Allow-Headers on OPTIONS, and the browser blocks the
             lead ("content-type is not allowed") before the POST is sent.
             Field names are unchanged so existing Zap maps still match. */
          const r = await fetch(LEAD_WEBHOOK_URL,{method:"POST",
            body: new URLSearchParams(payload)});
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
