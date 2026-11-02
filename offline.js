/* Mode hors-ligne (version web) : enregistre le service worker, affiche l'état dans le plan,
   propose de télécharger tous les sons, et resynchronise la progression au retour du réseau. */
(function () {
  if (!("serviceWorker" in navigator) || location.protocol === "file:") return;
  navigator.serviceWorker.register("sw.js").catch(e => console.warn("hors-ligne", e));

  const ask = (msg) => new Promise(ok => {
    const sw = navigator.serviceWorker.controller; if (!sw) return ok(null);
    const ch = new MessageChannel(); ch.port1.onmessage = ev => { if (ev.data.progress) { msg.onProgress && msg.onProgress(ev.data); return; } ok(ev.data); };
    sw.postMessage({ type: msg.type, urls: msg.urls }, [ch.port2]);
  });
  const packs = () => (typeof DATA !== "undefined" && DATA && DATA.packs) || [];

  function panel() {
    let el = document.getElementById("offline");
    const host = document.querySelector("#planSheet p.pr") || null;   // texte du plan
    if (!el && host) { el = document.createElement("div"); el.id = "offline"; el.className = "pr"; el.style.cssText = "margin:10px 0 0;display:flex;gap:10px;align-items:center;flex-wrap:wrap"; host.after(el); }
    return el;
  }
  async function render() {
    const el = panel(); if (!el) return;
    if (!navigator.serviceWorker.controller) { el.textContent = "Hors-ligne : disponible après le prochain chargement de la page."; return; }
    const s = await ask({ type: "audio-status", urls: packs() }); if (!s) return;
    const all = s.total && s.have === s.total;
    el.innerHTML = `<span>📴 Hors-ligne : l'app et les mots sont enregistrés sur cet appareil. Sons : ${s.have}/${s.total} salles${all ? " ✓" : ""}.</span>` +
      (all ? "" : `<button class="btn alt" type="button" id="offAudio">Télécharger tous les sons (≈16 Mo)</button>`);
    const b = document.getElementById("offAudio");
    if (b) b.onclick = async () => {
      b.disabled = true; b.textContent = "Téléchargement…";
      await ask({ type: "audio-fetch", urls: packs(), onProgress: p => { b.textContent = `Téléchargement… ${p.have}/${p.total}`; } });
      render();
    };
  }
  // le plan est construit par la page : on met l'état à jour à chaque ouverture
  const sheet = document.getElementById("planSheet");
  if (sheet) new MutationObserver(() => { if (!sheet.hidden) render(); }).observe(sheet, { attributes: true, attributeFilter: ["hidden"] });
  navigator.serviceWorker.addEventListener("controllerchange", () => setTimeout(render, 50));

  // retour du réseau : on renvoie la progression enregistrée localement
  window.addEventListener("online", () => {
    try { if (typeof store !== "undefined" && store.kind && typeof afterLogin === "function") afterLogin(); } catch (e) {}
    try { typeof toast === "function" && toast("De retour en ligne : progression synchronisée"); } catch (e) {}
  });
  window.addEventListener("offline", () => { try { typeof toast === "function" && toast("Hors-ligne : ta progression est gardée sur l'appareil"); } catch (e) {} });
})();
